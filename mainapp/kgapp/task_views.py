import time
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
from kgapp.serializers import *
from kgapp.models import *
from django.http import HttpResponse
# from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from rest_framework.authentication import BasicAuthentication
from django.http import StreamingHttpResponse
import os
import collections
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from modelapp.models import KgModel
from yunheKGPro import CsrfExemptSessionAuthentication
# Create your views here.
from yunheKGPro.neo import Neo4j


class KgTmpQAList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgTmpQAResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/tmpqa/',
            operation_summary="获取临时QA解析列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="任务ID"),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgTmpQAResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        taskId = request.GET.get("taskId", None)
        if taskId is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgTmpQAResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        try:
            tmptask = KgProductTask.objects.get(id=taskId)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        # querySet = KgTmpQA.objects.filter(task_id=taskId, doc_id=docId).all().order_by('-update_time')
        

        datatask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).first()
        from celery.result import AsyncResult
        import pprint
        res = AsyncResult(datatask.celery_id) # 参数为task id
        if not res:
            data = {"code": 201, "msg": "任务ID结果不存在" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if 'data' not in  res.result:
            data = {"code": 202, "msg": "暂无生产结果" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        querySet = res.result['data']
        data['total'] = len(querySet)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize) 
        try:
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        kds = KgTmpQASerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgTmpQAResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgTmpSimQAList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgTmpQAResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/tmpsimqa/',
            operation_summary="获取临时QA解析相似列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="任务ID"),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgTmpQAResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        taskId = request.GET.get("taskId", None)
        try:
            tmptask = KgProductTask.objects.get(id=taskId)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        simtask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=1).first()
        from celery.result import AsyncResult
        res = AsyncResult(simtask.celery_id) # 参数为task id
        if not res:
            data = {"code": 20, "msg": "任务ID结果不存在" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        page = int(request.GET.get("page", 1))
        pageSize = int(request.GET.get("pageSize", 10))
        querySet = [ent for ent in res.result['data'] if ent['simqas']]
        print(res.result['data'])
        data['total'] = len(querySet)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize) 
        try:
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        kds = KgTmpQASerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        
        serializers = KgTmpQAResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgProdTaskList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgTaskResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/',
            operation_summary="获取任务列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('taskType', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="生产类型 0(知识导入)|1(自动生成)|2(全文生产)|2(图谱生产)"),
                openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgTaskResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        taskTypeStr = request.GET.get("taskType", "0")
        taskTypes = str(taskTypeStr).split(",")
        tkstatus = request.GET.get("status", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        querySet = KgProductTask.objects

        if taskTypes:
            querySet = querySet.filter(task_type__in=taskTypes)

        if tkstatus:
            querySet = querySet.filter(task_status=tkstatus)

        querySet = querySet.all().order_by('-update_time')
        data['total'] = len(querySet)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize) 
        try:
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        kds = KgTaskSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgTaskResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KglistDocByTask(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /task/listDocByTask',
            operation_summary="获取任务文档列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    #参数名称
                    "keyword", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="关键词模糊搜索", 
                    # 参数字符类型
                    type=openapi.TYPE_STRING
                ),
                # 声明参数
                openapi.Parameter(
                    #参数名称
                    "taskid", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="任务ID", 
                    # 参数字符类型
                    type=openapi.TYPE_INTEGER
                ),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgDocResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        taskid = request.GET.get("taskid", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        try:
            tmptask = KgProductTask.objects.get(id=taskid)
        except:
            data = {"code": 20, "msg": "任务ID结果不存在" }
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if tmptask:
            querySet = tmptask.kg_doc_ids.all()
            if keyword:
                querySet = [doc for doc in querySet if '{}'.format(keyword) in doc.title]

        data['total'] = len(querySet)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize) 
        try:
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        kds = KgDocSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)

