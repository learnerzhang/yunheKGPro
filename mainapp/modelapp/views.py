import json
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
from modelapp.serializers import *
from modelapp.models import *
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
from rest_framework.permissions import IsAuthenticated
import os

from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from yaapp.serializer import BaseApiResponseSerializer
from yunheKGPro import CsrfExemptSessionAuthentication
# Create your views here.

class KgModelList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # permission_classes = [IsAuthenticated]  # 确保用户已认证
    serializer_class = KgModelResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /modelapp/kgmodel/',
            operation_summary="获取所有模型列表",
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
                openapi.Parameter(
                    #参数名称
                    "function", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="模型能力", 
                    # 参数字符类型
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter('activate', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="可用状态 0|1", ),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgModelResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['model'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        activate = request.GET.get("activate", None)
        function = request.GET.get("function", None)
        pageSize = request.GET.get("pageSize", 10)

        querySet = KgModel.objects
        if keyword:
            querySet = querySet.filter(name__contains="{}".format(keyword))
        if activate:
            querySet = querySet.filter(activate=int(activate))
        if function:
            querySet = querySet.filter(function=function)

        querySet = querySet.all().order_by('-update_time')

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
        # if keyword:
        #     for o in objs:
        #         o.highlight_title = str(o.title).replace(f"{keyword}", f"<span style=\"color:#F56C6C;\">{keyword}</span>")
        #         # o.title = str(o.title).replace(f"{keyword}", f"<span>{keyword}</span>")
        kds = KgModelSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgModelResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class ModelDetailApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgModelDetailResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /modelapp/kgmodel/detail',
            operation_summary="获取单个模型详情",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    #参数名称
                    "mid", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="模型ID", 
                    # 参数字符类型
                    type=openapi.TYPE_INTEGER
                ),
            ],
            responses={
                200: KgModelDetailResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['model'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        mid = request.GET.get("mid", None)
        if mid:
            try:
                doc = KgModel.objects.get(id=mid)
                data['data'] = model_to_dict(doc, exclude=[''])
                serializers = KgModelDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgModelDetailResponseSerializer(data={"code": 201, "msg": "不存在该模型"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)

        serializers = KgModelDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)

class ModelTypeListApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgModelTypeResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /modelapp/kgmodel/typelist',
            operation_summary="获取模型能力列表",
            # 接口参数 GET请求参数
            manual_parameters=[
            ],
            responses={
                200: KgModelTypeResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['model'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        try:
            tmpmodels = KgModel.objects.all()
            data['data'] = list(set([m.function  for m in tmpmodels]))
            serializers = KgModelTypeResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        except:
            serializers = KgModelTypeResponseSerializer(data={"code": 201, "msg": "系统错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)


class ModelAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True
    @swagger_auto_schema(
        operation_summary='[可用] 新增模型功能',
        operation_description='POST /modelapp/kgmodel/add/',
        manual_parameters=[
           openapi.Parameter(
               name='name',
               in_=openapi.IN_FORM,
               description='模型名称',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='function',
               in_=openapi.IN_FORM,
               description='功能介绍',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='desc',
               in_=openapi.IN_FORM,
               description='模型描述',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='url',
               in_=openapi.IN_FORM,
               description='调用接口',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='version',
               in_=openapi.IN_FORM,
               description='版本号',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='req_type',
               in_=openapi.IN_FORM,
               description='请求类型 0(post)|1(get)',
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
            200: KgModelDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['model']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        name = request.data.get("name", None)
        function = request.data.get("function", None)
        desc = request.data.get("desc", None)
        user_id = request.data.get("user_id", None)
        url = request.data.get("url", None)
        version = request.data.get("version", None)
        req_type = request.data.get("req_type", 0)
        if name is None or user_id is None or version is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgModelDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            try:
                tmpuser = User.objects.get(id=user_id)
            except:
                data = {"code": 201, "msg": "用户ID不存在！！！" }
                serializers = KgModelDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
 
            tmpModel, tmpbool = KgModel.objects.get_or_create(name=name, version=version)
            if tmpbool:
                tmpno = len(KgModel.objects.all())
                tmpModel.desc = desc
                tmpModel.create_time = datetime.now()
                tmpModel.update_time = datetime.now()
                tmpModel.function = function
                tmpModel.url = url
                tmpModel.no = tmpno
                tmpModel.activate = 0
                tmpModel.req_type = req_type
                tmpModel.kg_user_id = tmpuser
                tmpModel.save()
                data = {"code": 200, "msg": "模型创建成功" }
            else:
                data = {"code": 201, "msg": "该版本模型已存在~~~" }
            
            data['data'] = model_to_dict(tmpModel, exclude=[''])
            serializers = KgModelDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

class ModelUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    # serializer_class = KgModelResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgModelResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = BaseApiResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 更新模型功能',
        operation_description='[可用] 更新模型功能',
        manual_parameters=[
           openapi.Parameter(
               name='name',
               in_=openapi.IN_FORM,
               description='模型名称',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='function',
               in_=openapi.IN_FORM,
               description='功能介绍',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='desc',
               in_=openapi.IN_FORM,
               description='模型描述',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='url',
               in_=openapi.IN_FORM,
               description='调用接口',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='version',
               in_=openapi.IN_FORM,
               description='版本号',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='req_type',
               in_=openapi.IN_FORM,
               description='请求类型 0(post)|1(get)',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='user_id',
               in_=openapi.IN_FORM,
               description='创建作者ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='mid',
               in_=openapi.IN_FORM,
               description='模型ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='activate',
               in_=openapi.IN_FORM,
               description='模型状态',
               type=openapi.TYPE_INTEGER
           ),
        ],
        responses={
            200: KgModelResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['model']
    )
    def post(self, request):
        data = {"code": 200 }
        name = request.data.get("name", None)
        function = request.data.get("function", None)
        desc = request.data.get("desc", None)
        user_id = request.data.get("user_id", None)
        mid = request.data.get("mid", None)
        url = request.data.get("url", None)
        version = request.data.get("version", None)
        activate = request.data.get("activate", None)
        req_type = request.data.get("req_type", None)
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 201, "msg": "用户ID不存在！！！" }
            serializers = KgModelResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if mid is None:
            data['code'] = 201
            data['msg'] = '文档ID参数不能为空！！！'
            serializers = KgModelResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)

        tmpModel = KgModel.objects.get(id=mid)
        if desc:
            tmpModel.desc = desc
        if function:
            tmpModel.function = function
        
        if url:
            tmpModel.url = url

        if version:
            tmpModel.version = version
        
        if activate:
            tmpModel.activate = activate

        if name:
            tmpModel.name = name

        if req_type:
            tmpModel.req_type = req_type
        tmpModel.kg_user_id = tmpuser

        tmpModel.update_time = datetime.now()
        tmpModel.save()
        data = {"code": 200, "msg": "模型更新成功" }
        serializers = KgModelResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class ModelDelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgModelResponseSerializer

    @swagger_auto_schema(
        operation_description="模型删除",
        operation_summary="[可用] 模型删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mid'],
            properties={
                'mid': openapi.Schema(type=openapi.TYPE_STRING, description="模型ID"),
            },
        ),
        responses={
            200: KgModelResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['model']
    )
    @csrf_exempt
    def post(self, request):
        import platform
        data = {"code": 200 }

        mid = None
        if request.POST:
            mid = request.POST["mid"]
        if mid is None:
            mid = request.data["mid"]
        if mid is None:
            serializers = KgModelResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgModel.objects.get(id=mid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgModelResponseSerializer(data={"code": 200, "msg": "模型删除成功" }, many=False)
            else:
                serializers = KgModelResponseSerializer(data={"code": 201, "msg": "模型不存在" }, many=False)
        except:
            serializers = KgModelResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    




class KgModelParamList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgModelParamSerializer
    @swagger_auto_schema(
            operation_description='GET /modelapp/kgmodelparam/',
            operation_summary="获取所有模型参数列表",
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
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgModelParamResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['model'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        if keyword:
            querySet = KgModelParam.objects.filter(name__contains="{}".format(keyword))
        else:
            querySet = KgModelParam.objects.all()
        
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
        kds = KgModelParamSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgModelParamResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgModelParamListByModel(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgModelParamSerializer
    @swagger_auto_schema(
            operation_description='GET /modelapp/kgmodelparam/listbymodel',
            operation_summary="获取指定模型对应的参数列表",
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
                    "mid", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="模型ID", 
                    # 参数字符类型
                    type=openapi.TYPE_INTEGER
                ),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            ],
            responses={
                200: KgModelParamResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['model'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        mid = request.GET.get("mid", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        if mid is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少模型ID参数！！！'
            serializers = KgModelParamResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        try:
            tmpmodel = KgModel.objects.get(id=mid)
        except:
            data['code'] = 201
            data['msg'] = '该模型ID不存在！！！'
            serializers = KgModelParamResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        querySet = tmpmodel.kgmodelparam_set.all()
        if keyword:
            querySet = [q for q in querySet if keyword in q.name]
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
        kds = KgModelParamSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgModelParamResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class ModelParamAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True
    @swagger_auto_schema(
        operation_summary='[可用] 新增参数功能',
        operation_description='POST /modelapp/kgmodelparam/add',
        manual_parameters=[
           openapi.Parameter(
               name='mid',
               in_=openapi.IN_FORM,
               description='模型ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='name',
               in_=openapi.IN_FORM,
               description='参数名称',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='type',
               in_=openapi.IN_FORM,
               description='参数类型',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='desc',
               in_=openapi.IN_FORM,
               description='参数说明',
               type=openapi.TYPE_STRING
           ),
            openapi.Parameter(
                name='default',
                in_=openapi.IN_FORM,
                description='默认值',
                type=openapi.TYPE_STRING
            ),
           openapi.Parameter(
               name='necessary',
               in_=openapi.IN_FORM,
               description='必须 0|1',
               type=openapi.TYPE_STRING
           ),
        ],
        responses={
            200: KgModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['model']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        name = request.data.get("name", None)
        type = request.data.get("type", None)
        desc = request.data.get("desc", None)
        default = request.data.get("default", None)
        mid = request.data.get("mid", None)
        necessary = request.data.get("necessary", None)

        if mid is None or name is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgModelParamDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            try:
                tmpmodel = KgModel.objects.get(id=mid)
            except:
                data = {"code": 201, "msg": "模型ID不存在！！！" }
                serializers = KgModelParamDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
 
            tmpModelParma, tmpbool = KgModelParam.objects.get_or_create(name=name, type=type, kg_model_id=tmpmodel)
            if tmpbool:
                tmpno = len(KgModel.objects.all())
                tmpModelParma.name = name
                tmpModelParma.type = type
                tmpModelParma.desc = desc
                tmpModelParma.necessary = necessary
                tmpModelParma.activate = 0
                tmpModelParma.default = default
                tmpModelParma.create_time = datetime.now()
                tmpModelParma.update_time = datetime.now()
                # tmpModelParma.kg_model_id = tmpmodel
                tmpModelParma.save()
                data = {"code": 200, "msg": "参数创建成功" }
            else:
                data = {"code": 201, "msg": "该参数已存在~~~" }
            
            data['data'] = model_to_dict(tmpModelParma, exclude=[''])
            serializers = KgModelParamDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        

class ModelParamBatchAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True

    @swagger_auto_schema(
        operation_summary='[可用] 批量新增参数功能',
        operation_description='POST /modelapp/kgmodelparam/batchadd',
        manual_parameters=[
           openapi.Parameter(
               name='data',
               in_=openapi.IN_FORM,
               description='批量参数',
               type=openapi.TYPE_OBJECT
           ),
        ],
        responses={
            200: KgModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['model']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        reqdata = json.loads(request.data.get("data", {}))
        error_cnt = 0
        error_mid_cnt = 0
        succes_cnt = 0
        exist_cnt = 0
        if reqdata:
            values = reqdata['data']
            for ent in values:
                print("ent-->", ent)
                name = ent.get("name", None)
                type = ent.get("type", None)
                desc = ent.get("desc", None)
                default = ent.get("default", None)
                mid = ent.get("mid", None)
                necessary = ent.get("necessary", None)
                if mid is None:
                    error_mid_cnt=+1
                    continue
                try:
                    tmpmodel = KgModel.objects.get(id=mid)
                except:
                    error_mid_cnt+=1
                    continue

                if name is None or type is None:
                    error_cnt=+1
                tmpModelParma, tmpbool = KgModelParam.objects.get_or_create(name=name, type=type, kg_model_id=tmpmodel)
                if tmpbool:
                    tmpModelParma.name = name
                    tmpModelParma.type = type
                    tmpModelParma.desc = desc
                    tmpModelParma.necessary = necessary
                    tmpModelParma.activate = 0
                    tmpModelParma.default = default
                    tmpModelParma.create_time = datetime.now()
                    tmpModelParma.update_time = datetime.now()
                    # tmpModelParma.kg_model_id = tmpmodel
                    tmpModelParma.save()
                    succes_cnt+= 1
                else:
                    exist_cnt+=1
        # data['data'] = model_to_dict(tmpModelParma, exclude=[''])
        data['msg'] = f"成功添加{succes_cnt}, 已存在{exist_cnt}, 添加失败{error_cnt}, 模型ID错误 {error_mid_cnt}。"
        serializers = KgModelParamDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)

class ModelParamUpdateApiView(generics.GenericAPIView):
    # serializer_class = KgModelParamResponseSerializer

    parser_classes = (FormParser, MultiPartParser)

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True

    @swagger_auto_schema(
        operation_summary='[可用] 更新模型参数功能',
        operation_description='POST /modelapp/kgmodelparam/update/',
        manual_parameters=[
           openapi.Parameter(
               name='mid',
               in_=openapi.IN_FORM,
               description='模型ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='pid',
               in_=openapi.IN_FORM,
               description='参数ID',
               type=openapi.TYPE_INTEGER
           ),
           openapi.Parameter(
               name='name',
               in_=openapi.IN_FORM,
               description='参数名称',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='type',
               in_=openapi.IN_FORM,
               description='参数类型',
               type=openapi.TYPE_STRING
           ),
           openapi.Parameter(
               name='desc',
               in_=openapi.IN_FORM,
               description='参数说明',
               type=openapi.TYPE_STRING
           ),
            openapi.Parameter(
                name='default',
                in_=openapi.IN_FORM,
                description='默认值',
                type=openapi.TYPE_STRING
            ),
           openapi.Parameter(
               name='necessary',
               in_=openapi.IN_FORM,
               description='必须 0|1',
               type=openapi.TYPE_STRING
           ),
        ],
        responses={
            200: KgModelParamResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['model']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        name = request.data.get("name", None)
        type = request.data.get("type", None)
        desc = request.data.get("desc", None)
        default = request.data.get("default", None)
        mid = request.data.get("mid", None)
        pid = request.data.get("pid", None)
        necessary = request.data.get("necessary", None)

        if mid is None or pid is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgModelParamResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            try:
                tmpModelParma = KgModelParam.objects.get(id=pid)
                if name:
                    tmpModelParma.name = name
                
                if type:
                    tmpModelParma.type = type
                
                if desc:
                    tmpModelParma.desc = desc

                if default:
                    tmpModelParma.default = default

                if mid:
                    tmpmodel = KgModel.objects.get(id=mid)
                    tmpModelParma.kg_model_id = tmpmodel
                if necessary:
                    tmpModelParma.necessary = necessary
                tmpModelParma.update_time = datetime.now()
                tmpModelParma.save()
                data = {"code": 200, "msg": "参数创建成功" }
            except:
                data = {"code": 201, "msg": "模型ID不存在！！！" }
                serializers = KgModelParamResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            
            serializers = KgModelParamResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
class ModelParamBatchUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    
    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = BaseApiResponseSerializer
    swagger_fake_view = True

    @swagger_auto_schema(
        operation_summary='[可用] 批量新增参数功能',
        operation_description='POST /modelapp/kgmodelparam/batchupdate',
        manual_parameters=[
           openapi.Parameter(
               name='data',
               in_=openapi.IN_FORM,
               description='批量更新or新增参数',
               type=openapi.TYPE_OBJECT
           ),
        ],
        responses={
            200: KgModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags = ['model']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200 }
        # reqJson = json.loads(request.body.decode("utf-8"))
        print(request.data)
        # print(reqJson)
        reqdata = json.loads(request.data.get("data", {}))
        error_mid_cnt = 0
        add_succes_cnt = 0
        add_exist_cnt = 0
        update_succes_cnt = 0
        if reqdata:
            values = reqdata['data']
            for ent in values:
                pid = ent.get("pid", None)
                name = ent.get("name", None)
                type = ent.get("type", None)
                desc = ent.get("desc", None)
                default = ent.get("default", None)
                mid = ent.get("mid", None)
                activate = ent.get("activate", None)
                necessary = ent.get("necessary", None)
                if mid is None:
                    error_mid_cnt=+1
                    continue
                try:
                    tmpmodel = KgModel.objects.get(id=mid)
                except:
                    error_mid_cnt+=1
                    continue
                ### 存在pid
                if pid:
                    tmpModelParma = KgModelParam.objects.get(id=pid)
                    if tmpModelParma:
                        if name:
                            tmpModelParma.name = name
                        if type:
                            tmpModelParma.type = type
                        if desc:
                            tmpModelParma.desc = desc
                        if default is not None:
                            tmpModelParma.default = default
                        if necessary:
                            tmpModelParma.necessary = necessary
                        if activate:
                            tmpModelParma.activate = activate
                        tmpModelParma.save()
                        update_succes_cnt+=1
                        continue
                if name is None or type is None:
                    error_cnt=+1
                tmpModelParma, tmpbool = KgModelParam.objects.get_or_create(name=name, type=type, kg_model_id=tmpmodel)
                if tmpbool:
                    tmpModelParma.name = name
                    tmpModelParma.type = type
                    tmpModelParma.desc = desc
                    tmpModelParma.necessary = necessary
                    tmpModelParma.activate = 0
                    tmpModelParma.create_time = datetime.now()
                    tmpModelParma.update_time = datetime.now()
                    tmpModelParma.kg_model_id = tmpmodel
                    tmpModelParma.save()
                    add_succes_cnt+= 1
                else:
                    add_exist_cnt+=1
        # data['data'] = model_to_dict(tmpModelParma, exclude=[''])
        data['msg'] = f"成功添加{add_succes_cnt}, 更新{update_succes_cnt}个参数"
        serializers = KgModelParamDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
        
class ModelParamDeleteApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgModelParamResponseSerializer

    @swagger_auto_schema(
        operation_description="模型参数删除",
        operation_summary="[可用] 模型参数删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['pid'],
            properties={
                'pid': openapi.Schema(type=openapi.TYPE_STRING, description="模型参数ID"),
            },
        ),
        responses={
            200: KgModelParamResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['model']
    )
    @csrf_exempt
    def post(self, request):
        data = {"code": 200 }
        pid = request.data["pid"]
        if pid is None:
            serializers = KgModelParamResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgModelParam.objects.get(id=pid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgModelParamResponseSerializer(data={"code": 200, "msg": "模型参数删除成功" }, many=False)
            else:
                serializers = KgModelParamResponseSerializer(data={"code": 201, "msg": "模型参数不存在" }, many=False)
        except:
            serializers = KgModelParamResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    


class ModelParamDetailApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = KgModelParamResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /modelapp/kgmodelparam/detail/',
            operation_summary="获取单个模型参数详情",
            # 接口参数 GET请求参数
            manual_parameters=[
                # 声明参数
                openapi.Parameter(
                    #参数名称
                    "pid", 
                    # 参数类型为query
                    openapi.IN_QUERY, 
                    # 参数描述
                    description="模型ID", 
                    # 参数字符类型
                    type=openapi.TYPE_INTEGER
                ),
            ],
            responses={
                200: KgModelParamDetailResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['model'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        pid = request.GET.get("pid", None)
        if pid:
            try:
                tmpparam = KgModelParam.objects.get(id=pid)
                data['data'] = model_to_dict(tmpparam, exclude=[''])
                serializers = KgModelParamDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgModelParamDetailResponseSerializer(data={"code": 201, "msg": "不存在该模型参数"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)

        serializers = KgModelParamDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)