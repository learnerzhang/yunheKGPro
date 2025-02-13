# @Time    : 18-11-20
# @Author  : Zhiqi Kou
# @Email   : zhiqi1028@gmail.com

import xadmin
from xadmin import views
from .models import *
from django.utils.safestring import mark_safe
from yaapp.models import PlanByUser, PlanByUserDocument, PlanTemplate, TemplateNode, WordParagraph

# Register your models here.
class TemplateNodeAdmin(object):
    list_display = ("label", "description", "operation")
    search_fields = ("label", "description")
    list_filter = ("label", "description")
    model_icon = 'fa fa-bars'
    
    def operation(self, obj):
        del_str = '<a href="/xadmin/yaapp/templatenode/%s/delete/" class="btn btn-danger">删除</a>' % obj.pk
        return mark_safe(del_str)
    operation.short_description = '操作'

class WordParagraphAdmin(object):
    list_display = ("title", "ctype", "operation" )
    search_fields = ("title", "ctype", )
    list_filter = ("title", "ctype", )
    model_icon = 'fa fa-bars'
    
    def operation(self, obj):
        del_str = '<a href="/xadmin/yaapp/wordparagraph/%s/delete/" class="btn btn-danger">删除</a>' % obj.pk
        return mark_safe(del_str)

    operation.short_description = '操作'


class PlanTemplateAdmin(object):
    list_display = ("name","ctype", "operation")
    search_fields = ("ctype", "name")
    list_filter = ("ctype", "name")
    model_icon = 'fa fa-paper-plane'

    def operation(self, obj):
        del_str = '<a href="/xadmin/yaapp/plantemplate/%s/delete/" class="btn btn-danger">删除</a>' % obj.pk
        return mark_safe(del_str)
    operation.short_description = '操作'


class PlanByUserAdmin(object):
    list_display = ("name","ctype", "yadate", "operation")
    search_fields = ("ctype", "name")
    list_filter = ("ctype", "name")
    model_icon = 'fa fa-paper-plane'

    def operation(self, obj):
        del_str = '<a href="/xadmin/yaapp/planbyuser/%s/delete/" class="btn btn-danger">删除</a>' % obj.pk
        return mark_safe(del_str)
    operation.short_description = '操作'


class PlanByUserDocumentAdmin(object):
    list_display = ("name","document", "operation")
    search_fields = ("document", "name")
    list_filter = ("document", "name")
    model_icon = 'fa fa-paper-plane'

    def operation(self, obj):
        del_str = '<a href="/xadmin/yaapp/planbyuserdocument/%s/delete/" class="btn btn-danger">删除</a>' % obj.pk
        return mark_safe(del_str)
    operation.short_description = '操作'


class PTPtBusinessAdmin(object):
    list_display = ("name", "code")
    search_fields = ("name", )
    list_filter = ("name", )
    model_icon = 'fa fa-paper-plane'
    

xadmin.site.register(PlanTemplate, PlanTemplateAdmin)
xadmin.site.register(WordParagraph, WordParagraphAdmin)
xadmin.site.register(TemplateNode, TemplateNodeAdmin)
xadmin.site.register(PlanByUser, PlanByUserAdmin)
xadmin.site.register(PlanByUserDocument, PlanByUserDocumentAdmin)
xadmin.site.register(PtBusiness, PTPtBusinessAdmin)
