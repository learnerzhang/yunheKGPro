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
from . import views

urlpatterns = [
    path('templateList', views.TemplateList.as_view()),
    path('businesslist', views.PTBusinessList.as_view()),
    path('blockList', views.BlockList.as_view()),
    path('blockOptList', views.BlockOptionList.as_view()),
    path('sysTemplateDetail', views.TemplateDetail.as_view()),
    path('addOrUpdateSysTemplate', views.AddOrUpdateTemplate.as_view()),
    path('deleteSysTemplate', views.DeleteTemplate.as_view()),
    path('addOrUpdateSysTemplateByNode', views.AddOrUpdateTemplateByNode.as_view()),
    path('createSysTemplate', views.CreateSysTemplate.as_view()),
    path('updateSysTemplateNode', views.UpdateTemplateNode.as_view()),
    path('deleteNodeBySysTemplate', views.DeleteNodeByTemplate.as_view()),
    path('llmYuANSingleNodeUserPlan', views.LLMSingleNodePlan.as_view()),
    path('ragYuANSingleNodeUserPlan', views.RagSingleNodePlan.as_view()),
    path('llmYuANUserPlan', views.LLMNodePlan.as_view()),
    path('makeUserYuAnWord', views.MakePlanWord.as_view()),
    path('userPlanDocumentList', views.UserTemplateDocumentList.as_view()),
    path('deleteUserPlanDocument', views.DeleteUserPlanDocument.as_view()),
    path('updateUserPlanDocument', views.UpdateUserPlanDocument.as_view()),
    path('yuAnUserRecom', views.YuAnRecomApiPost.as_view()),
    path('yuAnRecomPtDetail', views.YuAnRecomPtDetailApiGet.as_view()),
    path('yuAnUserPtSave', views.YuAnUserPtSaveApiPost.as_view()),
    path('yuAnUserPtDelete', views.YuAnUserPtDeleteApiPost.as_view()),
    path('yuAnUserPtNodeAddOrUpdate', views.YuAnUserPtNodeAddOrUpdateApiPost.as_view()),
    path('yuAnUserPtDetail', views.YuAnUserPtDetailApiGet.as_view()),
    path('yuAnUserPlanDelete', views.YuAnUserPlanDeleteApiPost.as_view()),
    path('yuAnUserPlanList', views.YuAnUserPtListApiGet.as_view()),
    path('recentlyYuAnUserPt', views.RecentlyYuAnUserPtApiGet.as_view()),
    path('ddfaUpload', views.DDFAUploadApiPost.as_view()),
    path('downloadPlan', views.downloadPlan, name="downloadPlan"),
    path('llmYuAnTask', views.LLMYuAnTaskApiView.as_view(), name="llmYuAnTask"),
    path('llmYuAnTaskStatus', views.LLMYuAnTaskStatusApiView.as_view(), name="llmYuAnTaskStatus"),
    path('resultFromTask', views.ResultFromTaskApiView.as_view(), name="resultFromTask"),
]
