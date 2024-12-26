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
from . import views

urlpatterns = [
    path('kgmodel/', views.KgModelList.as_view()),
    path('kgmodel/add', views.ModelAddApiView.as_view()),
    path('kgmodel/update', views.ModelUpdateApiView.as_view()),
    path('kgmodel/delete', views.ModelDelApiView.as_view()),
    path('kgmodel/detail', views.ModelDetailApiView.as_view()),
    path('kgmodel/typelist', views.ModelTypeListApiView.as_view()),
    path('kgmodelparam/', views.KgModelParamList.as_view()),
    path('kgmodelparam/listbymodel', views.KgModelParamListByModel.as_view()),
    path('kgmodelparam/add', views.ModelParamAddApiView.as_view()),
    path('kgmodelparam/batchadd', views.ModelParamBatchAddApiView.as_view()),
    path('kgmodelparam/update', views.ModelParamUpdateApiView.as_view()),
    path('kgmodelparam/batchupdate', views.ModelParamBatchUpdateApiView.as_view()),
    path('kgmodelparam/delete', views.ModelParamDeleteApiView.as_view()),
    path('kgmodelparam/detail', views.ModelParamDetailApiView.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)