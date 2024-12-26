from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'logs/(?P<log_type>login|operation)', views.LogViewSet, basename='log')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('logs/<str:log_type>/', views.LogViewSet.as_view({'get': 'list'})),  
    path('logs/<str:log_type>/<int:pk>/', views.LogViewSet.as_view({'get': 'retrieve'})), 
]