# @Time    : 18-11-20
# @Author  : Zhiqi Kou
# @Email   : zhiqi1028@gmail.com

import xadmin
from xadmin import views
from .models import *


xadmin.site.site_header = '云河智能水利知识库系统'
xadmin.site.site_title = '云河智能水利知识库系统'


class MenuAdmin(object):
    list_display = ("id", "name", "title", "menu_type")
    list_display_links = ("id", "name", "title", "menu_type")
    search_fields = ("id", "name", "title", "menu_type")
    list_filter = ("id", "name", "title", "menu_type")
    model_icon = 'fa fa-bars'


class RoleAdmin(object):
    list_display = ("id", "name", "remark")
    list_display_links = ("id", "name", "remark")
    search_fields = ("id", "name", "remark")
    list_filter = ("id", "name", "remark")
    model_icon = 'fa fa-bars'

xadmin.site.register(Menu, MenuAdmin)
xadmin.site.register(Role, RoleAdmin)


from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


from xadmin import views

class GlobalSettings(object):
    site_title = "水利知识库管理平台"
    site_footer = '知识库研发组'
    menu_style = "accordion"  #选项卡折叠效果

xadmin.site.register(views.CommAdminView, GlobalSettings)

