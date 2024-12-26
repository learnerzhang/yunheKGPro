from django.contrib import admin

from userapp.models import User

admin.site.site_header = '云河Mock系统'
admin.site.site_title = '云河Mock系统'

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
    list_display_links = ("id", "username", "password")
    search_fields = ("id", "username", "password")
    list_filter = ("id", "username", "password")

admin.site.register(User, UserAdmin)