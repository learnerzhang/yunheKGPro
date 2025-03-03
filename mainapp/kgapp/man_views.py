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

from apiapp.serializers import KgAPIResponseSerializer
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
"""
    知识干预相关接口
"""

import requests
class KgQAList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgQAResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /kgapp/prodqalist/',
            operation_summary="获取入库QA列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('cid', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='目录ID',),
                openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间',),
                openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间',),
            ],
            responses={
                200: KgQAResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['artifi'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        cid = request.GET.get("cid", None)
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        querySet = KgQA.objects
        if cid is not None:
            tmpdocs = KgDoc.objects.filter(kg_table_content_id__id="{}".format(cid)).all()
            docids= [d.id for d in tmpdocs]
            querySet = querySet.filter(doc_id__in=docids)
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(question__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(create_time__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(create_time__lt="{}".format(end_time))
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
        
        kds = KgQASerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgQAResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgQAUpdateApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    serializer_class = KgQADetailResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
            operation_description='GET /kgapp/prodqalist/update',
            operation_summary="更新QA",

            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['tag_id'],
                properties={
                    'qid': openapi.Schema(type=openapi.TYPE_INTEGER, description="问题ID"),
                    'question': openapi.Schema(type=openapi.TYPE_STRING, description="问题"),
                    'answer': openapi.Schema(type=openapi.TYPE_STRING, description="答案"),
                },
            ),
            tags = ['artifi'])
    
    def post(self, request, *args, **kwargs):
        qid = request.data.get('qid', None)
        question = request.data.get('question', None)
        answer = request.data.get('answer', None)
        if qid is None:
            serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "问题ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        if question or answer:
            try:
                tmpqa = KgQA.objects.get(id=qid)
                if question:
                    tmpqa.question = question
                if answer:
                    tmpqa.answer = answer
                tmpqa.save()
                serializers = KgQADetailResponseSerializer(data={"code": 200, "msg": "问题更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "问题不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgQASynToLLMApiView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    serializer_class = KgAPIResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/prodqalist/synToLLM',
        operation_summary="同步问答对到大模型QA",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[''],
            properties={
                'qidlist': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_INTEGER), description="问题ID列表"),
            },
        ),
        tags=['artifi'])
    def post(self, request, *args, **kwargs):
        qidlist = request.data.get('qidlist', None)
        tmpqalist = KgQA.objects.filter(id__in=qidlist)
        headers = {
            'Content-Type': 'application/json'
        }
        params = []
        for tmqqa in tmpqalist:
            params.append({
                "text_url": tmqqa.doc_id.filepath,
                "text_tag": tmqqa.doc_id.tagstr,
                "text_name": tmqqa.doc,
                "question": tmqqa.question,
                "answer": tmqqa.answer
            })
        try:
            response = requests.request("POST", "http://10.4.145.209:8000/qa/QA_on_migration/", headers=headers, data=json.dumps(params), timeout=60000)
            data = {"code": 200, "msg": "执行成功", "data": response.json()}
        except:
            data = {"code": 201, "msg": "远程接口异常"}

        serializers = KgAPIResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgQADelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgQADetailResponseSerializer
    @swagger_auto_schema(
        operation_description="问题删除",
        operation_summary="[可用] 问题删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="问题ID"),
            },
        ),
        responses={
            200: KgQADetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['artifi']
    )
    @csrf_exempt
    def post(self, request):
        qid = request.data["id"]
        if qid is None:
            serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgQA.objects.get(id=qid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgQADetailResponseSerializer(data={"code": 200, "msg": "问题删除成功" }, many=False)
            else:
                serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "问题不存在" }, many=False)
        except:
            serializers = KgQADetailResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class KgQABatchDelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgQADetailResponseSerializer

    @swagger_auto_schema(
        operation_description="问题批量删除",
        operation_summary="[可用] 批量删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['idstr'],
            properties={
                'idstr': openapi.Schema(type=openapi.TYPE_STRING, description="问题IDStr"),
            },
        ),
        responses={
            200: KgQADetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['artifi']
    )
    @csrf_exempt
    def post(self, request):
        idstr = request.data["idstr"]
        if idstr is None:
            serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            qids = str(idstr).split(",")
            KgQA.objects.filter(id__in=qids).delete()
            serializers = KgQADetailResponseSerializer(data={"code": 200, "msg": "问题删除成功" }, many=False)
        except:
            serializers = KgQADetailResponseSerializer(data={"code": 202, "msg": "系统错误" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgQAUpdateApiView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    serializer_class = KgQADetailResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/prodqalist/update',
        operation_summary="更新QA",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['tag_id'],
            properties={
                'qid': openapi.Schema(type=openapi.TYPE_INTEGER, description="问题ID"),
                'question': openapi.Schema(type=openapi.TYPE_STRING, description="问题"),
                'answer': openapi.Schema(type=openapi.TYPE_STRING, description="答案"),
            },
        ),
        tags=['artifi'])
    def post(self, request, *args, **kwargs):
        qid = request.data.get('qid', None)
        question = request.data.get('question', None)
        answer = request.data.get('answer', None)
        if qid is None:
            serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "问题ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if question or answer:
            try:
                tmpqa = KgQA.objects.get(id=qid)
                if question:
                    tmpqa.question = question
                if answer:
                    tmpqa.answer = answer
                tmpqa.save()
                serializers = KgQADetailResponseSerializer(data={"code": 200, "msg": "问题更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "问题不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
        serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgAutoQAApiView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    serializer_class = KgQADetailResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/prodqalist/autoQA',
        operation_summary="问答对话QA",

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['question'],
            properties={
                'question': openapi.Schema(type=openapi.TYPE_STRING, description="问题"),
            },
        ),
        tags=['artifi'])
    def post(self, request, *args, **kwargs):
        question = request.data.get('question', None)
        if question is None:
            serializers = KgQADetailResponseSerializer(data={"code": 201, "msg": "问题不能为空"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        data = {"code": 200}

        objs = KgQA.objects.filter(question__contains=question).all()
        kds = KgQASerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgQAResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgRecomQuestApiView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    serializer_class = KgQAResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /prodqalist/recomQuest',
        operation_summary="推荐N条问题,默认10条",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('num', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgQAResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['artifi'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        num = int(request.data.get('num', 10))
        objs = KgQA.objects.order_by('?')[:num]
        kds = KgQASerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgQAResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)