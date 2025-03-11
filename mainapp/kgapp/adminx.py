from django.contrib import admin
from kgapp.models import KgDDRule, KgDDRuleAttribute, KgRelationScheme, KgEntityScheme, KgEntity, KgRelation, \
    KgEntityAtt, KgEntityAttrScheme, KgDataIndex, KgText2SQL
from kgapp.models import KgDoc, KgQA, KgTableContent, KgTag, KgBusiness, KgTemplates, KgProductTask, KgTask, KgTmpQA, \
    KgUpLoadTemplate

import xadmin
from xadmin import views
from .models import *

# Register your models here.
class ModelDoc(object):
    list_display = ("id", "title", "path")
    list_display_links = ("id", "title", "path")
    search_fields = ("id", "title", "path")
    list_filter = ("id", "title", "path")
    model_icon = 'fa fa-file'


class ModelTableContent(object):
    list_display = ("id", "name", "no")
    list_display_links = ("id", "name", "no")
    search_fields = ("id", "name", "no")
    list_filter = ("id", "name", "no")
    model_icon = 'fa fa-bars'

class ModelTag(object):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-tags'


class ModelDocTag(object):
    list_display = ("id", "kg_tag_id", "kg_doc_id")
    list_display_links = ("id", "kg_tag_id", "kg_doc_id")
    search_fields = ("id", "kg_tag_id", "kg_doc_id")
    list_filter = ("id", "kg_tag_id", "kg_doc_id")
    model_icon = 'fa fa-bars'

class ModelBusiness(object):
    list_display = ("id", "name", "kg_user_id")
    list_display_links = ("id", "name", "kg_user_id")
    search_fields = ("id", "name", "kg_user_id")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class ModelTemplate(object):
    list_display = ("id", "name", "kg_business_id", "kg_user_id")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class ProdTaskTemplate(object):
    list_display = ("id", "name", "desc", "task_type", "task_status")
    list_display_links = ("id", "name", "desc", "task_type", "task_status")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class TaskTemplate(object):
    list_display = ("id", "kg_prod_task_id", "celery_id", "task_step")
    list_display_links = ("id", "kg_prod_task_id", "celery_id", "task_step")
    search_fields = ("id", "kg_prod_task_id")
    list_filter = ("id", "kg_prod_task_id")
    model_icon = 'fa fa-bars'

class KgQATemplate(object):
    list_display = ("id", "question", "answer")
    list_display_links = ("id", "question")
    search_fields = ("id", "question")
    list_filter = ("id", "question")
    model_icon = 'fa fa-bars'

class KgTemplate(object):
    list_display = ("id", "title", "title")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")
    list_filter = ("id", "title")
    model_icon = 'fa fa-bars'

class KgEntityAttrSchemeTemplate(object):
    list_display = ("id", "attname", "atttype")
    list_display_links = ("id", "attname", "atttype")
    search_fields = ("id", "attname", "atttype")
    list_filter = ("id", "attname", "atttype")
    model_icon = 'fa fa-bars'

class KgEntitySchemeTemplate(object):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class KgRelationSchemeTemplate(object):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class KgEntityTemplate(object):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class KgEntityAttTemplate(object):
    list_display = ("id", "attname", "atttvalue")
    list_display_links = ("id", "attname", "atttvalue")
    search_fields = ("id", "attname", "atttvalue")
    list_filter = ("id", "attname", "atttvalue")
    model_icon = 'fa fa-bars'

class KgRelationTemplate(object):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

# class KgDDActionSchemeTemplate(object):
#     list_display = ("id", "name")
#     list_display_links = ("id", "name")
#     search_fields = ("id", "name")
#     list_filter = ("id", "name")

class KgDDAttrSchemeTemplate(object):
    list_display = ("id", "name", "type")
    list_display_links = ("id", "name", "type")
    search_fields = ("id", "name", "type")
    list_filter = ("id", "name", "type")
    model_icon = 'fa fa-bars'

class KgDDRuleSchemeTemplate(object):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("id", "name")
    model_icon = 'fa fa-bars'

