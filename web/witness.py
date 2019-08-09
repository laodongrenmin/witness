#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/7/12 9:03'


def do(req):
    pass

# return byte 已经编码好的字符流
def do_post(req):
    from HttpRequest import HttpRequest
    # json 字符串格式返回
    body = dict()
    body["result"] = "failed"
    if isinstance(req, HttpRequest):
        req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
        code = req.parameters.get('code',None)
        if code:

            cur = req.db_conn.cursor()
            cur.execute("select code, name, memo, image from witness where code=?", (code,))
            rows = cur.fetchone()
            # 数据库里有，就看是借还是还，没有就需要添加
            if rows:
                print(rows)
            else:
                cur.execute("insert into witness(code,name,memo,image) values(?,?,?,?)", (code, 'test', 'test is a good.', bytearray(b'abcdef')))
                req.db_conn.commit()
                body["type"] = "new"

            body["result"] = "success"
            body["code"] = code
        else:
            body["reason"] = "no code"
        req.res_body = json.dumps(body).encode('UTF-8')
    else:
        raise Exception('para req is not HttpRequest')
    req.res_body = json.dumps(body).encode('UTF-8')
    return True

def do_get(req):
    req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
    req.res_body = '{"result":"failed","reason":"get method is developing"}'.encode('UTF-8')
    return True

if __name__ == '__main__':
    exit(0)