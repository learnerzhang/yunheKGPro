from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('datamodellist/', views.DataModelListAPIView.as_view(), name='data-model-list'),
    path('datamodeldelete/', views.DataModelDeleteAPIView.as_view(), name='data-model-delete'),
    path('datamodelsearchoradd/', views.DataModelAPIView.as_view(), name='datamodel-searchoradd'),  # 用于获取和创建数据模型
    path('datamodelupdate/', views.DataModelUpdateAPIView.as_view(), name='datamodel-update'),  # 用于获取和创建数据模型
    path('datamodelretrive/', views.DataModelRetrieveAPIView.as_view(), name='datamodel-retrive'),  #
    path('datamodelsearch/', views.DataModelSearchAPIView.as_view(), name='datamodel-search'),
    path('datamodeltest/', views.DataModelTestAPIView.as_view(), name='datamodel-test'),  #
]