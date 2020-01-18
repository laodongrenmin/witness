#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng, UserDto

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/11/29 08:42'


def do(req):
    pass


# return byte 已经编码好的字符流
def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 1
    req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
    if isinstance(req, HttpRequest):
        # code, user_id, user_name, name, memo, image, create_time
        paras = req.parameters
        login_name = paras['userInfo'].get('login_name', None)
        name = paras['userInfo'].get('name', None)
        memo = paras['userInfo'].get('dept_name', None)
        mobile = paras['userInfo'].get('mobile',None)

        if name and memo and login_name and mobile:
            body['op_type'] = 64   # 新增用户
            _user = dbMng.get_user_by_logname(login_name)
            if _user:
                body['message'] = '已经存在用户：%s(%s)' % (_user.name, _user.log_name)
                body['user'] = _user.to_dict()
                body['status'] = 2
            else:
                _user = dbMng.get_or_create_user(UserDto(log_name=login_name, name=name, memo=memo, mobile=mobile))
                if _user:
                    body['message'] = '成功添加用户：%s(%s)' % (_user.name, _user.log_name)
                    body['user'] = _user.to_dict()
                    body['status'] = 0
                else:
                    body['message'] = '出现未知错误'
        else:
            body["message"] = "用户名称、用户唯一标识、用户部门、联系方式为必要项目。"
        req.res_body = json.dumps(body, ensure_ascii=False).encode('UTF-8')
    else:
        raise Exception('para req is not HttpRequest')
    return True


def do_get(req: HttpRequest):
    req.res_head['Content-Type'] = 'application/json; charset=UTF-8'
    req.res_body = '{"status":"1","message":"get method is developing"}'.encode('UTF-8')
    return True


if __name__ == '__main__':
    exit(0)