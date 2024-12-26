import random
import string
from uuid import uuid4
from django.shortcuts import render
import json
import pprint
import time
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.db.models import Count
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
from hydapp.serializer import BaseApiResponseSerializer
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.forms.models import model_to_dict
from django.db.models import Q  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from rest_framework.authentication import BasicAuthentication
import PIL
from PIL import ImageDraw, ImageFont, ImageFilter  
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os, io
from django.core.cache import cache  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from hydapp.models import *

# Create your views here.
class BaseApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='GET ///',
        operation_summary="GET",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "data": {}}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)
    

class BaseApiPost(generics.GenericAPIView):
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_summary='POST',
        operation_description='POST ///',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sid'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID"),
            },
        ),
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        xid = request.data.get("id", None)
        data = {"code": 200, "data": {}, "msg": "success"}
        serializers = BaseApiResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class FutureHDApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='未来河道水情',
        operation_summary="未来河道水情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('stcd', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        print("FutureHDApiGet:", request.GET)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        stcd = request.GET.get("stcd", None)
        start_time = request.GET.get("start_time", datetime.now().strftime("%Y-%m-%d"))
        end_time = request.GET.get("end_time", None)
        if end_time is None or stcd is None:
            bars = BaseApiResponseSerializer(data={"code": 201, "msg": "param error", "success": False}, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        
        objs = FutureHeDaoData.objects.filter(date__gte=start_time, date__lte=end_time, stcd=stcd).all()
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "result": [model_to_dict(obj, exclude=["sw_pk"]) for obj in objs]}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)


class SKListApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='水库列表',
        operation_summary="水库列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        print("FutureSKApiGet:", request.GET)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        objs = ShuiKu.objects.all()
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "result": [model_to_dict(obj) for obj in objs]}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)



class HDListApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='河道列表',
        operation_summary="河道列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        print("HDListApiGet:", request.GET)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        objs = ShuiWen.objects.all()
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "result": [model_to_dict(obj) for obj in objs]}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)


class FutureSKApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='未来水库水情',
        operation_summary="未来水库水情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('stcd', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        print("FutureSKApiGet:", request.GET)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        stcd = request.GET.get("stcd", None)
        start_time = request.GET.get("start_time", datetime.now().strftime("%Y-%m-%d"))
        end_time = request.GET.get("end_time", None)
        if end_time is None or stcd is None:
            bars = BaseApiResponseSerializer(data={"code": 201, "msg": "param error", "success": False}, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        
        objs = FutureShuiKuData.objects.filter(date__gte=start_time, date__lte=end_time, stcd=stcd).all()
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "result": [model_to_dict(obj, exclude=["sw_pk"]) for obj in objs]}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)
    


class RealHDApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='实时河道水情',
        operation_summary="实时河道水情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('stcd', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        print("RealHDApiGet:", request.GET)
        stcd = request.GET.get("stcd", None)
        if stcd is None:
            bars = BaseApiResponseSerializer(data={"code": 201, "msg": "param error", "success": False}, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        
        realtime = datetime.now().strftime("%Y-%m-%d")
        obj = HeDaoData.objects.filter(stcd=stcd).order_by('-date').first()
        if obj is None:
            bars = BaseApiResponseSerializer(data={"code": 201, "msg": "not found", "success": False}, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "data": model_to_dict(obj, exclude=["sw_pk"])}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)


class RealSKApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = BaseApiResponseSerializer

    @swagger_auto_schema(
        operation_description='实时水库水情',
        operation_summary="实时水库水情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('stcd', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={
            200: BaseApiResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['hydapi'])
    def get(self, request, *args, **kwargs):

        print("RealSKApiGet:", request.GET)
        stcd = request.GET.get("stcd", None)
        if stcd is None:
            bars = BaseApiResponseSerializer(data={"code": 201, "msg": "param error", "success": False}, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        
        realtime = datetime.now().strftime("%Y-%m-%d")
        obj = ShuiKuData.objects.filter(stcd=stcd).order_by('-date').first()
        if obj is None:
            bars = BaseApiResponseSerializer(data={"code": 201, "msg": "not found", "success": False}, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        bars = BaseApiResponseSerializer(data={"code": 200, "msg": "success", "data": model_to_dict(obj, exclude=['sk_pk'])}, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)
    