def read_file(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

class KgTemplate(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgTaskResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /task/template/',
            operation_summary="获取模板",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="问答对|其他"),
            ],
            responses={
                200: KgTaskTemplateResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        type_str = request.GET.get("type", None)
        try:
            tmp = KgUpLoadTemplate.objects.filter(title__contains=type_str).first()
            data = {"code": 200, "msg": "" }
            data['data'] = model_to_dict(tmp, exclude=['path'])
            data['data']['filepath'] = tmp.filepath
            serializers = KgTaskTemplateResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        except:
            data = {"code": 201, "msg": "模板不存在" }
            serializers = KgTaskTemplateResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class ProdTaskDetailApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgTaskDetailResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/detail',
            operation_summary="获取单个任务详情",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    "taskid", 
                    openapi.IN_QUERY, 
                    description="任务ID", 
                    type=openapi.TYPE_INTEGER
                ),
            ],
            responses={
                200: KgTaskDetailResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        taskid = request.GET.get("taskid", None)
        if taskid:
            try:
                task = KgProductTask.objects.get(id=taskid)
                data['data'] = model_to_dict(task, exclude=['kg_doc_ids'])
                data['data']['kg_doc'] = task.kg_doc
                data['data']['kg_doc_type'] = task.kg_doc_type
                serializers = KgTaskDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgTaskDetailResponseSerializer(data={"code": 201, "msg": "不存在该任务"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)

        serializers = KgTaskDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class ProdTaskAddApiView(generics.GenericAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskDetailResponseSerializer


    @swagger_auto_schema(
        operation_summary='[可用] 新增任务功能',
        operation_description='POST /kgapp/task/add',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['doc_ids', "user_id"],
            properties={
                'doc_ids': openapi.Schema(type=openapi.TYPE_STRING, description="关联文档ID(,)"),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="任务名称"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="任务描述"),
                'taskType': openapi.Schema(type=openapi.TYPE_INTEGER,
                                           description="生产类型 0(知识导入)|1(自动生成)|2(全文生产)|3(图谱导入)|4(图谱自动生产)"),
            },
        ),
        responses={
            200: KgTaskDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['task']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        name = request.data.get("name", None)
        taskType = int(request.data.get("taskType", 0))
        desc = request.data.get("desc", None)
        doc_idstr = request.data.get("doc_ids", None)
        user_id = request.data.get("user_id", None)

        if name is None or doc_idstr is None or user_id is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgTaskDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            
            if len(doc_idstr) > 0:
                ids = str(doc_idstr).split(',')
                tmpdocs = KgDoc.objects.filter(id__in=ids).all()
            else:
                data = {"code": 201, "msg": "系统错误！！！" }
                serializers = KgTaskDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            try:
                tmpuser = User.objects.get(id=user_id)
            except:
                data = {"code": 202, "msg": "用户ID不存在！！！" }
                serializers = KgTaskDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            
            tmptask = KgProductTask()
            tmptask.create_time = datetime.now()
            tmptask.update_time = datetime.now()
            tmptask.name = name
            tmptask.desc = desc
            tmptask.task_type = taskType
            
            tmptask.kg_user_id = tmpuser
            tmptask.task_status = 0  #### 0 未执行,  1 任务开启, 执行数据装载, 2 数据装载完成, 3 比对任务开启, 4 比对任务完成, 5 最终任务完成, -1 任务失败
            tmptask.save()
            for doc in tmpdocs:
                tmptask.kg_doc_ids.add(doc)

            tmptask.save()
            data = {"code": 200, "msg": "任务新建成功" }
            data['data'] = model_to_dict(tmptask, exclude=['kg_doc_ids'])
            data['data']['kg_doc_type'] = tmptask.kg_doc_type
            serializers = KgTaskDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class ProdTaskUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskDetailResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 更新任务功能',
        operation_description='POST /kgapp/task/update',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['parent_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
                'doc_ids': openapi.Schema(type=openapi.TYPE_STRING, description="关联文档ID"),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="任务名称"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="任务描述"),
                'taskType': openapi.Schema(type=openapi.TYPE_INTEGER, description="生产类型 0(知识导入)|1(自动生成)|2(全文生产)"),
            },
        ),
        responses={
            200: KgTaskDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['task']
    )

    def post(self, request):
        data = {"code": 200 }
        name = request.data.get("name", None)
        taskType = request.data.get("taskType", None)
        desc = request.data.get("desc", None)
        doc_idstr = request.data.get("doc_ids", None)
        user_id = request.data.get("user_id", None)
        task_id = request.data.get("task_id", None)

        try:
            tmptask = KgProductTask.objects.get(id=task_id)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 201, "msg": "用户ID不存在！！！" }
            serializers = KgTaskDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        if len(doc_idstr) > 0:
            docids = str(doc_idstr).split(",")
            try:
                tmpdocs = KgDoc.objects.filter(id__in=docids).all()
            except:
                data = {"code": 201, "msg": "系统错误" }
                serializers = KgTaskDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            
        
        tmptask.update_time = datetime.now()
        tmptask.name = name
        if desc is not None:
            tmptask.desc = desc

        if taskType is not None:
            tmptask.task_type = int(taskType)
        tmptask.kg_doc_ids.clear()
        for doc in tmpdocs:
            tmptask.kg_doc_ids.add(doc)
        tmptask.kg_user_id = tmpuser
        tmptask.save()
        data = {"code": 200, "msg": "任务更新成功" }
        serializers = KgTaskDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class ProdTaskDelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgTaskDetailResponseSerializer
    @swagger_auto_schema(
        operation_description="任务删除",
        operation_summary="[可用] 任务删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="任务ID"),
            },
        ),
        responses={
            200: KgTaskDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['task']
    )
    @csrf_exempt
    def post(self, request):
        global neo_client
        taskid = request.data["id"]
        if taskid is None:
            serializers = KgTaskDetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgProductTask.objects.get(id=taskid)
            if tmpkg:
                # 图谱删除
                if tmpkg.task_type == 3:
                    neo_client = None
                    try:
                        neo_client = Neo4j()
                    except:
                        print("neo4j 客户端连接出错...")
                        pass
                    try:
                        KgEntity.objects.filter(task=tmpkg).all().delete()
                        KgRelation.objects.filter(task=tmpkg).all().delete()
                        neo_client.deleteTaskAll(task_id=taskid)
                    except:
                        print("neo4j|数据库 -> 操作异常...")
                        pass
                tmpkg.delete()
                serializers = KgTaskDetailResponseSerializer(data={"code": 200, "msg": "该任务删除成功" }, many=False)
            else:
                serializers = KgTaskDetailResponseSerializer(data={"code": 201, "msg": "任务不存在" }, many=False)
        except:
            serializers = KgTaskDetailResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    


class TaskStatusApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgTaskStatusResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/status',
            operation_summary="异步任务状态",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    "taskid", 
                    openapi.IN_QUERY, 
                    description="任务ID", 
                    type=openapi.TYPE_INTEGER
                ),
                openapi.Parameter(
                    "taskstep", 
                    openapi.IN_QUERY, 
                    description="子任务步骤0(数据装载)|1(任务生产)", 
                    type=openapi.TYPE_INTEGER
                ),
            ],
            responses={
                200: KgTaskStatusResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):
        taskid = request.GET.get("taskid", None)
        taskstep = request.GET.get("taskstep", None)
        if taskid is None or taskstep is None:
            data = {"code": 201, "msg": "参数错误！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        tmptask = KgTask.objects.filter(kg_prod_task_id=taskid, task_step=taskstep).first()
        if tmptask:
            from celery.result import AsyncResult
            celery_task = AsyncResult(tmptask.celery_id)
            celery_status = celery_task.status
        else:
            celery_status = 'TASK_NOT_FOUND'
        data = {"code": 200, "msg": "", "status":  celery_status}
        serializers = KgTaskStatusResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TaskLoadApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskStatusResponseSerializer
    
    
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/load',
            operation_summary="装载数据任务",
            # 接口参数 GET请求参数
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
                'model_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="模型ID"),
                'force': openapi.Schema(type=openapi.TYPE_INTEGER, description="强制执行  0|1"),
            },
        ),
            responses={
                200: KgTaskStatusResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def post(self, request, *args, **kwargs):

        # 根据不同的任务，启动不同的装载数据方式
        task_id = request.data.get("task_id", None)
        model_id = request.data.get("model_id", None)
        force = int(request.data.get("force", 0))
        try:
            tmptask = KgProductTask.objects.get(id=task_id)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        if not force:
            t = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).filter()
            if t:
                if tmptask.task_status == 0:
                    data = {"code": 202, "msg": "数据加载任务已经开始"}
                else:
                    data = {"code": 203, "msg": "数据加载已经完成"}
                serializers = KgTaskStatusResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).delete()
        
        # 任务开始
        tmptask.task_status = 1
        tmptask.save()
        taskType = tmptask.task_type
        from yunheKGPro.celery import loadKgFromDoc, autoProWithLLM, autoFullProWithLLM, loadGraphKgFromDoc
        # 知识导入
        result = None
        param_dict = model_to_dict(tmptask, exclude=['kg_doc_ids'])
        param_dict['doc_ids'] = tmptask.kg_docid_list
        print("param_dict->", param_dict)
        if taskType == 0:
            result = loadKgFromDoc.delay(param_dict)
            print("result:",result)
        # 自动生产
        elif taskType == 1:
            try:
                tmpmodel = KgModel.objects.get(id=model_id)
            except:
                data = {"code": 204, "msg": "模型ID参数错误！！！" }
                serializers = KgTaskStatusResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            param_dict['model'] = model_to_dict(tmpmodel)
            result = autoProWithLLM.delay(param_dict)
        # 全文生产 全文生产 全文生产
        elif taskType == 2:
            try:
                tmpmodel = KgModel.objects.get(id=model_id)
            except:
                data = {"code": 204, "msg": "模型ID参数错误！！！" }
                serializers = KgTaskStatusResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            
            param_dict['model'] = model_to_dict(tmpmodel)
            result = autoFullProWithLLM.delay(param_dict)

        # 图谱导入功能
        elif taskType == 3:
            result = loadGraphKgFromDoc.delay(param_dict)
            print(result)
        # 记录 celery id 入库 
        if result:
            tmpkg, tmpbool = KgTask.objects.get_or_create(kg_prod_task_id=tmptask, task_step=0, celery_id=result.id)
            if tmpbool:
                print("LoadTask 任务创建成功...", tmpkg)
        
        data = {"code": 200, "msg": "数据加载任务创建成功" }
        serializers = KgTaskStatusResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgTmpGraphList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = KgGraphResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/tmpgraph/',
        operation_summary="获取临时图谱节点列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="任务ID"),
            # openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            # openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgGraphResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['task'])
    def get(self, request, *args, **kwargs):

        taskId = request.GET.get("taskId", None)
        try:
            tmptask = KgProductTask.objects.get(id=taskId)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！"}
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        loadtask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).first()
        from celery.result import AsyncResult
        res = AsyncResult(loadtask.celery_id)  # 参数为task id
        if not res:
            data = {"code": 20, "msg": "任务ID结果不存在"}
            serializers = KgGraphResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        data = res.result['data']
        # print("KgTmpGraphList->", data)
        serializers = KgGraphResponseSerializer(data={
            "data": data,
            "msg": "获取数据成功!",
            "code": 200,
        }, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTmpSimGraphList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = KgGraphResponseSerializer
    #TODO
    @swagger_auto_schema(
        operation_description='GET /kgapp/tmpsimgraph/',
        operation_summary="获取临时解析相似实体 实体对齐",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="任务ID"),
            # openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            # openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgGraphResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        taskId = request.GET.get("taskId", None)
        try:
            tmptask = KgProductTask.objects.get(id=taskId)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！"}
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        simtask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=1).first()
        from celery.result import AsyncResult
        res = AsyncResult(simtask.celery_id)  # 参数为task id
        if not res:
            data = {"code": 20, "msg": "任务ID结果不存在"}
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        data = res.result['data']
        # print("KgTmpSimGraphList->", data)
        serializers = KgGraphResponseSerializer(data={
            "data": data,
            "msg": "获取数据成功!",
            "code": 200,
        }, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TaskProductApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskStatusResponseSerializer
    
    
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/product',
            operation_summary="执行具体任务",
            # 接口参数 GET请求参数
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
                'force': openapi.Schema(type=openapi.TYPE_INTEGER, description="强制执行  0|1"),
            },
        ),
            responses={
                200: KgTaskStatusResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def post(self, request, *args, **kwargs):

        # 根据不同的任务，启动不同的装载数据方式
        task_id = request.data.get("task_id", None)
        force = int(request.data.get("force", 0))
        try:
            tmptask = KgProductTask.objects.get(id=task_id)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        print("【TaskProductApiView】", tmptask)
        if tmptask.task_status == 0:
            data = {"code": 201, "msg": "任务尚未开启" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        if tmptask.task_status == 1:
            data = {"code": 202, "msg": "数据任务尚未完成" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        if not force:
            t = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=1).all()
            if t:
                data = {"code": 203, "msg": "生产任务已经完成" }
                serializers = KgTaskStatusResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=1).delete()

        # 任务开始
        tmptask.task_status = 3
        tmptask.save()

        taskType = tmptask.task_type
        from yunheKGPro.celery import productKgSimTask, autoProSimQATask, autoFullProSimTask, importKgGraphSimTask
        # 知识导入

        param_dict = model_to_dict(tmptask, exclude=['kg_doc_ids'])
        param_dict['doc_ids'] = tmptask.kg_docid_list
        if taskType == 0:
            result = productKgSimTask.delay(param_dict)
        # 自动生产
        elif taskType == 1:
            result = autoProSimQATask.delay(param_dict)
        # 全文生产
        elif taskType == 2:
            result = autoFullProSimTask.delay(param_dict)
        # 知识图谱比对
        elif taskType == 3:
            result = importKgGraphSimTask.delay(param_dict)
        # 记录 celery id 入库 
        tmpkg, tmpbool = KgTask.objects.get_or_create(kg_prod_task_id=tmptask, task_step=1, celery_id=result.id)
        if tmpbool:
            print("ProductTask 任务创建成功...", tmpkg)
        data = {"code": 200, "msg": "生产任务创建成功" }
        serializers = KgTaskStatusResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)

class TaskLoadDoneApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskStatusResponseSerializer
    
    
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/kgloaddone',
            operation_summary="知识导入最终数据入库",
            # 接口参数 GET请求参数
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
                'qa_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_INTEGER), description="需要保存ID"),
                'replace_qa_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_INTEGER), description="需要替换的ID(删除的)"),
            },
        ),
            responses={
                200: KgTaskStatusResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def post(self, request, *args, **kwargs):

        # 根据不同的任务，启动不同的装载数据方式
        task_id = request.data.get("task_id", None)
        qa_ids = request.data.get("qa_ids", [])
        replace_qa_ids = request.data.get("replace_qa_ids", [])
        try:
            tmptask = KgProductTask.objects.get(id=task_id)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        datatask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=1).first()
        if datatask is None:
            data = {"code": 202, "msg": "暂无生产子任务失败" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        from celery.result import AsyncResult
        import pprint
        res = AsyncResult(datatask.celery_id) # 参数为task id
        if not res:
            data = {"code": 200, "msg": "任务ID结果不存在" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        print("res.result:", res.result)
        resultSet = res.result['data']
        
        ## 新入库文档
        for ent in resultSet:
            tmpid = ent['id']
            if tmpid not in qa_ids:
                continue
            del ent['id']
            del ent['doc']
            del ent['simqas']
            ent['task_id'] = tmptask
            ent['update_time'] = datetime.now()
            ent['create_time'] = datetime.now()
            # ent['kg_user_id'] = User.objects.get(id=tmptask.kg_user_id)
            ent['kg_user_id'] = tmptask.kg_user_id
            ent['doc_id'] = KgDoc.objects.get(id=ent['doc_id'])
            print("--->", dict(ent))
            KgQA.objects.create(**dict(ent))
        ## 替换文档
        if replace_qa_ids:
            KgQA.objects.filter(id__in=replace_qa_ids).delete()
        tmptask.task_status = 5
        tmptask.save()
        data = {"code": 200, "msg": "任务流程结束." }
        serializers = KgTaskStatusResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class TaskImportGraphDoneApiView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskStatusResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/task/kgimportgraphdone',
        operation_summary="图谱最终数据入库",
        # 接口参数 GET请求参数
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
                'ent_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_INTEGER),
                                         description="需要保存ID"),
                'replace_id_pairs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_OBJECT),
                                                 description="需要替换的ID,新的替换"),
            },
        ),
        responses={
            200: KgTaskStatusResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['task'])
    def post(self, request, *args, **kwargs):

        # 根据不同的任务，启动不同的装载数据方式
        task_id = request.data.get("task_id", None)
        ent_ids = request.data.get("ent_ids", [])
        replace_id_pairs = request.data.get("replace_id_pairs", {})
        try:
            tmptask = KgProductTask.objects.get(id=task_id)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！"}
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        from yunheKGPro.celery import importGraphKgByCelery
        # 知识导入
        param_dict = model_to_dict(tmptask, exclude=['kg_doc_ids'])
        param_dict['ent_ids'] = ent_ids
        param_dict['replace_id_pairs'] = replace_id_pairs

        try:
            result = importGraphKgByCelery.delay(param_dict)
            # 记录 celery id 入库
            tmpkg, tmpbool = KgTask.objects.get_or_create(kg_prod_task_id=tmptask, task_step=2, celery_id=result.id)
            if tmpbool:
                print("ProductTask 知识图谱入库任务创建成功...", tmpkg)
            # 图谱构建中....
            tmptask.task_status = 10
            tmptask.save()
        except:
            serializers = KgTaskStatusResponseSerializer(data={"code": 202, "msg": "图谱入库任务创建失败,请重新建立导入任务!"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgTaskStatusResponseSerializer(data={"code": 200, "msg": "图谱入库任务创建成功!"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TaskFullDoneApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskStatusResponseSerializer
    
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/kgfulldone',
            operation_summary="全文生产数据入库",
            # 接口参数 GET请求参数
            request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
            },
        ),
            responses={
                200: KgTaskStatusResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def post(self, request, *args, **kwargs):

        # 根据不同的任务，启动不同的装载数据方式
        task_id = request.data.get("task_id", None)
        try:
            tmptask = KgProductTask.objects.get(id=task_id)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        datatask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).first()
        if datatask is None:
            data = {"code": 202, "msg": "暂无生产子任务失败" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        from celery.result import AsyncResult
        import pprint
        res = AsyncResult(datatask.celery_id) # 参数为task id
        if not res:
            data = {"code": 20, "msg": "任务ID结果不存在" }
            serializers = KgTaskStatusResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        resultSet = res.result['data']
        
        ## 解析文档入库
        for ent in resultSet:
            tmpdocid = ent['id']
            tmpdocdesc = ent['desc']
            doc = KgDoc.objects.get(id=tmpdocid)
            doc.desc = tmpdocdesc
            doc.update_time = datetime.now()
            doc.prodflag = 1
            doc.save()
        tmptask.task_status = 5
        tmptask.save()
        data = {"code": 200, "msg": "全文生产任务流程结束." }
        serializers = KgTaskStatusResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)
    

class TaskApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgTaskResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/task/demo',
            operation_summary="异步任务测试",
            # 接口参数 GET请求参数
            manual_parameters=[
            ],
            responses={
                200: KgTaskResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):
        from yunheKGPro.celery import add
        result = add.delay(3, 5)
        #print({"taskid":result.id, "status": result.status })
        return Response({"taskid":result.id, "status": result.status },  status=status.HTTP_200_OK)

class TaskApiTestView(mixins.ListModelMixin,
                         generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgTaskStatusResponseSerializer

    @swagger_auto_schema(
        operation_description='POST /kgapp/task/result',
        operation_summary="获取任务结果",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="任务ID"),
            },
        ),
        responses={
            200: KgTaskStatusResponseSerializer(many=False),
            202: "任务尚未完成",
            400: "请求失败",
        },
        tags=['task']
    )
    def post(self, request, *args, **kwargs):
        task_id = request.data.get("task_id", None)
        if task_id is None:
            return Response({"code": 400, "msg": "任务ID不能为空"}, status=status.HTTP_400_BAD_REQUEST)
        from celery.result import AsyncResult
        # 尝试获取任务状态
        result = AsyncResult(task_id)
        if result.ready():
            # 任务完成，返回结果
            return Response({"result": result.result}, status=status.HTTP_200_OK)
        else:
            # 任务尚未完成
            return Response({"status": result.status}, status=status.HTTP_202_ACCEPTED)

class kgFullProdList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgDocResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/tmpfullprod/',
            operation_summary="获取全文解析生产列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="任务ID"),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgDocResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        taskId = request.GET.get("taskId", None)
        if taskId is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        try:
            tmptask = KgProductTask.objects.get(id=taskId)
        except:
            data = {"code": 201, "msg": "任务ID不存在！！！" }
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        # querySet = KgTmpQA.objects.filter(task_id=taskId, doc_id=docId).all().order_by('-update_time')
        

        datatask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).first()
        from celery.result import AsyncResult
        res = AsyncResult(datatask.celery_id) # 参数为task id
        if not res:
            data = {"code": 201, "msg": "任务ID结果不存在" }
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if 'data' not in res.result:
            data = {"code": 202, "msg": "暂无生产结果" }
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        querySet = res.result['data']
        data['total'] = len(querySet)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize) 
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        kds = KgDocSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


