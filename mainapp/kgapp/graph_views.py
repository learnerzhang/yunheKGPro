import json
import pprint
import time
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response

from apiapp.serializers import BaseApiResponseSerializer
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

"""
    知识图谱相关接口
"""

import requests


class KgRelationSchemeList(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    serializer_class = KgEntiySchemeResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphRelationScheme/',
        operation_summary="获取关系列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
        ],
        responses={
            200: KgRelationSchemeResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        querySet = KgRelationScheme.objects
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(name__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lt="{}".format(end_time))
        querySet = querySet.all().order_by('-updated_at')

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

        kds = KgRelationSchemeSerializer(data=objs, many=True)
        kds.is_valid()

        data['data'] = kds.data
        serializers = KgRelationSchemeResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgRelationSchemeAddApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgRelationSchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新建关系名称',
        operation_description='POST /kgapp/graphRelationScheme/add',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="关系名称"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="关系描述"),
            },
        ),
        responses={
            200: KgRelationSchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        name = request.data.get("name", None)
        desc = request.data.get("desc", "")
        if name is not None:
            tmprel, tmpbool = KgRelationScheme.objects.get_or_create(name=name)
            if tmpbool:
                tmprel.desc = desc
                tmprel.created_at = datetime.now()
                tmprel.updated_at = datetime.now()
                tmprel.save()
                data = {"code": 200, "msg": "新建关系成功"}
            else:
                data = {"code": 201, "msg": "关系名称已经存在！"}
        else:
            data = {"code": 201, "msg": "参数错误"}
        data['data'] = model_to_dict(tmprel, exclude=[''])
        serializers = KgRelationSchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgRelationSchemeUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgRelationSchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 更新关系',
        operation_description='POST /kgapp/graphRelationScheme/update',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sid'],
            properties={
                'rid': openapi.Schema(type=openapi.TYPE_INTEGER, description="关系ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="关系名称"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="关系描述"),
            },
        ),
        responses={
            200: KgRelationSchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        rid = request.data.get("rid", None)
        name = request.data.get("name", None)
        desc = request.data.get("desc", None)
        try:
            tmpent = KgRelationScheme.objects.get(id=rid)
        except:
            data = {"code": 201, "msg": "关系ID参数错误"}
            serializers = KgRelationSchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if name is not None:
            tmpent.name = name

        if desc is not None:
            tmpent.desc = desc

        tmpent.save()
        data = {"code": 200, "msg": "关系名称更新成功"}
        serializers = KgRelationSchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgRelationSchemeDeleteApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgRelationSchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 删除关系',
        operation_description='POST /kgapp/graphRelationScheme/delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sid'],
            properties={
                'rid': openapi.Schema(type=openapi.TYPE_INTEGER, description="关系ID"),
            },
        ),
        responses={
            200: KgRelationSchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        rid = request.data.get("rid", None)

        try:
            tmpent = KgRelationScheme.objects.get(id=rid)
            tmpent.delete()
        except:
            data = {"code": 201, "msg": "关系ID参数错误"}
            serializers = KgRelationSchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        data = {"code": 200, "msg": "关系删除成功...."}
        serializers = KgRelationSchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgRelationSchemeDetailApiView(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    generics.GenericAPIView):
    serializer_class = KgRelationSchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphRelationScheme/detail',
        operation_summary="获取实体详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgRelationSchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        tmpid = request.GET.get("id", None)
        if tmpid:
            try:
                tmp = KgRelationScheme.objects.get(id=tmpid)
                data['data'] = model_to_dict(tmp, exclude=[''])
                serializers = KgRelationSchemeDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgRelationSchemeDetailResponseSerializer(data={"code": 201, "msg": "不存在该关系"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgRelationSchemeDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = KgEntiySchemeResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphEntityScheme/',
        operation_summary="获取实体列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
        ],
        responses={
            200: KgEntiySchemeResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        taskId = request.GET.get("taskId", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        querySet = KgEntityScheme.objects

        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(name__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lt="{}".format(end_time))
        if taskId is not None:
            try:
                tmpTask = KgProductTask.objects.get(id=taskId)
                types = list(set([e.type for e in KgEntity.objects.filter(task=tmpTask).all()]))
                querySet = querySet.filter(name__in=types)
            except:
                data['code'] = 201
                data['msg'] = "当前生产任务不存在..."
                serializers = KgEntiySchemeResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        querySet = querySet.all().order_by('-updated_at')
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

        kds = KgEntitySchemeSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgEntiySchemeResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 更新实体',
        operation_description='POST /kgapp/graphEntityScheme/update',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sid'],
            properties={
                'sid': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="属性名称"),
                'color': openapi.Schema(type=openapi.TYPE_STRING, description="属性颜色"),
                'size': openapi.Schema(type=openapi.TYPE_INTEGER, description="节点大小"),
            },
        ),
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        sid = request.data.get("sid", None)
        name = request.data.get("name", None)
        color = request.data.get("color", None)
        size = request.data.get("size", None)

        try:
            tmpent = KgEntityScheme.objects.get(id=sid)
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if name is not None:
            tmpent.name = name

        if color is not None:
            tmpent.color = color

        if size is not None:
            tmpent.size = size
        tmpent.updated_at = datetime.now()
        tmpent.save()
        data = {"code": 200, "msg": "实体属性更新成功"}

        serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeDeleteApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 删除实体',
        operation_description='POST /kgapp/graphEntityScheme/delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sid'],
            properties={
                'sid': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
            },
        ),
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        sid = request.data.get("sid", None)

        try:
            tmpent = KgEntityScheme.objects.get(id=sid)
            tmpent.delete()
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        data = {"code": 200, "msg": "实体删除成功...."}
        serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeAddApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新建实体名称',
        operation_description='POST /kgapp/graphEntityScheme/add',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="实体名称"),
            },
        ),
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        name = request.data.get("name", None)
        if name is not None:
            tmpent, tmpbool = KgEntityScheme.objects.get_or_create(name=name)
            if tmpbool:
                tmpent.created_at = datetime.now()
                tmpent.updated_at = datetime.now()
                tmpent.save()
                data = {"code": 200, "msg": "新建实体成功"}
            else:
                data = {"code": 201, "msg": "实体名称已经存在！"}
        else:
            data = {"code": 201, "msg": "参数错误"}
        data['data'] = model_to_dict(tmpent, exclude=['attrs'])
        data['data']['attlist'] = tmpent.attlist
        serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeDetailApiView(mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  generics.GenericAPIView):
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphEntityScheme/detail',
        operation_summary="获取实体详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        tmpid = request.GET.get("id", None)
        if tmpid:
            try:
                tmp = KgEntityScheme.objects.get(id=tmpid)
                data['data'] = model_to_dict(tmp, exclude=['attrs'])
                data['data']['attlist'] = tmp.attlist
                serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgEntitySchemeDetailResponseSerializer(data={"code": 201, "msg": "不存在该实体"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgEntitySchemeDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeAddAttrApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新建实体属性',
        operation_description='POST /kgapp/graphEntityScheme/addattr',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['esid'],
            properties={
                'esid': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="属性名称"),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description="属性类型"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="属性描述"),
                'multi_flag': openapi.Schema(type=openapi.TYPE_INTEGER, description="单|多值"),
            },
        ),
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        data = {"code": 200}
        esid = request.data.get("esid", None)
        name = request.data.get("name", None)
        type = request.data.get("type", None)
        desc = request.data.get("desc", None)
        multi_flag = request.data.get("multi_flag", 0)

        try:
            tmpent = KgEntityScheme.objects.get(id=esid)
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if name is not None and type is not None:
            tmpentAttr = KgEntityAttrScheme()
            tmpentAttr.attname = name
            tmpentAttr.attmulti = multi_flag
            tmpentAttr.atttype = type
            tmpentAttr.attdesc = desc
            tmpentAttr.created_at = datetime.now()
            tmpentAttr.updated_at = datetime.now()
            tmpentAttr.save()
            tmpent.attrs.add(tmpentAttr)
            # tmpent.attrs.remove(tmpentAttr)
            tmpent.save()
            data = {"code": 200, "msg": "新建实体属性成功"}
        else:
            data = {"code": 201, "msg": "新建实体成功"}

        serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeUpdateAttrApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新建实体属性',
        operation_description='POST /kgapp/graphEntityScheme/updateattr',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['esid'],
            properties={
                'esid': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
                'esaid': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体属性ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="属性名称"),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description="属性类型"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="属性描述"),
                'multi_flag': openapi.Schema(type=openapi.TYPE_INTEGER, description="单|多值"),
            },
        ),
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        data = {"code": 200}
        esid = request.data.get("esid", None)
        esaid = request.data.get("esaid", None)
        name = request.data.get("name", None)
        type = request.data.get("type", None)
        desc = request.data.get("desc", None)
        multi_flag = request.data.get("multi_flag", None)

        try:
            tmpent = KgEntityScheme.objects.get(id=esid)
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpattent = KgEntityAttrScheme.objects.get(id=esaid)
        except:
            data = {"code": 201, "msg": "实体属性ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if name is not None:
            tmpattent.attname = name

        if type is not None:
            tmpattent.atttype = type

        if desc is not None:
            tmpattent.attdesc = desc

        if multi_flag is not None:
            tmpattent.attmulti = int(multi_flag)

        tmpattent.updated_at = datetime.now()
        tmpattent.save()
        tmpent.attrs.add(tmpattent)
        tmpent.save()
        data = {"code": 200, "msg": "新建实体属性更新成功"}
        serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntitySchemeDelAttrApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntitySchemeDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 删除实体属性',
        operation_description='POST /kgapp/graphEntityScheme/delattr',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['esid'],
            properties={
                'esid': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
                'esaid': openapi.Schema(type=openapi.TYPE_INTEGER, description="属性ID"),
            },
        ),
        responses={
            200: KgEntitySchemeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        data = {"code": 200}
        esid = request.data.get("esid", None)
        esaid = request.data.get("esaid", None)
        try:
            tmpent = KgEntityScheme.objects.get(id=esid)
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        try:
            tmpattent = KgEntityAttrScheme.objects.get(id=esaid)
        except:
            data = {"code": 201, "msg": "实体属性ID参数错误"}
            serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        tmpent.attrs.remove(tmpattent)
        tmpent.save()
        data = {"code": 200, "msg": "实体属性删除成功！"}
        serializers = KgEntitySchemeDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityByTypeList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = KgEntiyResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphEntityByTypeList/',
        operation_summary="获取实体卡片列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='实体类型'),
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='任务ID'),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
        ],
        responses={
            200: KgEntiyResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        taskId = request.GET.get("taskId", None)
        type = request.GET.get("type", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        querySet = KgEntity.objects

        if taskId is not None:
            tmpTask = KgProductTask.objects.get(id=taskId)
            querySet = querySet.filter(task=tmpTask)
        if type is not None and len(type) > 0:
            querySet = querySet.filter(type="{}".format(type))
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(name__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lt="{}".format(end_time))

        querySet = querySet.all().order_by('-updated_at')
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

        kds = KgEntitySerializer(data=objs, many=True)
        kds.is_valid()

        data['data'] = kds.data
        serializers = KgEntiyResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityDetailApiView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    serializer_class = KgEntityDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphEntity/detail',
        operation_summary="获取实体详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgEntityDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        tmpid = request.GET.get("id", None)

        if tmpid:
            try:
                tmp = KgEntity.objects.get(id=tmpid)
            except:
                serializers = KgEntityDetailResponseSerializer(data={"code": 201, "msg": "不存在该实体"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            data['data'] = model_to_dict(tmp, exclude=['atts', 'tags'])
            data['data']['attlist'] = tmp.attlist
            data['data']['taglist'] = tmp.taglist
            data['data']['tagliststr'] = tmp.tagliststr
            data['data']['relations'] = tmp.relations
            serializers = KgEntityDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgEntityDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityDetailByNameTypeApiView(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      generics.GenericAPIView):
    serializer_class = KgEntityDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphEntity/detailByNameType',
        operation_summary="获取实体详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={
            200: KgEntityDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        name = request.GET.get("name", None)
        type = request.GET.get("type", None)
        taskId = request.GET.get("taskId", None)

        if name is not None and type is not None and taskId is not None:
            try:
                tmpTask = KgProductTask.objects.get(id=taskId)
                tmp = KgEntity.objects.filter(name=name, type=type, task=tmpTask).first()
                data['data'] = model_to_dict(tmp, exclude=['atts', 'tags'])
                data['data']['attlist'] = tmp.attlist
                data['data']['taglist'] = tmp.taglist
                data['data']['tagliststr'] = tmp.tagliststr
                data['data']['relations'] = tmp.relations
                data['data']['groupRelations'] = tmp.groupRelations
                serializers = KgEntityDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgEntityDetailResponseSerializer(data={"code": 201, "msg": "不存在该实体"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgEntityDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntityDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 更新实体名称',
        operation_description='POST /kgapp/graphEntity/update',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="实体名称"),
                'attrs': openapi.Schema(type=openapi.TYPE_OBJECT, description="属性对"),
            },
        ),
        responses={
            200: KgEntityDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        eid = request.data.get("id", None)
        name = request.data.get("name", None)
        attrs = request.data.get("attrs", {})
        try:
            tmpent = KgEntity.objects.get(id=eid)
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntityDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if name is not None:
            tmpent.name = name
            tmpent.save()
        if attrs:
            tmpent.atts.clear()
            for attK, attV in dict(attrs).items():
                tka, tkb = KgEntityAtt.objects.get_or_create(attname=attK, atttvalue=attV)
                if tkb:
                    tka.updated_at = datetime.now()
                    tka.created_at = datetime.now()
                    tka.save()
                tmpent.atts.add(tka)
        tmpent.updated_at = datetime.now()
        tmpent.save()
        data = {"code": 200, "msg": "实体更新成功!"}
        serializers = KgEntityDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityDeleteApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntityDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 删除实体',
        operation_description='POST /kgapp/graphEntity/delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
            },
        ),
        responses={
            200: KgEntityDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        sid = request.data.get("id", None)
        neo_client = None
        try:
            neo_client = Neo4j()
        except:
            print("neo4j 客户端连接出错...")
            pass

        try:
            # 获取实体节点
            tmpent = KgEntity.objects.get(id=sid)
            # 删除关联关系
            try:
                neo_client.delNodeAndRelation(name=tmpent.name, node_type=tmpent.type)
            except:
                pass
            KgRelation.objects.filter(from_nodeid=sid).all().delete()
            KgRelation.objects.filter(to_nodeid=sid).all().delete()
            # 删除属性值
            tmpent.attrs.clear()
            tmpent.delete()
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntityDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        data = {"code": 200, "msg": "实体删除成功...."}
        serializers = KgEntityDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityUpdateAttrApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgEntityDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 更新实体',
        operation_description='POST /kgapp/graphEntity/update',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['esid'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="实体ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="实体名称"),
                'attrs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_STRING),
                                        description="属性值 => [{'id': 'xx', 'name': 'xx', 'value': 'xxx'}, ]"),
            },
        ),
        responses={
            200: KgEntityDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        eid = request.data.get("id", None)
        name = request.data.get("name", None)
        attrs = request.data.get("attrs", [])

        neo_client = None
        try:
            neo_client = Neo4j()
        except:
            print("neo4j 客户端连接出错...")
            pass

        try:
            tmpent = KgEntity.objects.get(id=eid)
        except:
            data = {"code": 201, "msg": "实体ID参数错误"}
            serializers = KgEntityDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if name is not None:
            tmpent.name = name
            try:
                neo_client.reNameNodeByName(oldname=tmpent.name, oldtype=tmpent.type, name=name)
            except:
                print("Neo4j 操作异常")

        tmpent.updated_at = datetime.now()
        tmpent.save()

        cnt = 0
        for att in attrs:
            aid = att['id']
            name = att['name'] if 'name' in att else None
            val = att['value'] if 'value' in att else None
            try:
                tmpatt = KgEntityAtt.objects.get(id=aid)
                if name is not None:
                    tmpatt.atttvalue = val
                if val is not None:
                    tmpatt.attname = name
                tmpatt.updated_at = datetime.now()
                tmpatt.save()
                cnt += 1
            except:
                pass
        data = {"code": 200, "msg": f"实体更新成功, 修改属性{cnt}个"}
        serializers = KgEntityDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityApiView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    serializer_class = KgGraphResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graph',
        operation_summary="获取图谱详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('total', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgGraphResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        total = int(request.GET.get("total", 100))
        total = 300 if total > 300 else total
        taskId = request.GET.get("taskId", None)
        neo_client = None
        try:
            neo_client = Neo4j()
        except:
            print("neo4j 客户端连接出错...")
            pass
        nodes, links, categories = [], [], []
        try:
            totalLinkNum = neo_client.totalLinkNum(task_id=taskId)[0]['COUNT']
            totalNodeNum = neo_client.totalNodeNum(task_id=taskId)[0]['COUNT']
            entityLabels = neo_client.entityLabels()

            type2color = {kes.name: kes.color for kes in KgEntityScheme.objects.all()}
            type2size = {kes.name: kes.size for kes in KgEntityScheme.objects.all()}
            categories = [{"name": ent['label'],
                           "color": type2color[ent['label']] if ent['label'] in type2color else '#9AA1AC',
                           "size": type2size[ent['label']] if ent['label'] in type2size else 60} for ent in
                          entityLabels]

            results = neo_client.indexRelationship(total=total, task_id=taskId)
            node_used = set()
            for record in results:
                # print("record:", record)

                p_label = list(record['p'].labels)[0]
                q_label = list(record['q'].labels)[0]
                p_node_id = record['p'].identity

                if 'name' in record['q']:
                    q_name = record['q']['name']
                else:
                    for k in record['q']:
                        q_name = record['q'][k]

                if 'name' in record['p']:
                    p_name = record['p']['name']
                else:
                    for k in record['p']:
                        p_name = record['p'][k]
                q_node_id = record['q'].identity
                rel_name = type(record['r']).__name__
                rel_id = record['r'].identity
                if p_name not in node_used:
                    nodes.append({'category': p_label, 'name': p_name, 'nodeid': p_node_id})
                    node_used.add(p_name)
                if q_name not in node_used:
                    nodes.append({'category': q_label, 'name': q_name, 'nodeid': q_node_id})
                    node_used.add(q_name)
                links.append(
                    {'source': p_node_id, 'target': q_node_id, 'value': rel_name, 'name': rel_name, "id": rel_id})
        except:
            print("Graph 操作异常")
            pass
        data['nodes'] = nodes
        data['links'] = links
        data['categories'] = categories
        data['nodeNum'] = len(nodes)
        data['linkNnum'] = len(links)
        serializers = KgGraphResponseSerializer(
            data={"nodeNum": len(nodes), "linkNnum": len(links), "totalNodeNum": totalNodeNum,
                  "totalLinkNum": totalLinkNum,
                  "nodes": nodes, "links": links, "categories": categories}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgEntityExpandApiView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    serializer_class = KgGraphResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/graphExpand',
        operation_summary="获取图谱点扩展",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('taskId', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgGraphResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        entity_name = request.GET.get("name", None)
        entity_type = request.GET.get("type", None)
        taskId = request.GET.get("taskId", None)
        neo_client = None
        try:
            neo_client = Neo4j()
        except:
            print("neo4j 客户端连接出错...")
            pass
        nodes, links = [], []
        try:
            totalLinkNum = neo_client.totalLinkNum(task_id=taskId)[0]['COUNT']
            totalNodeNum = neo_client.totalNodeNum(task_id=taskId)[0]['COUNT']
            entityLabels = neo_client.entityLabels()
            type2color = {kes.name: kes.color for kes in KgEntityScheme.objects.all()}
            type2size = {kes.name: kes.size for kes in KgEntityScheme.objects.all()}
            categories = [{"name": ent['label'],
                           "color": type2color[ent['label']] if ent['label'] in type2color else '#9AA1AC',
                           "size": type2size[ent['label']] if ent['label'] in type2size else 60} for ent in
                          entityLabels]
            results = neo_client.fullLeftLinkEntity(value=entity_name, entityType=entity_type, task_id=taskId)
            node_used = set()
            for record in results:
                # print("record:", record)
                p_label = list(record['p'].labels)[0]
                q_label = list(record['q'].labels)[0]
                p_node_id = record['p'].identity

                if 'name' in record['q']:
                    q_name = record['q']['name']
                else:
                    for k in record['q']:
                        q_name = record['q'][k]

                if 'name' in record['p']:
                    p_name = record['p']['name']
                else:
                    for k in record['p']:
                        p_name = record['p'][k]
                q_node_id = record['q'].identity
                rel_name = type(record['r']).__name__
                rel_id = record['r'].identity
                if p_name not in node_used:
                    nodes.append({'category': p_label, 'name': p_name, 'nodeid': p_node_id})
                    node_used.add(p_name)
                if q_name not in node_used:
                    nodes.append({'category': q_label, 'name': q_name, 'nodeid': q_node_id})
                    node_used.add(q_name)
                links.append(
                    {'source': p_node_id, 'target': q_node_id, 'value': rel_name, 'name': rel_name, "id": rel_id})
        except:
            print("Graph 操作异常")
            pass
        data['nodes'] = nodes
        data['links'] = links
        data['categories'] = categories
        data['nodeNum'] = len(nodes)
        data['linkNnum'] = len(links)
        serializers = KgGraphResponseSerializer(
            data={"nodeNum": len(nodes), "linkNnum": len(links), "totalNodeNum": totalNodeNum,
                  "totalLinkNum": totalLinkNum,
                  "nodes": nodes, "links": links, "categories": categories}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgClearGraphApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgGraphResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 清空实体&关系&neo4j',
        operation_description='POST /kgapp/clearGraph',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
            },
        ),
        responses={
            200: KgEntityDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['graph']
    )
    def post(self, request):
        neo_client = None
        try:
            neo_client = Neo4j()
        except:
            print("neo4j 客户端连接出错...")
            pass
        try:
            # 获取实体节点
            KgEntityAtt.objects.all().delete()
            KgEntity.objects.all().delete()
            KgRelation.objects.all().delete()
            try:
                neo_client.deleteAll()
            except:
                pass
            # 删除属性值
        except:
            data = {"code": 201, "msg": "删除操作异常"}
            serializers = KgGraphResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        data = {"code": 200, "msg": "删库跑路成功！慎重执行"}
        serializers = KgGraphResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)

