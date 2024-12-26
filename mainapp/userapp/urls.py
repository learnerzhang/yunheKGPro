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
    path('userapi/list', views.KgUserList.as_view()),
    path('userapi/detail', views.UserDetailApiView.as_view()),
    path('userapi/delete', views.UserDeleteApiView.as_view()),
    path('userapi/login', views.UserLoginApiView.as_view()),
    path('userapi/logout', views.UserLogoutApiView.as_view()),
    path('userapi/status', views.UserLoginStatusApiView.as_view()),
    path('userapi/regist', views.UserRegistApiView.as_view()),
    path('userapi/addorUpdate', views.UserAddorUpdateApiView.as_view()),
    path('userapp/roleList', views.RoleList.as_view()),
    path('userapp/roleDetail', views.RoleDetailApiView.as_view()),
    path('userapi/roleDelete', views.RoleDeleteApiView.as_view()),
    path('userapp/roleAddorUpdate', views.RoleAddorUpdateApiView.as_view()),
    path('userapi/menus', views.KgMenuList.as_view()),
    path('userapi/menusByUser', views.KgMenuByUserList.as_view()),
    path('userapi/menusaddByUser', views.KgMenuAddByUser.as_view()),
    path('userapi/menusdeleteByUser', views.KgMenuDeleteByUser.as_view()),
    path('userapi/menushiddenByUser', views.KgMenuHideByUser.as_view()),
    path('userapi/menusupdateByUser', views.KgMenuUpdateByUser.as_view()),
    path('userapi/menusetrieveByUser', views.KgMenuRetrieveByUser.as_view()),
    path('userapi/menuAddOrUpdate', views.MenuAddOrUpdateApiView.as_view()),
    path('userapi/menuDelete', views.MenuDeleteApiView.as_view()),
    path('userapi/menuDetail', views.MenuDetailApiView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)