class KgDataIndexTemplate(object):
    list_display = ("id", "span_type")
    list_display_links = ("id", "span_type")
    search_fields = ("id", "span_type")
    list_filter = ("id", "span_type")
    model_icon = 'fa fa-bars'

class TsqkAdmin(object):
    list_display = ("id", "query", "sql_ctt", "activate")
    list_display_links = ("id", "query", "sql_ctt", "activate")
    search_fields = ("id", "query", "sql_ctt", "activate")
    list_filter = ("id", "query", "sql_ctt", "activate")
    model_icon = 'fa fa-bars'

class BusinessAdmin(object):
    list_display = ("id", "name", "code")
    list_display_links = ("id", "name", "code")
    search_fields = ("id", "name", "code")
    list_filter = ("id", "name", "code")
    model_icon = 'fa fa-bars'

class QuestionCategoryAdmin(object):
    list_display = ("id", "name", "desc")
    list_display_links = ("id", "name", "desc")
    search_fields = ("id", "name", "desc")
    list_filter = ("id", "name", "desc")
    model_icon = 'fa fa-bars'

class DisplayQuestionAdmin(object):
    list_display = ("id", "question", "category", "business")
    list_display_links = ("id", "question", "category", "business")
    search_fields = ("id", "question", "category", "business")
    list_filter = ("id", "question", "category", "business")
    model_icon = 'fa fa-bars'


xadmin.site.register(KgDoc, ModelDoc)
xadmin.site.register(KgTableContent, ModelTableContent)
xadmin.site.register(KgTag, ModelTag)
xadmin.site.register(KgBusiness, ModelBusiness)
xadmin.site.register(KgTemplates, ModelTemplate)

xadmin.site.register(KgProductTask, ProdTaskTemplate)
xadmin.site.register(KgTask, TaskTemplate)
xadmin.site.register(KgQA, KgQATemplate)

xadmin.site.register(KgUpLoadTemplate, KgTemplate)
xadmin.site.register(KgRelationScheme, KgRelationSchemeTemplate)
xadmin.site.register(KgEntityAttrScheme, KgEntityAttrSchemeTemplate)
xadmin.site.register(KgEntityScheme, KgEntitySchemeTemplate)

xadmin.site.register(KgRelation, KgRelationTemplate)
xadmin.site.register(KgEntity, KgEntityTemplate)
xadmin.site.register(KgEntityAtt, KgEntityAttTemplate)

# xadmin.site.register(KgDDAction, KgDDActionSchemeTemplate)
xadmin.site.register(KgDDRuleAttribute, KgDDAttrSchemeTemplate)
xadmin.site.register(KgDDRule, KgDDRuleSchemeTemplate)
xadmin.site.register(KgDataIndex, KgDataIndexTemplate)
xadmin.site.register(KgText2SQL, TsqkAdmin)


xadmin.site.register(Business, BusinessAdmin)
xadmin.site.register(QuestionCategory, QuestionCategoryAdmin)
xadmin.site.register(DisplayQuestion, DisplayQuestionAdmin)


class KgKnowledgeAdmin(object):
    list_display = ("id", "hashid", "name")
    list_display_links = ("id", "hashid", "name")
    search_fields = ("id", "hashid", "name")
    list_filter = ("id", "hashid", "name")
    model_icon = 'fa fa-square'

class KgFragTagAdmin(object):
    list_display = ("id", "name", "weight")
    list_display_links = ("id", "name", "weight")
    search_fields = ("id", "name", "weight")
    model_icon = 'fa fa-tags'


class KgDocFragmentationAdmin(object):
    list_display = ("id", "content", "kg_knowledge_id", "recall_cnt")
    list_display_links = ("id", "content", "kg_knowledge_id", "recall_cnt")
    search_fields = ("id", "content", "kg_knowledge_id", "recall_cnt")
    list_filter = ("id", "content", "kg_knowledge_id", "recall_cnt")
    model_icon = 'fa fa-file-text-o'

xadmin.site.register(Knowledge, KgKnowledgeAdmin)
xadmin.site.register(KgDocCttTag, KgFragTagAdmin)
xadmin.site.register(KgDocFragmentation, KgDocFragmentationAdmin)
