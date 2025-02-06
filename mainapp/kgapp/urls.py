"""GeographicKG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from kgapp import drule_views
from . import views
from . import bus_views
from . import task_views
from . import man_views
from . import graph_views


urlpatterns = [
    path('text2sqllist', views.KgText2SqlList.as_view()),
    path('recomqalist', views.RecomQAList.as_view()),
    path('kgdoc/list', views.KgDocList.as_view()),
    path('kgdoc/search', views.KgDocSearch.as_view()),
    path('dataIndex', views.KgDataIndexApiView.as_view()),
    path('kgdoc/listByCtt', views.KgDocByCttList.as_view()),
    path('kgdoc/allDocIds', views.DocAllIdListApiView.as_view()),
    path('kgdoc/add', views.DocAddApiView.as_view()),
    path('kgdoc/batchadd', views.DocBatchAddApiView.as_view()),
    path('kgdoc/addtag', views.DocAddTagApiView.as_view()),
    path('kgdoc/update', views.DocUpdateApiView.as_view()),
    path('kgdoc/batchdelprodflag', views.DocBatchUpdateApiView.as_view()),
    path('kgdoc/delete', views.DocDelApiView.as_view()),
    path('kgdoc/detail', views.DocDetailApiView.as_view()),
    path('kgtabtag/list', views.KgTabTagList.as_view()),
    path('kgtabtag/listByTab', views.KgTagByTabList.as_view()),
    path('kgtabtag/add', views.TabTagAddApiView.as_view()),
    path('kgtabtag/update', views.TabTagUpdateApiView.as_view()),
    path('kgtabtag/batchaddtags', views.TabTagAddTagApiView.as_view()),
    path('kgtabtag/delete', views.TabTagDelApiView.as_view()),
    path('kgtag/list', views.KgTagList.as_view()),
    path('kgtag/add', views.TagAddApiView.as_view()),
    path('kgtag/update', views.TagUpdateApiView.as_view()),
    path('kgtag/delete', views.TagDelApiView.as_view()),
    path('kgtag/detail', views.TagDetailApiView.as_view()),
    path('kgctt/list', views.KgTabCTTList.as_view()),
    path('kgctt/add', views.KgTabCTTAddAPIList.as_view()),
    path('kgctt/delete', views.KgTabCTTDelAPIList.as_view()),
    path('kgctt/update', views.KgTabCTTUpdateAPIList.as_view()),
    path('kgtbus/list', bus_views.KgBusList.as_view()),
    path('kgtbus/add', bus_views.BusAddApiView.as_view()),
    path('kgtbus/update', bus_views.BusUpdateApiView.as_view()),
    path('kgtbus/delete', bus_views.BusDelApiView.as_view()),
    path('kgtemp/list', bus_views.KgTempList.as_view()),
    path('kgtemp/add', bus_views.KgTempAddApiView.as_view()),
    path('kgtemp/update', bus_views.KgTempUpdateApiView.as_view()),
    path('kgtemp/delete', bus_views.KgTempDelApiView.as_view()),
    path('kgtemp/detail', bus_views.KgTempDetailApiView.as_view()),
    path('kgtempctt/list', bus_views.KgTabCTTList.as_view()),
    path('kgtempctt/add', bus_views.KgTabCTTAddAPIList.as_view()),
    path('kgtempctt/delete', bus_views.KgTabCTTDelAPIList.as_view()),
    path('kgtempctt/update', bus_views.KgTabCTTUpdateAPIList.as_view()),
    path('kgtemp/listByCtt', bus_views.KgTempByCttList.as_view()),
    path('task/list', task_views.KgProdTaskList.as_view()),
    path('task/listDocByTask', task_views.KglistDocByTask.as_view()),
    path('task/template', task_views.KgTemplate.as_view()),
    path('task/detail', task_views.ProdTaskDetailApiView.as_view()),
    path('task/add', task_views.ProdTaskAddApiView.as_view()),
    path('task/update', task_views.ProdTaskUpdateApiView.as_view()),
    path('task/delete', task_views.ProdTaskDelApiView.as_view()),
    path('task/status', task_views.TaskStatusApiView.as_view()),
    path('task/load', task_views.TaskLoadApiView.as_view()),
    path('task/product', task_views.TaskProductApiView.as_view()),
    path('task/kgloaddone', task_views.TaskLoadDoneApiView.as_view()),
    path('task/kgimportgraphdone', task_views.TaskImportGraphDoneApiView.as_view()),
    path('task/kgfulldone', task_views.TaskFullDoneApiView.as_view()),
    path('task/demo', task_views.TaskApiView.as_view()),
    path('task/demotest', task_views.TaskApiTestView.as_view()),
    path('tmpqa/list', task_views.KgTmpQAList.as_view()),
    path('tmpsimqa/list', task_views.KgTmpSimQAList.as_view()),
    path('tmpgraph/list', task_views.KgTmpGraphList.as_view()),
    path('tmpsimgraph/list', task_views.KgTmpSimGraphList.as_view()),
    path('tmpfullprod/list', task_views.kgFullProdList.as_view()),
    path('prodqalist/list', man_views.KgQAList.as_view()),
    path('prodqalist/update', man_views.KgQAUpdateApiView.as_view()),
    path('prodqalist/synToLLM', man_views.KgQASynToLLMApiView.as_view()),
    path('prodqalist/delete', man_views.KgQADelApiView.as_view()),
    path('prodqalist/batchdelete', man_views.KgQABatchDelApiView.as_view()),
    path('graphEntityScheme/list', graph_views.KgEntitySchemeList.as_view()),
    path('graphEntityScheme/add', graph_views.KgEntitySchemeAddApiView.as_view()),
    path('graphEntityScheme/detail', graph_views.KgEntitySchemeDetailApiView.as_view()),
    path('graphEntityScheme/update', graph_views.KgEntitySchemeUpdateApiView.as_view()),
    path('graphEntityScheme/delete', graph_views.KgEntitySchemeDeleteApiView.as_view()),
    path('graphEntityScheme/addattr', graph_views.KgEntitySchemeAddAttrApiView.as_view()),
    path('graphEntityScheme/updateattr', graph_views.KgEntitySchemeUpdateAttrApiView.as_view()),
    path('graphEntityScheme/deleteattr', graph_views.KgEntitySchemeDelAttrApiView.as_view()),
    path('graphRelationScheme/list', graph_views.KgRelationSchemeList.as_view()),
    path('graphRelationScheme/add', graph_views.KgRelationSchemeAddApiView.as_view()),
    path('graphRelationScheme/update', graph_views.KgRelationSchemeUpdateApiView.as_view()),
    path('graphRelationScheme/delete', graph_views.KgRelationSchemeDeleteApiView.as_view()),
    path('graphRelationScheme/detail', graph_views.KgRelationSchemeDetailApiView.as_view()),
    path('graphEntityByTypeList/', graph_views.KgEntityByTypeList.as_view()),
    path('graphEntity/detail', graph_views.KgEntityDetailApiView.as_view()),
    path('graphEntity/delete', graph_views.KgEntityDeleteApiView.as_view()),
    path('graphEntity/update', graph_views.KgEntityUpdateAttrApiView.as_view()),
    path('graphEntity/detailByNameType', graph_views.KgEntityDetailByNameTypeApiView.as_view()),
    path('graph', graph_views.KgEntityApiView.as_view()),
    path('clearGraph', graph_views.KgClearGraphApiView.as_view()),
    path('graphExpand', graph_views.KgEntityExpandApiView.as_view()),
    # path('ddrule/actionlist/', drule_views.KgDDActionList.as_view()),
    # path('ddrule/actionadd', drule_views.KgDDActionSaveApiView.as_view()),
    # path('ddrule/actiondel', drule_views.KgDDActionDelApiView.as_view()),
    path('ddrule/attrlist', drule_views.KgDDRuleAttributeList.as_view()),
    path('ddrule/attradd', drule_views.KgDDRuleAttributeSaveApiView.as_view()),
    path('ddrule/attrdel', drule_views.KgDDRuleAttributeDelApiView.as_view()),
    path('ddrule/rulelist', drule_views.KgDDRuleList.as_view()),
    path('ddrule/ruleadd', drule_views.KgDDRuleSaveApiView.as_view()),
    path('ddrule/ruleenable', drule_views.KgDDRuleEnableApiView.as_view()),
    path('ddrule/ruledetail', drule_views.KgDDRuleDetailApiView.as_view()),
    path('ddrule/ruledel', drule_views.KgDDRuleDelApiView.as_view()),
    path('ddrule/ruleresult', drule_views.KgDDRuleResultApiView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)