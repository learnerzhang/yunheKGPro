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
import os
import collections

from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from apiapp.serializers import BaseApiResponseSerializer
from yunheKGPro import CsrfExemptSessionAuthentication
# Create your views here.

class KgTempList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/Kgtemp/',
            operation_summary="获取所有模板列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    #参数名称
                    "keyword", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="模板关键词模糊搜索", 
                    # 参数字符类型
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间',),
                openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间',),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgTempResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['temp'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        querySet = KgTemplates.objects
        
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(name__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lt="{}".format(end_time))
        querySet = querySet.all().order_by('-updated_at')
        # querySet = KgDoc.objects.all()
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
        kds = KgTemplateSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgTempResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgTempDetailApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgTempDetailResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtemp/detail',
            operation_summary="获取单个模板详情",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    #参数名称
                    "tmpid", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="模板ID", 
                    # 参数字符类型
                    type=openapi.TYPE_INTEGER
                ),
            ],
            responses={
                200: KgTempDetailResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['temp'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        tmpid = request.GET.get("tmpid", None)
        if tmpid:
            try:
                tmp = KgTemplates.objects.get(id=tmpid)
                data['data'] = model_to_dict(tmp, exclude=['path'])
                data['data']['filepath'] = tmp.filepath
                data['data']['kg_user'] = tmp.kg_user
                data['data']['kg_cct_id'] = tmp.kg_ctt_id
                data['data']['kg_cct'] = tmp.kg_ctt
                data['data']['kg_business'] = tmp.kg_business
                serializers = KgTempDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgTempDetailResponseSerializer(data={"code": 201, "msg": "不存在该模板"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)

        serializers = KgTempDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgTempAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True
    @swagger_auto_schema(
        operation_summary='[可用] 新增业务模板功能',
        operation_description='POST /kgapp/kgtemp/add',
        manual_parameters=[
           openapi.Parameter(
               name='file',
               in_=openapi.IN_FORM,
               description='上传的文件',
               type=openapi.TYPE_FILE
           ),
           openapi.Parameter(
               name='name',
               in_=openapi.IN_FORM,
               description='模板名称',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='desc',
               in_=openapi.IN_FORM,
               description='模板描述',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='bus_id',
               in_=openapi.IN_FORM,
               description='业务ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='create_date',
               in_=openapi.IN_FORM,
               description='创建时间',
               type=openapi.FORMAT_DATE
           ),
           openapi.Parameter(
               name='version',
               in_=openapi.IN_FORM,
               description='版本',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='cid',
               in_=openapi.IN_FORM,
               description='所属目录ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='user_id',
               in_=openapi.IN_FORM,
               description='创建作者',
               type=openapi.TYPE_INTEGER
           ),
        ],
        responses={
            200: KgTempResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['temp']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        tmpfile = request.data.get("file", None)
        name = request.data.get("name", None)
        version = request.data.get("version", '')
        desc = request.data.get("desc", None)
        bus_id = request.data.get("bus_id", None)
        user_id = request.data.get("user_id", None)
        create_date = request.data.get("create_date", None)
        cid = request.data.get("cid", None)
        if tmpfile is None or bus_id is None or cid is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgTempResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            filename = str(tmpfile)
            filetype = filename.split(".")[-1]
            new_filename = str(abs(hash(filename + str(time.time())))) + "." + filetype
            local_dir = os.path.join("media", "temps")
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
                print("create", local_dir, "!!!")
            else:
                print("subdir", local_dir, "exist!!!")
            new_path = os.path.join(local_dir, new_filename)
            try:
                f = open(new_path, "wb+")
                for chunk in tmpfile.chunks():
                    f.write(chunk)
                f.close()
            except:
                data = {"code": 201, "msg": "模板文件写入错误..." }
                serializers = KgTempResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            filepath = os.path.join("temps", new_filename)
            try:
                tmpuser = User.objects.get(id=user_id)
            except:
                data = {"code": 201, "msg": "用户ID不存在！！！" }
                serializers = KgTempResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            
            tmpctc = KgTempTableContent.objects.get(id=cid)
            tmpbus = KgBusiness.objects.get(id=bus_id)
            tmp, tmpbool = KgTemplates.objects.get_or_create(name=name, kg_business_id=tmpbus, kg_temp_content_id=tmpctc,version=version)
            if desc:
                tmp.desc = desc
            
            if create_date:
                tmp.created_at = create_date
            else:
                tmp.created_at = datetime.now()
            tmp.version = version
            tmp.updated_at = datetime.now()
            tmp.path = filepath
            tmp.kg_user_id = tmpuser
            tmp.save()
            if tmpbool:
                data = {"code": 200, "msg": "模板保存成功" }
            else:
                data = {"code": 201, "msg": "该业务下模板名称已经存在,更新模板文件..." }
            
            data['data'] = model_to_dict(tmp, exclude=['path'])
            data['data']['filepath'] = tmp.filepath
            data['data']['kg_user'] = tmp.kg_user
            data['data']['kg_cct_id'] = tmp.kg_ctt_id
            data['data']['kg_cct'] = tmp.kg_ctt
            data['data']['kg_business'] = tmp.kg_business
            serializers = KgTempResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class KgTempUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    # serializer_class = KgDocResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgDocResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True
    @swagger_auto_schema(
        operation_summary='[可用] 更新模板功能',
        operation_description='[可用] 更新模板功能',
        manual_parameters=[
           openapi.Parameter(
               name='file',
               in_=openapi.IN_FORM,
               description='上传的文件',
               type=openapi.TYPE_FILE
           ),
           openapi.Parameter(
               name='name',
               in_=openapi.IN_FORM,
               description='模板名称',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='desc',
               in_=openapi.IN_FORM,
               description='模板描述',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='bus_id',
               in_=openapi.IN_FORM,
               description='业务ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='create_date',
               in_=openapi.IN_FORM,
               description='创建时间',
               type=openapi.FORMAT_DATE
           ),
           openapi.Parameter(
               name='version',
               in_=openapi.IN_FORM,
               description='版本',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='user_id',
               in_=openapi.IN_FORM,
               description='创建作者',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='temp_id',
               in_=openapi.IN_FORM,
               description='模板',
               type=openapi.TYPE_INTEGER
           ),
        ],
        responses={
            200: KgTempResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['temp']
    )
    def post(self, request):
        data = {"code": 200 }
        tmpfile = request.data.get("file", None)
        name = request.data.get("name", None)
        version = request.data.get("version", None)
        desc = request.data.get("desc", None)
        bus_id = request.data.get("bus_id", None)
        temp_id = request.data.get("temp_id", None)
        user_id = request.data.get("user_id", None)
        create_date = request.data.get("create_date", None)

        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 201, "msg": "用户ID不存在！！！" }
            serializers = KgTempResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if temp_id is None:
            data['code'] = 201
            data['msg'] = '模板ID参数不能为空！！！'
            serializers = KgTempResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        tmpbus = KgBusiness.objects.get(id=bus_id)
        tmp = KgTemplates.objects.get(id=temp_id)
        if tmpfile:
            filename = str(tmpfile)
            # new_filename = str(abs(hash(filename + str(time.time())))) + "." + filetype
            local_dir = os.path.join("media", "temps")
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
                print("create", local_dir, "!!!")
            else:
                print("subdir", local_dir, "exist!!!")
            new_path = os.path.join(local_dir, filename)
            print("upload name:", filename, new_path)
            try:
                f = open(new_path, "wb+")
                for chunk in tmpfile.chunks():
                    f.write(chunk)
                f.close()
            except:
                data = {"code": 201, "msg": "文件写入错误..." }
                serializers = KgTempResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            filepath = os.path.join("temps", filename)
            tmp.path = filepath
            # tmpdoc.filename = filename
        if desc:
            tmp.desc = desc
        if create_date:
            tmp.created_at = create_date
        if version:
            tmp.version = version
        if name:
            tmp.name = name
        tmp.kg_user_id = tmpuser
        tmp.kg_business_id = tmpbus
        tmp.updated_at = datetime.now()
        tmp.save()
        data = {"code": 200, "msg": "模板更新成功" }
        serializers = KgTempResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTempDelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgTempResponseSerializer

    @swagger_auto_schema(
        operation_description="模板删除",
        operation_summary="[可用] 模板删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="模板ID"),
            },
        ),
        responses={
            200: KgTempResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    @csrf_exempt
    def post(self, request):
        data = {"code": 200 }

        tmpid = None
        if request.POST:
            tmpid = request.POST["id"]
        if tmpid is None:
            tmpid = request.data["id"]
        if tmpid is None:
            serializers = KgTempResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgTemplates.objects.get(id=tmpid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgTempResponseSerializer(data={"code": 200, "msg": "模板删除成功" }, many=False)
            else:
                serializers = KgTempResponseSerializer(data={"code": 201, "msg": "模板不存在" }, many=False)
        except:
            serializers = KgTempResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    


class KgBusList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgBusResponseSerializer
    
    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtbus/',
            operation_summary="获取所有业务列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    "keyword", 
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="业务模糊搜索", 
                    # 参数字符类型
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            tags = ['temp'])
    
    def get(self, request, *args, **kwargs):
        data = {"code": 200 }
        keyword = request.GET.get('keyword', None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        if keyword:
            values = KgBusiness.objects.filter(name__icontains=keyword).all().order_by('-updated_at')
        else:
            values = KgBusiness.objects.all().order_by('-updated_at')

        data['total'] = len(values)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(values, pageSize) 
        try:
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        data['data'] = [model_to_dict(e) for e in values]
        serializers = KgBusResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class BusAddApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer
    
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtbus/add',
            operation_summary="新增业务",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['user_id'],
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签"),
                },
            ),
            tags = ['temp'])
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        name = request.data.get('name', None)
        print(request.data)
        if user_id and name:
            tmpuser = User.objects.get(id=user_id)
            print("user:", tmpuser)
           
            try:
                tmpbus, tmpbool = KgBusiness.objects.get_or_create(name=name)
                if tmpbool:
                    tmpbus.created_at = datetime.now()
                    tmpbus.updated_at = datetime.now()
                    tmpbus.kg_user_id = tmpuser
                    tmpbus.save()
                    serializers = KgBusResponseSerializer(data={"code": 200, "msg": "新建业务成功"}, many=False)
                else:
                    serializers = KgBusResponseSerializer(data={"code": 202, "msg": "业务已存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgBusResponseSerializer(data={"code": 201, "msg": "用户不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        
        serializers = KgBusResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)

    

class BusUpdateApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtbus/update',
            operation_summary="业务更新",
            # 接口参数 GET请求参数

            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['user_id'],
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                    'bus_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="业务ID"),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="业务名称"),
                },
            ),
            tags = ['temp'])
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        bus_id = request.data.get('bus_id', None)
        name = request.data.get('name', None)
        if bus_id is None:
            serializers = KgBusResponseSerializer(data={"code": 201, "msg": "业务ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        if user_id and name:
            try:
                tmpuser = User.objects.get(id=user_id)
                tmpbus = KgBusiness.objects.get(id=bus_id)
                tmpbus.kg_user_id = tmpuser
                tmpbus.name = name
                tmpbus.save()
                serializers = KgBusResponseSerializer(data={"code": 200, "msg": "业务更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgBusResponseSerializer(data={"code": 201, "msg": "用户不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        serializers = KgBusResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)
    

class BusDelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgBusResponseSerializer

    @swagger_auto_schema(
        operation_description="业务删除",
        operation_summary="[可用] 业务删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="文件ID"),
            },
        ),
        responses={
            200: KgBusResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['temp']
    )
    @csrf_exempt
    def post(self, request):
        data = {"code": 200 }

        tagid = None
        if request.POST:
            tagid = request.POST["id"]
        if tagid is None:
            tagid = request.data["id"]
        if tagid is None:
            serializers = KgBusResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgBusiness.objects.get(id=tagid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgBusResponseSerializer(data={"code": 200, "msg": "业务删除成功" }, many=False)
            else:
                serializers = KgBusResponseSerializer(data={"code": 201, "msg": "业务不存在" }, many=False)
        except:
            serializers = KgBusResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)

    
class KgTabCTTList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgTabCTTResponseSerializer
    
    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtempctt/',
            operation_summary="获取目录列表",
            # 接口参数 GET请求参数
            manual_parameters=[
            ],
            tags = ['temp'])
    
    def get(self, request, *args, **kwargs):

        def arr2tree(source, parent):
            tree = []
            for item in source:
                if item['parent_id'] == parent:
                    item['children'] = arr2tree(source, item['id'])
                    tree.append(item)
            return tree
        
        data = {"code": 200 }
        ctts = KgTempTableContent.objects.all().order_by('-updated_at')

        tmpctts = [model_to_dict(ctt) for ctt in ctts]
        data['tabctt'] = arr2tree(tmpctts, 0)
        serializers = KgTabCTTResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgTabCTTAddAPIList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgTabCTTResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtempctt/add',
            operation_summary="新增目录",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['parent_id'],
                properties={
                    'parent_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="目录名称"),
                },
            ),
            tags = ['temp'])
    
    def post(self, request, *args, **kwargs):
        data={"code": 200, "msg": "目录创建成功"}
        parent_id = int(request.data.get('parent_id', 0))
        user_id = request.data.get('user_id', None)
        name = request.data.get('name', None)
        if name is None or len(name) == 0:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        if user_id:
            tmpUser = User.objects.get(id=user_id)
        else:
            tmpUser = None
        tmpctt, tmpbool = KgTempTableContent.objects.get_or_create(parent_id=parent_id, name=name)
        if tmpbool:
            if tmpUser:
                tmpctt.kg_user_id = tmpUser
                tmpctt.save()
            data['msg'] = "创建成功"
        else:
            data={"code": 202, "msg": "已经存在该目录"}

        data['data'] = model_to_dict(tmpctt, exclude=[''])
        serializers = KgTabCTTResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgTabCTTDelAPIList(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgTabCTTResponseSerializer

    @swagger_auto_schema(
        operation_description="目录删除",
        operation_summary="[可用] 目录删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="文件ID"),
            },
        ),
        responses={
            200: KgTabCTTResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['temp']
    )
    @csrf_exempt
    def post(self, request):
        cctid = None
        if request.POST:
            cctid = request.POST["id"]
        if cctid is None:
            cctid = request.data["id"]
        if cctid is None:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            querySet = KgTemplates.objects.filter(kg_temp_content_id__id="{}".format(cctid))
            if len(querySet) > 0:
                serializers = KgTabCTTResponseSerializer(data={"code": 202, "msg": "该文件夹下存在文件，不能直接删除" }, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            
            tmpkg = KgTempTableContent.objects.get(id=cctid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgTabCTTResponseSerializer(data={"code": 200, "msg": "当前目录删除成功" }, many=False)
            else:
                serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "目录不存在" }, many=False)
        except:
            serializers = KgTabCTTResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTabCTTUpdateAPIList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtempctt/update',
            operation_summary="更新目录名称",
            # 接口参数 GET请求参数
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['id'],
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="标签ID"),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签"),
                },
            ),
            tags = ['temp'])
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        ctt_id = request.data.get('id', None)
        name = request.data.get('name', None)
        if ctt_id is None:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "文档ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        if user_id:
            tmpuser = User.objects.get(id=user_id)
        else:
            tmpuser = None

        if ctt_id and name:
            try:
                tmpcct = KgTempTableContent.objects.get(id=ctt_id)
                if tmpuser:
                    tmpcct.kg_user_id = tmpuser
                tmpcct.name = name
                tmpcct.save()
                serializers = KgTabCTTResponseSerializer(data={"code": 200, "msg": "目录更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "目录ID不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
class KgTempByCttList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/kgtemp/listByCtt',
            operation_summary="获取目录下所有模板列表",
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
                    "cid", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="目录的ID", 
                    # 参数字符类型
                    type=openapi.TYPE_INTEGER
                ),
                openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的开始时间',),
                openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的结束时间',),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgTempResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['temp'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        cid = request.GET.get("cid", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        querySet = KgTemplates.objects
        if cid is not None and len(cid) > 0:
            querySet = querySet.filter(kg_temp_content_id__id="{}".format(cid))
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(title__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lt="{}".format(end_time))
        querySet = querySet.all()
        # querySet = KgDoc.objects.all()
        data['total'] = len(querySet)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize) 
        try:
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs =  paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        kds = KgTemplateSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgTempResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)