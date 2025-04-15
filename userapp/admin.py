from django.contrib import admin

from kgapp.models import KgText2SQL
from userapp.models import User, Menu, Role

# Register your models here.
# Register your models here.
admin.site.site_header = '云河智能水利知识库系统'
admin.site.site_title = '云河智能水利知识库系统'


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
    list_display_links = ("id", "username", "password")
    search_fields = ("id", "username", "password")
    list_filter = ("id", "username", "password")


class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "menu_type")
    list_display_links = ("id", "name", "title", "menu_type")
    search_fields = ("id", "name", "title", "menu_type")
    list_filter = ("id", "name", "title", "menu_type")


class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "remark")
    list_display_links = ("id", "name", "remark")
    search_fields = ("id", "name", "remark")
    list_filter = ("id", "name", "remark")


admin.site.register(User, UserAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Role, RoleAdmin)
