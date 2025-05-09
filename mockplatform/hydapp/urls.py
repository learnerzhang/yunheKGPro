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
from hydapp import views

urlpatterns = [
    path('baseget', views.BaseApiGet.as_view()),
    path('basepost', views.BaseApiPost.as_view()),
    path('hdList', views.HDListApiGet.as_view()),
    path('skList', views.SKListApiGet.as_view()),
    path('futureHD', views.FutureHDApiGet.as_view()),
    path('futureSK', views.FutureSKApiGet.as_view()),
    path('realHD', views.RealHDApiGet.as_view()),
    path('realSK', views.RealSKApiGet.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)