#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> request
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 11:18 AM
@Desc   ：
=================================================="""
from urllib import parse
from utils import generate_trace_id
from web.conf import Conf
import os
import sys
import datetime
import json

from watchdog.observers import Observer
from watchdog.events import *
from threading import Thread
from functools import lru_cache


# 文件监控事件接收处理器
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, cache_func, monitor_path):
        FileSystemEventHandler.__init__(self)
        self.update_flag = False
        self.cache_func = cache_func
        self.observer = Observer()
        self.observer.schedule(self, monitor_path, True)
        self.observer.start()
        p = Thread(target=self.clear_task, args=(self,), daemon=True)
        p.start()

    def on_moved(self, event):
        print("[%d] on_moved: %s to %s" % (os.getpid(), event.src_path, event.dest_path))
        self.update_flag = True

    def on_created(self, event):
        print("[%d] on_created: %s" % (os.getpid(), event.src_path))
        self.update_flag = True

    def on_deleted(self, event):
        print("[%d] on_deleted: %s" % (os.getpid(), event.src_path))
        self.update_flag = True

    def on_modified(self, event):
        print("[%d] on_modified: %s" % (os.getpid(), event.src_path))
        self.update_flag = True

    def stop(self):
        self.observer.stop()

    def clear_task(self, file_event_handle):
        import time
        print("[%d] clear_task thread running..." % (os.getpid()))
        while True:
            time.sleep(1)
            if file_event_handle.update_flag:
                print("[%d] cache_clear." % (os.getpid()))
                file_event_handle.update_flag = False
                file_event_handle.cache_func.cache_clear()


# 获取静态网页文本内容，并缓存, 文件大了有风险,一般不会太大，就是网站静态页面的大小
@lru_cache(maxsize=None, typed=True)
def get_file_content(file_path):
    print("[%d] read file： %s." % (os.getpid(), file_path))
    f = open(file_path, 'rb')
    b = f.read()
    f.close()
    return b


event_handler = FileEventHandler(get_file_content, os.path.join(os.path.split(os.path.realpath(__file__))[0], "root"))


# 返回码
class ResponseCode(object):
    OK = b"HTTP/1.1 200 OK\r\n"
    INNER_ERROR = b"HTTP/1.1 500 OK\r\n"
    NOT_FOUND = b"HTTP/1.1 404 Not Found\r\n"
    BAD_REQUEST = b'HTTP/1.1 400 Bad Request\r\n'
    NOT_IMPLEMENTED = b'HTTP/1.1 501 Not Implemented\r\n'


class Command(object):
    def __init__(self, request_line, paras):
        self.method, self.path, self.protocol = request_line.decode('UTF-8').split(' ')
        self.method = self.method.upper()
        self.path = parse.unquote(self.path)
        self.command = '%s %s %s' % (self.method, self.path, self.protocol)
        k_v = self.path.split('?', 1)
        if len(k_v) == 2:
            self.path = k_v[0]
            k_v = k_v[1].split('&')
            for o in k_v:
                kv = o.split("=")
                if len(kv) == 2:
                    paras[kv[0]] = kv[1]


class ContentType(object):
    """
    Content-Type: application/json; charset=utf-8
    Content-Type: text/html; charset=utf-8
    Content-Type: multipart/form-data; boundary=something
    """

    def __init__(self, content_type):
        self.content_type = content_type

        pos = self.content_type.lower().find('charset=')
        if pos != -1:
            self.charset = content_type[pos + 8:]
        else:
            self.charset = 'utf-8'

    def get_charset(self):
        return self.charset

    def is_json(self):
        return self.content_type.lower().find('application/json') != -1

    def is_form_data(self):
        return self.content_type.lower().find('multipart/form-data') != -1

    def get_boundary(self):
        pos = self.content_type.lower().find('boundary=')
        if pos != -1:
            return self.content_type[pos + 9:]
        else:
            return None


class AttachFile(object):
    def __init__(self, _filed_head, _filed_content):
        self.head = _filed_head
        self.content = _filed_content
        self.name = re.sub('name="|";', '', re.findall('name=".+";', self.head)[0])
        tmp_content_type = re.findall('Content-Type:.+', self.head)
        if len(tmp_content_type) == 0:
            tmp_content_type = re.findall('content-type:.+', self.head)
        else:
            self.content_type = re.sub('Content-Type: ', '', tmp_content_type[0])
        if len(tmp_content_type) == 0:
            raise Exception('Attachfile Content-Type or content-type not found.')
        else:
            self.content_type = re.sub('Content-Type: ', '', tmp_content_type[0])

        self.file_name = re.sub('filename="|"', '', re.findall('filename=".+"', self.head)[0])

    def get_bytes(self):
        return self.name, self.head.encode('UTF-8') + b'\r\n\r\n' + self.content[0:-2]


class HttpRequest(object):
    root_url = Conf.root_url

    gmt_format = '%a, %d %b %Y %X GMT+0800(CST)'

    def __init__(self, sock=None, addr=None, db_conn=None):
        self.sock = sock
        self.addr = addr
        self.db_conn = db_conn
        # self.rfile = sock.makefile("rb", -1)
        # self.wfile = sock.makefile('wb', 0)

        self.command = None
        self.req_head = dict()
        self._raw_head = bytearray()
        self._raw_body = bytearray()

        self.parameters = dict()

        self.files = list()

        self.res_command = ResponseCode.INNER_ERROR
        self.res_head = dict()
        self.res_body = None

    def parse_head(self, line):
        line = line.decode('UTF-8').strip('\r\n')
        k_v = line.split(': ', 1)
        if len(k_v) == 2:
            self.req_head[k_v[0].title()] = k_v[1]
        else:
            self.req_head[k_v] = ''

    def recv_head(self):
        request_line = self.sock.recv(4096)
        pos = request_line.find(b'\r\n\r\n')
        if pos > 0:
            # print(request_line)
            self._raw_head[0:] = request_line[0:pos]
            self._raw_body[0:] = request_line[pos + 4:]

            request_line, request_head = self._raw_head.split(b'\r\n', 1)
            self.command = Command(request_line, self.parameters)

            k_v = request_head.split(b'\r\n')
            for head_line in k_v:
                if len(head_line) == 0:
                    continue
                self.parse_head(head_line)
        else:
            if not request_line:
                print('[%d] client socket closed. %s' % (os.getpid(), self.addr))
            else:
                print("[%d] read head wrong. %s" % (os.getpid(), self.addr))
            self.sock.close()
            raise Exception('client socket closed.')

    def parse_body(self):
        # print(self._raw_head)
        # print(self._raw_body)
        content_type = ContentType(self.req_head['Content-Type'])
        if content_type.is_json():
            self.parameters.update(json.loads(self._raw_body.decode('UTF-8')))
            return True
        elif content_type.is_form_data():  # 解析字段以及附件
            boundary = content_type.get_boundary()
            sp = bytearray('--'.encode('utf-8'))
            sp[2:] = boundary.encode('UTF-8')
            tmps = self._raw_body.split(sp)
            for tmp in tmps:
                print(tmp)
                if not tmp or tmp == b'--\r\n':
                    continue
                head_content = tmp.split(b'\r\n\r\n', 2)
                if len(head_content) == 2:
                    head, content = head_content
                    head = head.decode('utf-8')

                    if head.find('filename="') != -1:
                        # 文件
                        name, value = AttachFile(head, content).get_bytes()
                    else:
                        # 字段
                        name = re.sub('name="|"', '', re.findall('name=".+"', head)[0])
                        content = content.decode('UTF-8')
                        value = content.strip('\r\n')
                    self.parameters[name] = value
            '''
            ---------------------------974767299852498929531610575
            Content-Disposition: form-data; name="description" 

            some text
            ---------------------------974767299852498929531610575
            Content-Disposition: form-data; name="myFile"; filename="foo.txt" 
            Content-Type: text/plain 

            (content of the uploaded file foo.txt)
            ---------------------------974767299852498929531610575--
            '''
        return False

    def recv_body(self):
        content_length = int(self.req_head.get('Content-Length', '-1'))
        size = len(self._raw_body)
        if size <= content_length:
            while size < content_length:
                self._raw_body[size:] = self.sock.recv(1024)
                size = len(self._raw_body)
                if size == content_length:
                    break

            return self.parse_body()
        else:
            return False

    # 只提供制定类型的静态文件
    def static_request(self):

        mimi_type = {
            ".html": "text/html", ".htm": "text/html",
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".ico": "image/x-icon", ".js": "application/x-javascript"
        }
        path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "root")
        cp = self.command.path
        if cp.startswith(self.root_url):
            cp = cp[len(self.root_url) + 1:]
        elif cp.startswith('/'):
            cp = cp[1:]
        else:
            cp = cp[0:]
        p = os.path.join(path, cp)  # 去掉头 /wtn/ or /
        if not os.path.isfile(p):
            self.res_head['Content-Type'] = 'text/html'
            p = os.path.join(path, '404.html')
            self.res_command = ResponseCode.NOT_FOUND
        else:
            extension_name = os.path.splitext(p)[1]  # 扩展名
            self.res_head['Content-Type'] = mimi_type.get(extension_name, "application/octet-stream")
            self.res_command = ResponseCode.OK

        self.res_head['Cache-Control'] = 'max-age=31536000'
        self.res_head['Expires'] = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime(self.gmt_format)

        self.res_body = get_file_content(p)
        # f = open(p, 'rb')
        # # 文件大了就有隐患
        # self.res_body = f.read()
        return True

    def pre(self):
        # 返回True 需要后续发送， False 不需要, 在调用动态方式时候使用
        # Date: Mon, 08 Jul 2019 09:18:15 GMT
        # Server: WSGIServer / 0.2
        self.res_head['Server'] = 'HFServer/0.0.0.1'

        self.res_head['Date'] = datetime.datetime.now().strftime(self.gmt_format)

        keep_alive = self.req_head.get('Connection', 'Close')
        self.res_head['Connection'] = keep_alive  # 'Keep-Alive' or 'Close' 需要检查报文头，是close，还是keep-Alive
        cookie = self.req_head.get('Cookie', '')
        # print('[%d] %s' %(os.getpid(), cookie) )
        if cookie:
            if cookie.upper().find('PSESSIONID=') == -1:
                cookie = "psessionid=%s;" % generate_trace_id()
        else:
            cookie = "psessionid=%s;" % generate_trace_id()

        self.res_head['Set-Cookie'] = cookie

        m = Conf.router.get(self.command.path, None)
        # 没有配置，当静态资源直接打开文件返回了
        if not m:
            # 以后使用配置文件，确定根目录
            return self.static_request()
        else:
            # 此处代码，需要添加缓存，只寻找一次
            __import__(m)
            lib = sys.modules[m]
            if self.command.method == 'POST':
                func = lib.do_post
            elif self.command.method == 'GET':
                func = lib.do_get
            else:
                func = lib.do  # 处理post、get之外的其他任何操作
            self.res_command = ResponseCode.OK
            self.res_head['Cache-Control'] = 'no-cache,must-revalidate,no-store'
            self.res_head['Pragma'] = 'no-cache'
            return func(self)

    def do(self):
        self.recv_head()
        self.recv_body()
        return self.pre()