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
from . import knowledge_views

urlpatterns = [
    path('api/outline', views.OutlineApiView.as_view()),
    path('api/onlineqa', views.OlineQAApiView.as_view()),
    path('api/abstract', views.OlineAbstractApiView.as_view()),
    path('api/text2sql', views.OlineText2SQLApiView.as_view()),
    path('api/text_extends', views.TextExtentApiView.as_view()),
    path('api/graphquery', views.GraphQueryApiView.as_view()),
    path("knowledge/upload", knowledge_views.KnowledgeUploadApiView.as_view()),
    path('knowledge/train', knowledge_views.KnowledgeTrainTaskApiView.as_view()),
    path('knowledge/parse', knowledge_views.KnowledgeDocParseTaskApiView.as_view()),
    path('knowledge/batchparse', knowledge_views.KnowledgeDocBatchParseTaskApiView.as_view()),
    path('knowledge/add', knowledge_views.KnowledgeAddApiView.as_view()),
    path('knowledge/del', knowledge_views.KnowledgeDeleteApiView.as_view()),
    path('knowledge/list', knowledge_views.KnowledgeListApiView.as_view()),
    path('knowledge/retrieval', knowledge_views.KnowledgeRetrieval.as_view()),
]
