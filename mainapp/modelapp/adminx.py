# @Time    : 18-11-20
# @Author  : Zhiqi Kou
# @Email   : zhiqi1028@gmail.com

import xadmin
from xadmin import views
from .models import *


# Register your models here.

class KgModelAdmin(object):
    list_display = ("name", "function", "desc")
    search_fields = ("name", "function", "desc")
    list_filter = ("name", "function", "desc")
    model_icon = 'fa fa-hashtag'

class KgModelParamAdmin(object):
    list_display = ("name", "type", "desc")
    search_fields = ("name", "type", "desc")
    list_filter = ("name", "type", "desc")
    model_icon = 'fa fa-bars'

xadmin.site.register(KgModel, KgModelAdmin)
xadmin.site.register(KgModelParam, KgModelParamAdmin)
