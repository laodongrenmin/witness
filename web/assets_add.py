#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from HttpRequest import HttpRequest
from web.DBMng import dbMng, AssetsDto

__author__ = 'laodongrenmin'
__version__ = '0.0.0.1'
__date__ = '2019/7/24 19:51'


def do(req):
    pass


# return byte 已经编码好的字符流
def do_post(req: HttpRequest):
    # json 字符串格式返回
    body = dict()
    body['status'] = 2
    req.res_head['Content-Type'] = 'text/html; charset=UTF-8'
    if isinstance(req, HttpRequest):
        # code, user_id, user_name, name, memo, image, create_time
        paras = req.parameters
        code = paras.get('code', None)
        name = paras.get('name', None)
        memo = paras.get('memo', None)
        image = paras.get('image', None)
        # 应该从session里面取，现在用前端送上来
        login_name = paras.get('userInfo.login_name', None)
        if not login_name:
            userInfo = paras.get('userInfo')
            if userInfo:
                login_name = paras['userInfo'].get('login_name', None)
        # --------------------------------------------------------------

        if code and name and login_name:
            body['op_type'] = 1   # 新建资产
            body['status'] = 1
            _assets = dbMng.get_assets_bycode(code=code)
            if _assets:
                body['assets'] = _assets.to_dict()
                body['message'] = '已经存在相同编码的资产，请重新编码'
            else:
                _user = dbMng.get_user_by_logname(login_name)
                _assets = AssetsDto(code=code, user_id=_user.id, user_name=_user.name, name=name, memo=memo, image=image)
                dbMng.do_biz(_user, _assets)
                _assets = dbMng.get_assets_bycode(code)
                if _assets:
                    body['message'] = '已经成功添加资产到资产库'
                    body['status'] = 0
                    body['assets'] = _assets.to_dict()
                else:
                    body['message'] = '出现未知错误'
        else:
            body["message"] = "没有上送资产编码 或者 没有登陆认证获取不到用户信息"
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