from drf_yasg import openapi  
from .models import LoginLog, OperationLog
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, pagination
from .logSerializer import LoginLogSerializer, OperationLogSerializer

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10  # 每页显示多少条数据
    page_size_query_param = 'page_size'
    max_page_size = 100  # 最大页数

class LogViewSet(viewsets.ReadOnlyModelViewSet):
  
    def get_queryset(self):
        log_type = self.kwargs.get('log_type')  # 获取日志类型
        if log_type == 'login':
            return LoginLog.objects.all()
        elif log_type == 'operation':
            return OperationLog.objects.all()
        else:
            return None  # 如果类型不匹配，则返回 None

    def get_serializer_class(self):
        log_type = self.kwargs.get('log_type')
        if log_type == 'login':
            return LoginLogSerializer
        elif log_type == 'operation':
            return OperationLogSerializer
        return None  # 如果类型不匹配，则返回 None
    
    @swagger_auto_schema(  
        operation_summary='获取日志列表',  
        operation_description='根据日志类型获取相应的日志列表。',  
        manual_parameters=[  
            openapi.Parameter('log_type', openapi.IN_PATH, description="日志类型（登录日志:login 或 操作日志:operation）", type=openapi.TYPE_STRING),  
            openapi.Parameter('fields', openapi.IN_QUERY, description="指定返回字段，以逗号分隔", type=openapi.TYPE_STRING)  
        ],  
        responses={200: openapi.Response('成功返回日志列表')}  
    ) 

    def list(self, request, *args, **kwargs):
        fields = request.query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
        else:
            fields = [field.name for field in self.get_serializer_class().Meta.model._meta.get_fields()]

        queryset = self.filter_queryset(self.get_queryset())
        
        serializer = self.get_serializer(queryset, many=True)
        data = []
        
        for item in serializer.data:
            filtered_item = {field: item[field] for field in fields if field in item}
            data.append(filtered_item)

        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(data)
