from django.contrib import admin
from modelapp.models import KgModel, KgModelParam
# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "version")
    list_display_links = ("id", "name", "version")
    search_fields = ("id", "name", "version")
    list_filter = ("id", "name", "version")


class ModelParamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    list_display_links = ("id", "name", "type")
    search_fields = ("id", "name", "type")
    list_filter = ("id", "name", "type")


admin.site.register(KgModel, ModelAdmin)
admin.site.register(KgModelParam, ModelParamAdmin)
