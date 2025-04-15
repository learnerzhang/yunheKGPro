from django.contrib import admin
from kgapp.models import KgDDRule, KgDDRuleAttribute, KgRelationScheme, KgEntityScheme, KgEntity, KgRelation, \
    KgEntityAtt, KgEntityAttrScheme, KgDataIndex, KgText2SQL
from kgapp.models import KgDoc, KgQA, KgTableContent, KgTag, KgBusiness, KgTemplates, KgProductTask, KgTask, KgTmpQA, \
    KgUpLoadTemplate


# Register your models here.
class ModelDoc(admin.ModelAdmin):
    list_display = ("id", "title", "path")
    list_display_links = ("id", "title", "path")
    search_fields = ("id", "title", "path")
    list_filter = ("id", "title", "path")


class ModelTableContent(admin.ModelAdmin):
    list_display = ("id", "name", "no")
    list_display_links = ("id", "name", "no")
    search_fields = ("id", "name", "no")
    list_filter = ("id", "name", "no")


class ModelTag(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class ModelDocTag(admin.ModelAdmin):
    list_display = ("id", "kg_tag_id", "kg_doc_id")
    list_display_links = ("id", "kg_tag_id", "kg_doc_id")
    search_fields = ("id", "kg_tag_id", "kg_doc_id")
    list_filter = ("id", "kg_tag_id", "kg_doc_id")


class ModelBusiness(admin.ModelAdmin):
    list_display = ("id", "name", "kg_user_id")
    list_display_links = ("id", "name", "kg_user_id")
    search_fields = ("id", "name", "kg_user_id")
    list_filter = ("id", "name")


class ModelTemplate(admin.ModelAdmin):
    list_display = ("id", "name", "kg_business_id", "kg_user_id")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class ProdTaskTemplate(admin.ModelAdmin):
    list_display = ("id", "name", "desc", "task_type", "task_status")
    list_display_links = ("id", "name", "desc", "task_type", "task_status")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class TaskTemplate(admin.ModelAdmin):
    list_display = ("id", "kg_prod_task_id", "celery_id", "task_step")
    list_display_links = ("id", "kg_prod_task_id", "celery_id", "task_step")
    search_fields = ("id", "kg_prod_task_id")
    list_filter = ("id", "kg_prod_task_id")


class KgQATemplate(admin.ModelAdmin):
    list_display = ("id", "question", "answer")
    list_display_links = ("id", "question")
    search_fields = ("id", "question")
    list_filter = ("id", "question")


class KgTemplate(admin.ModelAdmin):
    list_display = ("id", "title", "title")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")
    list_filter = ("id", "title")


class KgEntityAttrSchemeTemplate(admin.ModelAdmin):
    list_display = ("id", "attname", "atttype")
    list_display_links = ("id", "attname", "atttype")
    search_fields = ("id", "attname", "atttype")
    list_filter = ("id", "attname", "atttype")


class KgEntitySchemeTemplate(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class KgRelationSchemeTemplate(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class KgEntityTemplate(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class KgEntityAttTemplate(admin.ModelAdmin):
    list_display = ("id", "attname", "atttvalue")
    list_display_links = ("id", "attname", "atttvalue")
    search_fields = ("id", "attname", "atttvalue")
    list_filter = ("id", "attname", "atttvalue")


class KgRelationTemplate(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


# class KgDDActionSchemeTemplate(admin.ModelAdmin):
#     list_display = ("id", "name")
#     list_display_links = ("id", "name")
#     search_fields = ("id", "name")
#     list_filter = ("id", "name")

class KgDDAttrSchemeTemplate(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    list_display_links = ("id", "name", "type")
    search_fields = ("id", "name", "type")
    list_filter = ("id", "name", "type")


class KgDDRuleSchemeTemplate(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")


class KgDataIndexTemplate(admin.ModelAdmin):
    list_display = ("id", "span_type")
    list_display_links = ("id", "span_type")
    search_fields = ("id", "span_type")
    list_filter = ("id", "span_type")


class TsqkAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "sql_ctt", "activate")
    list_display_links = ("id", "query", "sql_ctt", "activate")
    search_fields = ("id", "query", "sql_ctt", "activate")
    list_filter = ("id", "query", "sql_ctt", "activate")


admin.site.register(KgText2SQL, TsqkAdmin)

admin.site.register(KgDoc, ModelDoc)
admin.site.register(KgTableContent, ModelTableContent)
admin.site.register(KgTag, ModelTag)
admin.site.register(KgBusiness, ModelBusiness)
admin.site.register(KgTemplates, ModelTemplate)

admin.site.register(KgProductTask, ProdTaskTemplate)
admin.site.register(KgTask, TaskTemplate)
admin.site.register(KgQA, KgQATemplate)

admin.site.register(KgUpLoadTemplate, KgTemplate)
admin.site.register(KgRelationScheme, KgRelationSchemeTemplate)
admin.site.register(KgEntityAttrScheme, KgEntityAttrSchemeTemplate)
admin.site.register(KgEntityScheme, KgEntitySchemeTemplate)

admin.site.register(KgRelation, KgRelationTemplate)
admin.site.register(KgEntity, KgEntityTemplate)
admin.site.register(KgEntityAtt, KgEntityAttTemplate)

# admin.site.register(KgDDAction, KgDDActionSchemeTemplate)
admin.site.register(KgDDRuleAttribute, KgDDAttrSchemeTemplate)
admin.site.register(KgDDRule, KgDDRuleSchemeTemplate)

admin.site.register(KgDataIndex, KgDataIndexTemplate)
