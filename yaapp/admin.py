from django.contrib import admin

from yaapp.models import PlanByUser, PlanByUserDocument, PlanTemplate, PtBusiness, TemplateNode, WordParagraph

# Register your models here.
class TemplateNodeAdmin(admin.ModelAdmin):
    list_display = ("label", "description")
    search_fields = ("label", "description")
    list_filter = ("label", "description")


class WordParagraphAdmin(admin.ModelAdmin):
    list_display = ("title", "ctype", )
    search_fields = ("title", "ctype", )
    list_filter = ("title", "ctype", )


class PlanTemplateAdmin(admin.ModelAdmin):
    list_display = ("name","ctype")
    search_fields = ("ctype", "name")
    list_filter = ("ctype", "name")

admin.site.register(PlanTemplate, PlanTemplateAdmin)
admin.site.register(WordParagraph, WordParagraphAdmin)
admin.site.register(TemplateNode, TemplateNodeAdmin)
admin.site.register(PlanByUser)
admin.site.register(PlanByUserDocument)
admin.site.register(PtBusiness)