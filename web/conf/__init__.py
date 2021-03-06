#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PycharmProjects -> __init__.py
@IDE    ：PyCharm
@Author ：Mr. toiler
@Date   ：1/18/2020 10:34 AM
@Desc   ：
=================================================='''
__all__ = ['Conf']


class Conf(object):
    # 访问的根，必须配置
    root_url = '/wtn'
    is_print_req_head = False
    is_print_req_body = False
    is_print_req_paras = True

    # ----------------------  db_config  ---------------------------
    # 是否打印执行的SQL
    is_print_sql = True

    # db 处理类
    db_module = 'web.dao.db'
    db_file_path_rw = 'my_sqlite3_1.db'

    db_file_path_img = 'my_sqlite3_img.db'

    # -------------------- app -----------------------------------
    # 是否把返回的报文保存到文件
    is_save_response = True
    save_response_file_path = 'response.log'

    @staticmethod
    def get(para_name, default=None):
        if para_name in Conf.__dict__.keys():
            return Conf.__dict__[para_name]
        return default

    # ----------------------  router  ---------------------------
    # 路由，请求Url和处理模块的对应关系
    # 模块需要实现 do_post ， do_get 方法
    # 参数是 HttpRequest
    router = {
        root_url + '/assets': 'web.servlet.assets',
        root_url + '/assets_add': 'web.servlet.assets',
        root_url + '/assets_list': 'web.servlet.assets',
            }

# '/wtn/witness': 'web.witness',
#             '/wtn/assets_add': 'web.assets_add',
#             '/wtn/assets_list': 'web.assets_list',
#             '/wtn/my_assets_list': 'web.myassets_list',
#             "/wtn/my_assets_add": 'web.myassets_add',
#             '/wtn/assets': 'web.assets',
#             '/wtn/log_list': 'web.log_list',
#             '/wtn/note_list': 'web.note_list',
#             '/wtn/user_add': 'web.user_add',