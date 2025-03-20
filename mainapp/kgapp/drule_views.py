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
from kgapp.base_enum import AttributeValueTypeEnum, RuleContentConnectEnum, RuleContentConnectList, RuleContentJudgeTypeEnum, RuleContentJudgeTypeList, RuleContentOperatorList, RuleContentTypeEnum
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
    调度规则相关接口
"""
import requests
# class KgDDActionList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
    
#     serializer_class = KgDDActionResponseSerializer
#     @swagger_auto_schema(
#             operation_description='GET /ddrule/actionlist/',
#             operation_summary="获取调度规则目标列表",
#             # 接口参数 GET请求参数
#             manual_parameters=[
#                 openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#                 openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
#                 openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
#                 openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间',),
#                 openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间',),
#             ],
#             responses={
#                 200: KgDDActionResponseSerializer(many=False),
#                 400: "请求失败",
#             },
#             tags = ['ddrule'])
#     def get(self, request, *args, **kwargs):

#         data = {"code": 200}
#         keyword = request.GET.get("keyword", None)
#         page = request.GET.get("page", 1)
#         pageSize = request.GET.get("pageSize", 10)
#         start_time = request.GET.get("start_time", None)
#         end_time = request.GET.get("end_time", None)

#         querySet = KgDDAction.objects
#         if keyword is not None and len(keyword) > 0:
#             querySet = querySet.filter(name__contains="{}".format(keyword))
#         if start_time:
#             querySet = querySet.filter(created_at__gt="{}".format(start_time))
#         if end_time:
#             querySet = querySet.filter(created_at__lt="{}".format(end_time))
#         querySet = querySet.all().order_by('-updated_at')

#         data['total'] = len(querySet)
#         data['page'] = page
#         data['pageSize'] = pageSize
#         paginator = Paginator(querySet, pageSize) 
#         try:
#             objs =  paginator.page(page)
#         except PageNotAnInteger:
#             objs = paginator.page(1)
#         except:
#             objs = paginator.page(paginator.num_pages)
        
#         kds = KgDDActionSerializer(data=objs, many=True)
#         kds.is_valid()
#         data['data'] = kds.data
#         serializers = KgDDActionResponseSerializer(data=data, many=False)
#         serializers.is_valid()
#         return Response(serializers.data,  status=status.HTTP_200_OK)


# class KgDDActionSaveApiView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):

#     serializer_class = KgQADetailResponseSerializer
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#     @swagger_auto_schema(
#             operation_description='GET /ddrule/actionsave/',
#             operation_summary="保存(增加|更新)规则调度目标",
#             request_body=openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 required=['name', 'user_id'],
#                 properties={
#                     'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="用户ID"),
#                     'action_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="目标ID"),
#                     'name': openapi.Schema(type=openapi.TYPE_STRING, description="目标名称"),
#                 },
#             ),
#             tags = ['ddrule'])
    
#     def post(self, request, *args, **kwargs):
#         user_id = request.data.get('user_id', None)
#         action_id = request.data.get('action_id', None)
#         name = request.data.get('name', None)
#         if user_id is None:
#             serializers = KgDDActionDetailResponseSerializer(data={"code": 201, "msg": "用户ID错误"}, many=False)
#             serializers.is_valid()
#             return Response(serializers.data,  status=status.HTTP_200_OK)
        
#         try:
#             tmpuser = User.objects.get(id=user_id)
#         except:
#             data = {"code": 202, "msg": "用户ID不存在！！！" }
#             serializers = KgDDActionDetailResponseSerializer(data=data, many=False)
#             serializers.is_valid()
#             return Response(serializers.data, status=status.HTTP_200_OK)
        
#         if action_id is None:
#             # 保存操作
#             tmpent, tmpbool = KgDDAction.objects.get_or_create(name=name)
#             if tmpbool:
#                 tmpent.kg_user_id = tmpuser
#                 tmpent.created_at = datetime.now()
#                 tmpent.updated_at = datetime.now()
#                 tmpent.save()
#                 data = {"code": 200, "msg": "新建目标成功"}
#                 data['data'] = model_to_dict(tmpent, exclude=['kg_user_id'])
#                 data['data']['kguser'] = tmpent.kguser
#                 serializers = KgDDActionDetailResponseSerializer(data=data, many=False)
#             else:
#                 serializers = KgDDActionDetailResponseSerializer(data={"code": 203, "msg": "实体名称已经存在！"}, many=False)
#         else:
#             # 更新操作
#             try:
#                 tmpact = KgDDAction.objects.get(id=action_id)
#                 if name is not None and len(name) > 0:
#                     tmpent = KgDDAction.objects.filter(name=name).first()
#                     if tmpent and tmpact.id != tmpent.id:
#                         serializers = KgDDActionDetailResponseSerializer(data={"code": 204, "msg": "目标名称已经存在"}, many=False)
#                     else:
#                         tmpact.name = name
#                         tmpact.save()
#                         data = {"code": 200, "msg": "更新目标成功"}
#                         data['data'] = model_to_dict(tmpact, exclude=['kg_user_id'])
#                         data['data']['kguser'] = tmpact.kguser
#                         serializers = KgDDActionDetailResponseSerializer(data=data, many=False)
#                 else:
#                     serializers = KgDDActionDetailResponseSerializer(data={"code": 205, "msg": "目标名称参数错误"}, many=False)
#             except:
#                 serializers = KgDDActionDetailResponseSerializer(data={"code": 206, "msg": "目标ID不存在"}, many=False)

#         serializers.is_valid()
#         return Response(serializers.data,  status=status.HTTP_200_OK)


# class KgDDActionDelApiView(APIView):

#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     serializer_class = KgDDActionDetailResponseSerializer
#     @swagger_auto_schema(
#         operation_description="规则调度删除",
#         operation_summary="[可用] 规则调度删除",
#         # request_body is used to specify parameters
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['id'],
#             properties={
#                 'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="调度规则目标ID"),
#             },
#         ),
#         responses={
#             200: KgDDActionDetailResponseSerializer(many=False),
#             400: "请求失败",
#         },
#         tags=['ddrule']
#     )
#     @csrf_exempt
#     def post(self, request):
#         aid = request.data["id"]
#         if aid is None:
#             serializers = KgDDActionDetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
#             serializers.is_valid()
#             return Response(serializers.data, status=status.HTTP_200_OK)
#         try:
#             tmpkg = KgDDAction.objects.get(id=aid)
#             if tmpkg:
#                 tmpkg.delete()
#                 serializers = KgDDActionDetailResponseSerializer(data={"code": 200, "msg": "规则删除成功" }, many=False)
#             else:
#                 serializers = KgDDActionDetailResponseSerializer(data={"code": 201, "msg": "调度规则不存在" }, many=False)
#         except:
#             serializers = KgDDActionDetailResponseSerializer(data={"code": 202, "msg": "调度规则ID不存在" }, many=False)
        
#         serializers.is_valid()
#         return Response(serializers.data, status=status.HTTP_200_OK)
    

class KgDDRuleAttributeList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgDDRuleAttributeResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /ddrule/attrlist/',
            operation_summary="获取调度条件指标列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="1则搜索条件; 2则搜索目标"),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间',),
                openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间',),
            ],
            responses={
                200: KgDDRuleAttributeResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['ddrule'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        type = request.GET.get("type", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        querySet = KgDDRuleAttribute.objects

        if type is not None:
            querySet = querySet.filter(type="{}".format(type))
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(zhName__contains="{}".format(keyword))
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
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        kds = KgDDRuleAttributeSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgDDRuleAttributeResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgDDRuleAttributeSaveApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    serializer_class = KgQADetailResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
            operation_description='GET /ddrule/attrsave/',
            operation_summary="保存(增加|更新)条件指标|目标",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['name', 'valueType'],
                properties={
                    'attr_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="指标ID"),
                    'zhName': openapi.Schema(type=openapi.TYPE_STRING, description="指标名称"),
                    'type': openapi.Schema(type=openapi.TYPE_INTEGER, description="指标类型: 1则搜索条件; 2则搜索目标"),
                    'valueType': openapi.Schema(type=openapi.TYPE_STRING, description="值类型: type:2  int|string"),
                },
            ),
            tags = ['ddrule'])
    
    def post(self, request, *args, **kwargs):
        attr_id = request.data.get('attr_id', None)
        zhName = request.data.get('zhName', None)
        type = request.data.get('type', None)
        valueType = request.data.get('valueType', None)
        
        if attr_id is None:
            # 保存操作
            tmpent, tmpbool = KgDDRuleAttribute.objects.get_or_create(zhName=zhName)
            if tmpbool:
                tmpent.type = type
                tmpent.valueType = valueType
                tmpent.zhName = zhName

                if zhName and len(zhName) > 0:
                    import pypinyin
                    psrt = pypinyin.pinyin(zhName, style=pypinyin.NORMAL)
                    tmpent.name = "".join([item for innerlist in psrt for item in innerlist])
                else:
                    tmpent.name = ""

                tmpent.created_at = datetime.now()
                tmpent.updated_at = datetime.now()
                tmpent.save()
                data = {"code": 200, "msg": "新建指标成功"}
                data['data'] = model_to_dict(tmpent, exclude=[''])
                serializers = KgDDRuleAttributeDetailResponseSerializer(data=data, many=False)
            else:
                serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 203, "msg": "实体名称已经存在！"}, many=False)
        else:
            # 更新操作
            try:
                tmpatt = KgDDRuleAttribute.objects.get(id=attr_id)
                if zhName is not None and len(zhName) > 0:
                    tmpent = KgDDRuleAttribute.objects.filter(zhName=zhName).first()
                    if tmpent and tmpatt.id != tmpent.id:
                        serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 204, "msg": "目标名称已经存在"}, many=False)
                    else:
                        if zhName and len(zhName) > 0:
                            import pypinyin
                            tmpatt.zhName = zhName
                            psrt = pypinyin.pinyin(zhName, style=pypinyin.NORMAL)
                            tmpatt.name = "".join([item for innerlist in psrt for item in innerlist])
                        if type:
                            tmpatt.type = type

                        if valueType:
                            tmpatt.valueType = valueType
                        
                        tmpatt.updated_at = datetime.now()
                        tmpatt.save()
                        data = {"code": 200, "msg": "更新属性成功"}
                        data['data'] = model_to_dict(tmpatt, exclude=[''])
                        serializers = KgDDRuleAttributeDetailResponseSerializer(data=data, many=False)
                else:
                    serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 205, "msg": "目标名称参数错误"}, many=False)
            except:
                serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 206, "msg": "目标ID不存在"}, many=False)

        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)


class KgDDRuleAttributeDelApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgDDRuleAttributeDetailResponseSerializer
    @swagger_auto_schema(
        operation_description="条件指标删除",
        operation_summary="[可用] 条件指标删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="调度条件指标ID"),
            },
        ),
        responses={
            200: KgDDRuleAttributeDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['ddrule']
    )
    @csrf_exempt
    def post(self, request):
        aid = request.data["id"]
        if aid is None:
            serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgDDRuleAttribute.objects.get(id=aid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 200, "msg": "规则指标删除成功" }, many=False)
            else:
                serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 201, "msg": "规则规则不存在" }, many=False)
        except:
            serializers = KgDDRuleAttributeDetailResponseSerializer(data={"code": 202, "msg": "规则规则ID不存在" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    


class KgDDRuleList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgDDRuleResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /ddrule/rulelist/',
            operation_summary="获取调度规则列表",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
                openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
                openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间',),
                openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间',),
            ],
            responses={
                200: KgDDRuleResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['ddrule'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        querySet = KgDDRule.objects
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
            objs =  paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        
        kds = KgDDRuleSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgDDRuleResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)
    

def checkContent(childlist: list, conditionIds: set):
    if not childlist:
        raise ValueError("尚未添加决策目标！请添加后再进行保存和发布。")

    for children in childlist:
        if RuleContentTypeEnum.attr.name == children['type']:
            attribute = KgDDRuleAttribute.objects.get(id=children['id'])
            if attribute is None:
                raise ValueError("部分条件指标为空！请补充后再进行保存和发布。")
            
            conditionIds.add(attribute.id)
            checkContent(children['children'], conditionIds)
        elif RuleContentTypeEnum.condition.name == children['type']:
            if not children['conditionInfos']:
                raise ValueError("部分判断条件为空！请补充后再进行保存和发布。")
            elif len(children['conditionInfos']) != 2:
                raise ValueError("条件节点数量错误！")
            for i, info in enumerate(children['conditionInfos']):
                print("check:", info)
                connect = info['connect']
                operator = info['operator']
                value = info['value']
                valueType = info['valueType']
                judgeType = info['judgeType']
                if i == 1:
                    if len(connect) == 0 and len(operator) == 0 and len(value) == 0 and len(valueType) == 0 and len(judgeType) == 0:
                        continue
                    elif len(connect) != 0 and connect not in RuleContentConnectList:
                        raise ValueError("规则详情连接符错误！")
                if operator not in RuleContentOperatorList:
                    raise ValueError("部分判断条件为空！请补充后再进行保存和发布。")
                elif valueType != AttributeValueTypeEnum.int.name and valueType != AttributeValueTypeEnum.boolean.name:
                    raise ValueError("节点值类型错误！")
                elif judgeType not in RuleContentJudgeTypeList:
                    raise ValueError("节点判断类型错误！")
                elif judgeType == RuleContentJudgeTypeEnum.select.name:
                    try:
                        tmpid = int(value)
                    except:
                        raise ValueError("规则详情条件节点属性错误!")
                    attribute = KgDDRuleAttribute.objects.get(id=tmpid)
                    if attribute is None:
                        raise ValueError("规则详情条件节点属性错误!")
                    conditionIds.add(attribute.id)
                else:
                    try:
                        tmpv = float(value)
                    except:
                        raise ValueError("规则详情条件节点值错误!")
            checkContent(children['children'], conditionIds)

        elif RuleContentTypeEnum.action.name == children['type']:
            if 'value' in children and len(children['value']) == 0:
                raise ValueError("决策目标暂未填写！请填写后再进行保存和发布。")
        else:
            raise ValueError("部分节点类型错误！")


def getContent(content: dict, conditionIds: set):

    if not content or 'type' not in content or 'children' not in content:
        return json.dumps(content)
    if RuleContentTypeEnum.root.name != content['type']:
        raise ValueError("没有找到根节点！")

    checkContent(content['children'], conditionIds)
    return json.dumps(content)


class KgDDRuleSaveApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    serializer_class = KgDDRuleDetailResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
            operation_description='GET /ddrule/rulesave/',
            operation_summary="保存(增加|更新)规则实例",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=[''],
                properties={
                    'rule_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="规则ID"),
                    'action_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="目标ID"),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="规则名称"),
                    'desc': openapi.Schema(type=openapi.TYPE_STRING, description="规则描述"),
                    'content': openapi.Schema(type=openapi.TYPE_OBJECT, description="规则内容"),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER, description="规则状态"),
                },
            ),
            tags = ['ddrule'])
    
    def post(self, request, *args, **kwargs):
        rule_id = request.data.get('rule_id', None)
        action_id = request.data.get('action_id', None)
        name = request.data.get('name', None)
        desc = request.data.get('desc', None)
        status_code = request.data.get('status', None)
        contentJson = request.data.get('content', {})

        attributeAction = KgDDRuleAttribute.objects.get(id=action_id)
        if attributeAction is None:
            serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "无效决策目标"}, many=False)
            serializers.is_valid()

            return Response(serializers.data,  status=status.HTTP_200_OK)
        conditionIds = set()
        # content = getContent(contentJson, conditionIds)
        try:
            content = getContent(contentJson, conditionIds)
        except ValueError as errmsg:
            serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": str(errmsg) }, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)

        ruleAction = KgDDRule.objects.filter(action_id=action_id).first()
        if rule_id is None:
            info = KgDDRule.objects.filter(name=name)
            if info:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "规则名称已经存在！"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            if ruleAction:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 202, "msg": "决策目标已被其他规则使用"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            try:
                info = KgDDRule()
                info.name = name
                info.desc = desc if desc and len(desc) > 0 else ""
                info.created_at = datetime.now()
                info.updated_at = datetime.now()
                info.type = 1
                info.order = 0
                info.action_id = action_id
                info.content = content
                info.status = status_code
                info.save()
                for cid in conditionIds:
                    tmp = KgDDRuleAttribute.objects.get(id=cid)
                    info.attrs.add(tmp)
                info.save()
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 200, "msg": "新增成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            except:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 203, "msg": "新增失败"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
        else:
            try:
                info = KgDDRule.objects.get(id=rule_id)
            except:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 204, "msg": "无效ID"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            nameInfo = KgDDRule.objects.filter(name=name).first()
            if nameInfo and nameInfo.id != info.id:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 205, "msg": "已存在同名的规则"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)

            if ruleAction and ruleAction.id != info.id:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 206, "msg": "决策目标已被其他规则使用"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)

            try:
                info.name = name
                info.desc = desc if desc and len(desc) > 0 else ""
                info.updated_at = datetime.now()
                info.type = 1
                info.order = 0
                if action_id is not None:
                    info.action_id = action_id
                info.content = content
                if status_code is not None:
                    info.status = status_code
                info.save()
                info.attrs.clear()
                for cid in conditionIds:
                    tmp = KgDDRuleAttribute.objects.get(id=cid)
                    info.attrs.add(tmp)
                info.save()

                serializers = KgDDRuleDetailResponseSerializer(data={"code": 200, "msg": "更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)
            except:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 207, "msg": "更新失败"}, many=False)
                serializers.is_valid()
                return Response(serializers.data,  status=status.HTTP_200_OK)


class KgDDRuleEnableApiView(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgDDRuleDetailResponseSerializer
    @swagger_auto_schema(
        operation_description="启用/停用规则接口",
        operation_summary="[可用] 启用/停用规则接口",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="调度条件指标ID"),
                'status': openapi.Schema(type=openapi.TYPE_INTEGER, description="启停状态"),
            },
        ),
        responses={
            200: KgDDRuleDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['ddrule']
    )
    @csrf_exempt
    def post(self, request):
        rid = request.data.get('id', None)
        status_code = request.data.get('status', None)
        if rid is None:
            serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...." }, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgDDRule.objects.get(id=rid)
            if tmpkg:
                tmpkg.status = status_code
                tmpkg.save()
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 200, "msg": "规则状态更新成功" }, many=False)
            else:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "调度规则不存在" }, many=False)
        except:
            serializers = KgDDRuleDetailResponseSerializer(data={"code": 202, "msg": "调度规则ID不存在" }, many=False)
        
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)

class KgDDRuleDetailApiView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = KgDDRuleDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET ddrule/ruledetail',
        operation_summary="获取规则详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgDDRuleDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['ddrule'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        tmpid = request.GET.get("id", None)
        if tmpid:
            try:
                tmp = KgDDRule.objects.get(id=tmpid)
                data['data'] = model_to_dict(tmp, exclude=['attrs'])
                data['data']['action'] = tmp.action
                data['data']['attrlist'] = tmp.attrlist
                data['data']['conditionInfos'] = tmp.conditionInfos
                serializers = KgDDRuleDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "不存在该规则"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgDDRuleDelApiView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgDDRuleDetailResponseSerializer

    @swagger_auto_schema(
        operation_description="条件指标删除",
        operation_summary="[可用] 条件指标删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="调度条件指标ID"),
            },
        ),
        responses={
            200: KgDDRuleDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['ddrule']
    )
    @csrf_exempt
    def post(self, request):
        rid = request.data.get('id', None)
        if rid is None:
            serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "请求参数错误...."}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgDDRule.objects.get(id=rid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 200, "msg": "调度规则删除成功"}, many=False)
            else:
                serializers = KgDDRuleDetailResponseSerializer(data={"code": 201, "msg": "调度规则不存在"},
                                                                        many=False)
        except:
            serializers = KgDDRuleDetailResponseSerializer(data={"code": 202, "msg": "调度规则ID不存在"}, many=False)

        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


def nodePass(info, parentValue, condictions: list):
    connect = info['connect']
    operator = info['operator']
    value = info['value']
    valueType = info['valueType']
    judgeType = info['judgeType']

    value = None
    if judgeType == 'input':
        value = float(info['value'])
    else:
        val = ""
        for cc in condictions:
            if int(cc['id']) == int(info['value']):
                val = cc['value']
        if len(val) == 0:
            return False
        try:
            value = float(val)
        except:
            return False

    isPass = False
    if operator == "=":
        isPass = abs(parentValue-value) < 0.001
    elif operator == ">":
        isPass = parentValue > value
    elif operator == ">=":
        isPass = parentValue > value or abs(parentValue-value) < 0.001
    elif operator == "<":
        isPass = parentValue < value
    elif operator == "<=":
        isPass = parentValue < value or abs(parentValue-value) < 0.001

    return isPass


def doAction(children, condictions, result, parentValue):

    if RuleContentTypeEnum.attr.name == children['type']:
        try:
            inputValue = None
            for cc in condictions:
                if int(cc['id']) == int(children['id']):
                    inputValue = float(cc['value'])
        except:
            serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "条件规则必须是数字！"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        for child in children['children']:
            doAction(child, condictions, result, inputValue)

    elif RuleContentTypeEnum.condition.name == children['type']:
        isPass = False
        info0 = children['conditionInfos'][0]
        info1 = children['conditionInfos'][1]

        connect = info1['connect']
        operator = info1['operator']
        value = info1['value']
        valueType = info1['valueType']
        judgeType = info1['judgeType']
        isOneCondition = len(connect) == 0 and len(operator) == 0 \
                         and len(value) == 0 and len(valueType) == 0 \
                         and len(judgeType) == 0

        if isOneCondition:
            isPass = nodePass(info0, parentValue, condictions)
        else:
            isPass0 = nodePass(info0, parentValue, condictions)
            isPass1 = nodePass(info1, parentValue, condictions)
            isOr = connect == '|'
            isPass = (isOr and (isPass0 or isPass1)) or (not isOr and isPass0 and isPass1)
        if isPass:
            for actChild in children['children']:
                doAction(actChild, condictions, result, None)

    elif RuleContentTypeEnum.action.name == children['type']:
        result.append(children['value'])


def getAction(content: dict, condictions:list):
    result = []
    for children in content['children']:
        print("getAction->", children)
        doAction(children, condictions, result, None)

    print("getAction-->", result)
    if not result:
        serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "未命中决策规则，请检查是否有指标条件缺少！"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    serializers = KgDDRuleResultResponseSerializer(data={"code": 200, "msg": "success", "data": result}, many=False)
    serializers.is_valid()
    return Response(serializers.data, status=status.HTTP_200_OK)


class KgDDRuleResultApiView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgDDRuleResultResponseSerializer

    @swagger_auto_schema(
        operation_description="规则运行推理",
        operation_summary="[可用] 规则运行推理",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="调度规则ID"),
                'flag': openapi.Schema(type=openapi.TYPE_INTEGER, description="本地测试环境"),
            },
        ),
        responses={
            200: KgDDRuleResultResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['ddrule']
    )
    @csrf_exempt
    def post(self, request):
        ruleId = request.data.get('id', None)
        flag = request.data.get('flag', 0)
        conditionInfos = request.data.get('conditionInfos', [])
        if ruleId is None:
            serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "请求参数错误...."}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            rule = KgDDRule.objects.get(id=ruleId)
        except:
            serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "规则不存在"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if rule.status == 0 and flag == 0:
            serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "规则未启用"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        attribute_ids = sorted([att.id for att in rule.attrs.all()])
        condition_ids = sorted([int(param['id']) for param in conditionInfos])

        if len(attribute_ids) != len(condition_ids):
            serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "规则已修改,请刷新"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        for attid, conid in zip(attribute_ids, condition_ids):
            if attid != conid:
                serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "规则已修改,请刷新"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        content = json.loads(rule.content)
        if not content:
            serializers = KgDDRuleResultResponseSerializer(data={"code": 201, "msg": "规则内容失败，请检查规则配置！"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        return getAction(content, conditionInfos)
