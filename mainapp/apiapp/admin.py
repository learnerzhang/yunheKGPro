from django.contrib import admin

# Register your models here.
from apiapp.models import DDPlan, WaterRecord


class DDPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class WaterRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "dt")
    list_display_links = ("id", "name", "type", "dt")
    search_fields = ("id", "name", "type", "dt")
    list_filter = ("id", "name", "type", "dt")

admin.site.register(DDPlan, DDPlanAdmin)
admin.site.register(WaterRecord, WaterRecordAdmin)
