# -*- coding=utf-8 -*-
import socket
import multiprocessing
import time
import os, sys
from queue import Empty
import signal
import traceback

from HttpRequest import HttpRequest
from HttpRequest import ResponseCode
from tools import utils

import types
import sqlite3
import selectors

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__server__ = 'HFServer'

if __name__ == '__main__':
    from optparse import OptionParser
    cmd_parser = OptionParser(usage="usage: %prog [options] package.module:app")
    _opt = cmd_parser.add_option
    _opt("-v","--version", action="store_true", help="show version number.")
    _opt("-b", "--bind", metavar="ADDRESS", help="bind socket to ADDRESS.")
    _opt("--debug", action="store_true", help="start server in debug mode.")
    _opt("--reload", action="store_true", help="auto-reload on file changes.")
    _opt("--shutdown", action="store_true", help="shutdown this server.")
    cmd_options, cmd_args = cmd_parser.parse_args()


class ProcessPool():
    def __init__(self, process_number, queue_maxsize):
        self.process_number = process_number
        self.work_queue = multiprocessing.Queue(maxsize=queue_maxsize)
        self.alive_sock_queue = multiprocessing.Queue(maxsize=queue_maxsize)
        self.sel = selectors.DefaultSelector()
        self.pools = []
        self.term_flag = False
        for i in range(self.process_number):
            p = multiprocessing.Process(target=self.e, args=(self.work_queue,self.alive_sock_queue))
            p.daemon = True
            p.start()
            self.pools.append(p)

    def _term_handler(self,signal_num, frame):
        print('[%d] pool ' % os.getpid() + " get Termination num is {} {}".format(signal_num, frame))
        self.term_flag = True

    def e(self, work_queue, alive_sock_queue):
        signal.signal(signal.SIGTERM, self._term_handler)  # SIGTERM 关闭程序信号
        signal.signal(signal.SIGINT, self._term_handler)  # 接收ctrl+c 信号
        print('[%d] Work process wait task.' % os.getpid())
        conn = sqlite3.connect('my_sqlite3.db')
        while not self.term_flag:
            # 接收sock， 放入选择队列
            try:
                # print(os.getpid(),self.term_flag)
                func, args = work_queue.get(block=True, timeout=1.0)
                func(*args, alive_sock_queue, conn)
            except Empty:
                pass
            except BaseException:  # ignore all exception
                print('[%d] pool %s' % (os.getpid(), traceback.format_exc()))
                time.sleep(0.001)
                pass
        conn.close()
        print('[%d] exit.' % os.getpid())

    def add_work(self, func, *args):
        if not self.term_flag:
            self.work_queue.put((func, args))


def tcp_link(sock, addr, alive_sock_queue, conn):
    # print('[%d] conn id:%d ' % (os.getpid(), id(conn)))
    t_start = time.time()
    # print('[%d]' % os.getpid() + ' Accept new connection from %s:%s...' % (addr), sock)
    exception_trace_id = None

    req = HttpRequest(sock, addr, conn)
    need_send = False
    try:
        need_send = req.do()
    except Exception as e:
        if str(e).find('client socket closed.') != -1:
            return
        exception_trace_id = utils.generate_id() + ' ' + str(e)
        print('[%d] tcp_link TraceId:%s %s' % (os.getpid(), exception_trace_id, traceback.format_exc()))
    except BaseException as be:
        exception_trace_id = utils.generate_id() + ' ' + str(be)
        print('[%d] tcp_link TraceId:%s %s' % (os.getpid(), exception_trace_id, traceback.format_exc()))

    if exception_trace_id:
        req.res_command = ResponseCode.INNER_ERROR
        req.res_body = ("Exception traceId: %s " % exception_trace_id).encode('UTF-8')
        req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
        need_send = True

    if need_send:
        req.res_head['Content-Length'] = str(len(req.res_body))
        response_header = utils.dict2header(req.res_head).encode('UTF-8')
        # print(req.res_command)
        # print(response_header)
        # print(req.res_body)
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

        signal.signal(signal.SIGTERM, self._term_handler)  # SIGTERM 关闭程序信号
        signal.signal(signal.SIGINT, self._term_handler)   # 接收ctrl+C 信号 (Ctrl+C -->SIGINT; Ctrl+\ -->SIGQUIT; Ctrl+Z -->SIGTSTP
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
        pidfile = os.path.split(os.path.realpath(sys.argv[0]))[0] + "/pidfile.lock"  # 获取运行路径
        fd = open(pidfile, 'w+')
        fd.write("%s\n" % pid)
        fd.close()

    def stop(self):
        """
        Stop the server
        """
        pidfile = os.path.split(os.path.realpath(sys.argv[0]))[0] + "/pidfile.lock"  # 获取运行路径

        # Get the pid from the pidfile
        try:
            pf = open(pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "file %s does not exist. Daemon not running?\n"
            print(message % pidfile)
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
                if os.path.exists(pidfile):
                    os.remove(pidfile)
            else:
                print(err)
        except BaseException as be:
            print(be)


if __name__ == '__main__':
    if cmd_options.version:
        print('Server %s\n'%__version__)
        exit(0)

    if cmd_options.shutdown:
        Server.stop(None)
        exit(1)

    s = Server(host='0.0.0.0', port=8010, process_number=5, queue_number=15)
    s.run()
