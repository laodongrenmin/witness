# -*- coding: utf-8 -*-

# 访问的根，必须配置
g_root_url = '/wtn'

# 路由，请求Url和处理模块的对应关系
# 模块需要实现 do_post ， do_get 方法
# 参数是 HttpRequest
g_router = {'/wtn/witness': 'web.witness',
            '/wtn/assets_add': 'web.assets_add',
            '/wtn/assets_list': 'web.assets_list',
            '/wtn/my_assets_list': 'web.myassets_list',
            "/wtn/my_assets_add": 'web.myassets_add',
            '/wtn/assets': 'web.assets',
            '/wtn/log_list': 'web.log_list',
            '/wtn/note_list': 'web.note_list',
            '/wtn/user_add': 'web.user_add',
            }




