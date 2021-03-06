#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Project -> File   ：PycharmProjects -> phserver
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 11:02 AM
@Desc   ：
=================================================="""
import socket
import multiprocessing
import time
import os
import sys
from queue import Empty
import signal
import traceback

from request import HttpRequest
from request import ResponseCode
from utils import *
from web.conf import Conf

import types
import selectors
import json

__author__ = 'toiler'
__email__ = 'zhengbangdong.zh@ccbft.com'
__version__ = '0.0.0.1'
__server__ = 'PHServer'
__date__ = '1/18/2020 11:02 AM'

if __name__ == '__main__':
    from optparse import OptionParser
    cmd_parser = OptionParser(usage="usage: %prog [options] package.module:app")
    _opt = cmd_parser.add_option
    _opt("-v", "--version", action="store_true", help="show version number.")
    _opt("--debug", action="store_true", help="start server in debug mode.")
    _opt("--reload", action="store_true", help="auto-reload on file changes.")
    _opt("--shutdown", action="store_true", help="shutdown this server.")
    _opt("-p","--port", action="store", type='int', dest='port', default='8010',
         help="server listen port, default 8010.")
    _opt("-b", "--bind", action="store", type='string', dest="host", default='0.0.0.0',
         help="bind socket to ADDRESS.default 0.0.0.0 ")
    _opt("--process", action="store", type='int', dest='process', default='1',
         help="server process number, default 5.")
    _opt("--queue", action="store", type='int', dest='queue', default='50',
         help="server queue number, default 50.")
    cmd_options, cmd_args = cmd_parser.parse_args()


def te(work_queue, alive_sock_queue):
    my_print('Work process wait task.')
    # conn = sqlite3.connect('my_sqlite3.db')
    if Conf.db_module:
        __import__(Conf.db_module)
        lib = sys.modules[Conf.db_module]
        _db = lib.DB(Conf.db_file_path_rw)
        _img_db = lib.DB(Conf.db_file_path_img)
    else:
        _db = None
        _img_db = None
    i = 0
    while i < 100000000:
        # 接收sock， 放入选择队列
        try:
            # my_print("中断标志: {0}".format(self.term_flag))
            func, args = work_queue.get(block=True, timeout=1.0)
            func(*args, alive_sock_queue, _db, _img_db)
        except Empty:
            pass
        except BaseException:  # ignore all exception
            my_print('pool {0}'.format(traceback.format_exc(), ))
            time.sleep(0.001)
    if _db:
        _db.close()

    my_print('exit.')


class ProcessPool(object):
    def __init__(self, process_number, queue_maxsize):
        self.process_number = process_number
        self.work_queue = multiprocessing.Queue(maxsize=queue_maxsize)
        self.alive_sock_queue = multiprocessing.Queue(maxsize=queue_maxsize)
        self.sel = selectors.DefaultSelector()
        self.pools = []
        self.term_flag = False
        for i in range(self.process_number):
            # p = multiprocessing.Process(target=self.e, args=(self.work_queue, self.alive_sock_queue))
            p = multiprocessing.Process(target=te, args=(self.work_queue, self.alive_sock_queue))
            p.daemon = True
            p.start()
            self.pools.append(p)

    def _term_handler(self, signal_num, frame):
        print('[%d] pool ' % os.getpid() + " get Termination num is {} {}".format(signal_num, frame))
        self.term_flag = True

    def e(self, work_queue, alive_sock_queue):
        signal.signal(signal.SIGTERM, self._term_handler)  # SIGTERM 关闭程序信号
        signal.signal(signal.SIGINT, self._term_handler)  # 接收ctrl+c 信号
        my_print('Work process wait task.')
        # conn = sqlite3.connect('my_sqlite3.db')
        if Conf.db_module:
            __import__(Conf.db_module)
            lib = sys.modules[Conf.db_module]
            _db = lib.DB()
        else:
            _db = None
        while not self.term_flag:
            # 接收sock， 放入选择队列
            try:
                # my_print("中断标志: {0}".format(self.term_flag))
                func, args = work_queue.get(block=True, timeout=1.0)
                func(*args, alive_sock_queue, _db)
            except Empty:
                pass
            except BaseException:  # ignore all exception
                my_print('pool {0}'.format(traceback.format_exc(),))
                time.sleep(0.001)
        if _db:
            _db.close()

        my_print('exit.')

    def add_work(self, func, *args):
        if not self.term_flag:
            self.work_queue.put((func, args))


def tcp_link(sock, addr, alive_sock_queue, _db, _img_db):
    t_start = time.time()
    my_print('Accept new connection from {0}...'.format(addr,))
    exception_trace_id = generate_trace_id()
    exception_message = None
    has_exception = True

    req = HttpRequest(sock, addr, _db=_db, _img_db=_img_db, trace_id=exception_trace_id)
    need_send = False
    try:
        success = req.do()
        if success:   # 成功的请求，以后可以缓存
            pass
        has_exception = False
        need_send = True
    except Exception as e:
        tb = traceback.format_exc()
        if str(e).find('client socket closed.') != -1:
            return
        exception_message = str(e)
    except BaseException as be:
        tb = traceback.format_exc()
        exception_message = str(be)

    if has_exception:
        my_print('tcp_link TraceId:{0} {1} {2}'.format(exception_trace_id, exception_message, tb))
        req.res_command = ResponseCode.INNER_ERROR
        body = dict()
        body['status'] = 9999
        body['message'] = exception_message
        body['traceId'] = exception_trace_id
        ymp = json.dumps(body, ensure_ascii=False)
        req.res_body = ymp.encode('UTF-8')
        req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
        need_send = True

    if need_send:
        if req.res_body is None or 0 == len(req.res_body):
            my_print("trace_id:{} header:{} body:{}".format(req.trace_id, req._raw_head, get_print_string(req._raw_body)))
            req.res_body = 'UNKNOWN ERROR,trace_id:{} req.trace_id:{}'.format(
                req.trace_id, req.parameters.get('trace_id', None)).encode('utf-8')
            req.res_command = b"HTTP/1.1 500 OK\r\n"
        req.res_head['Content-Length'] = str(len(req.res_body))
        response_header = dict2header(req.res_head).encode('UTF-8')
        if Conf.get('is_save_response'):
            write_to_file(Conf.get('save_response_file_path'), req.get_res_data())
        sock.sendall(req.res_command)
        sock.sendall(response_header)
        sock.sendall(req.res_body)

        if req.res_head.get('Connection', 'Close').lower() == 'keep-alive':
            data = types.SimpleNamespace(sock=sock, addr=addr)
            alive_sock_queue.put(data)
        else:
            sock.close()
    else:
        sock.close()

    t_stop = time.time()
    print("[%d] %s,%s %s %.5f" % (os.getpid(), addr[0], addr[1], req.command.command, t_stop - t_start))


class Server(object):
    def __init__(self, host='127.0.0.1', port=9999, listen_number=5, process_number=5, queue_number=10):
        self.term_flag = False
        self.host = host
        self.port = port
        self.listen_number = listen_number
        self.process_number = process_number
        self.queue_number = queue_number
        self.pool = ProcessPool(self.process_number, self.queue_number)
        self.sel = selectors.DefaultSelector()
        self.pid_file = os.path.split(os.path.realpath(sys.argv[0]))[0] + "/pid_file.lock"  # 获取运行路径

    def accept_wrapper(self, listen_sock):
        sock, addr = listen_sock.accept()
        print('[%d] Accept new connection %s' % (os.getpid(), addr))
        sock.setblocking(False)
        data = types.SimpleNamespace(addr=addr, sock=sock, inb=b'', outb=b'')
        self.sel.register(sock, selectors.EVENT_READ, data=data)

    def service_connection(self, key, mask):
        if mask == selectors.EVENT_READ:
            self.sel.unregister(key.fileobj)
            key.fileobj.setblocking(True)
            self.pool.add_work(tcp_link, *(key.fileobj, key.data.addr))

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(False)
        s.settimeout(60)
        s.bind((self.host, self.port))
        s.listen(self.listen_number)
        print('listen in %s:%d' % (self.host, self.port))

        self.sel.register(s, selectors.EVENT_READ, data=None)
        # SIGTERM 关闭程序信号
        signal.signal(signal.SIGTERM, self._term_handler)
        # 接收ctrl+C 信号 (Ctrl+C -->SIGINT; Ctrl+\ -->SIGQUIT; Ctrl+Z -->SIGTSTP
        signal.signal(signal.SIGINT, self._term_handler)
        self.record_pid()
        while not self.term_flag:
            try:
                events = self.sel.select(timeout=0.05)
                for key, mask in events:
                    # If None indicates a socket for listening
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)

                while True:
                    try:
                        data = self.pool.alive_sock_queue.get(block=False)
                        data.sock.setblocking(False)
                        self.sel.register(data.sock, selectors.EVENT_READ, data)
                    except Empty:
                        break
            except BaseException as be:  # ignore all exception
                print('[%d] pool ' % os.getpid() + traceback.format_exc())
                # continue

            # events = self.sel.select(timeout=1.02)
            # print('selectors', events)
            # for key, mask in events:
            #     if mask == selectors.EVENT_READ:  # 只有这种情况注册了，只需要处理这一种情况
            #         self.sel.unregister(key.fileobj)

    def _term_handler(self,signal_num,frame):
        print('[%d] server' % os.getpid() + " get Termination num is {} {}".format(signal_num, frame))
        self.term_flag = True

    def terminate(self):
        for p in self.pool.pools:
            p.terminate()

    def record_pid(self):
        pid = str(os.getpid())
        fd = open(self.pid_file, 'w+')
        fd.write("%s\n" % pid)
        fd.close()

    def stop(self):
        """
        Stop the server
        """
        try:
            pf = open(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "file %s does not exist. Daemon not running?\n"
            print(message % self.pid_file)
            return  # not an error in a restart

        # Try killing the main process
        try:
            retry_count = 5    #尝试几次以后，直接用kill -9
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.5)
                retry_count -= 1
                if retry_count == 0:
                    os.kill(pid, signal.SIGKILL)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                print(err)
        except BaseException as be:
            print(be)


if __name__ == '__main__':
    if cmd_options.version:
        print('Server %s %s %s\n' % (__server__, __version__, __date__))
        exit(0)

    if cmd_options.shutdown:
        Server.stop(None)
        exit(1)

    s = Server(host=cmd_options.host, port=cmd_options.port,
               process_number=cmd_options.process, queue_number=cmd_options.queue)
    s.run()

