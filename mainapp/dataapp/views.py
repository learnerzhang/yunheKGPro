from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from kgapp.serializers import KgBaseResponseSerializer
from .models import AppAPIModel, DataModel, DataModelParam  # 确保导入您的接口
from kgapp.models import KgTag
from userapp.models import User
from .serializers import DataModelSerializer, DataModelParamDetailResponseSerializer, DataModelParamSerializer
from django.utils import timezone
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import NotFound, ValidationError
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from rest_framework.views import APIView
from django.forms.models import model_to_dict
import json
# import datetime
import requests
from datetime import datetime
from langchain_community.llms import Ollama
from urllib.parse import urlencode
from yunheKGPro import CsrfExemptSessionAuthentication


def query_question(text):
    llm = Ollama(model="qwen2.5")
    res = llm(text)
    return res


class DataModelAPIView(generics.GenericAPIView):
    serializer_class = DataModelSerializer
    queryset = DataModel.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='获取数据接口列表',
        operation_description='GET /dataapp/datamodel/',
        manual_parameters=[
            openapi.Parameter(
                'keyword',
                openapi.IN_QUERY,
                description='关键词搜索',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'activate',
                openapi.IN_QUERY,
                description='激活状态 0|1',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: DataModelSerializer(many=True),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        try:
            keyword = request.query_params.get('keyword', '')
            activate = request.query_params.get('activate', None)

            queryset = self.get_queryset()
            if keyword:
                queryset = queryset.filter(name__icontains=keyword)
            if activate is not None:
                queryset = queryset.filter(activate=activate)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='新增数据接口',
        operation_description='POST /dataapp/datamodel/',
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_FORM, description='接口id', type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('name', openapi.IN_FORM, description='接口名称', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('req_type', openapi.IN_FORM, description='请求方式 0(post)|1(get)',
                              type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('url', openapi.IN_FORM, description='接口地址', type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('activate', openapi.IN_FORM, description='激活状态 0|1', type=openapi.TYPE_INTEGER,
                              required=True),
            openapi.Parameter('function', openapi.IN_FORM, description='功能介绍', type=openapi.TYPE_STRING,
                              required=False),
            openapi.Parameter('desc', openapi.IN_FORM, description='接口描述', type=openapi.TYPE_STRING,
                              required=False),
            openapi.Parameter('version', openapi.IN_FORM, description='版本号', type=openapi.TYPE_STRING,
                              required=False),
            openapi.Parameter('user_id', openapi.IN_FORM, description='创建作者ID', type=openapi.TYPE_INTEGER,
                              required=False),
            openapi.Parameter('no', openapi.IN_FORM, description='接口编号', type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('business_tag', openapi.IN_FORM, description='业务标签ID', type=openapi.TYPE_INTEGER,
                              required=True),
            openapi.Parameter('user_name', openapi.IN_FORM, description='创建用户名称', type=openapi.TYPE_STRING,
                              required=False),
            openapi.Parameter('update_time', openapi.IN_FORM, description='更新时间', type=openapi.TYPE_STRING,
                              required=False),
            openapi.Parameter('create_time', openapi.IN_FORM, description='创建时间', type=openapi.TYPE_STRING,
                              required=False),
        ],
        responses={
            200: DataModelSerializer,
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def post(self, request, *args, **kwargs):
        try:
            # 获取必需参数
            name = request.data.get('name')
            req_type = request.data.get('req_type')
            url = request.data.get('url')
            activate = request.data.get('activate')

            # 验证必需参数
            if not all([name, req_type is not None, url, activate is not None]):
                return Response({
                    'code': 400,
                    'msg': '缺少必要参数：接口名称、请求方式、接口地址和激活状态为必填项'
                }, status=status.HTTP_400_BAD_REQUEST)

            req_type = int(req_type)
            # 验证请求方式的值
            if req_type not in [0, 1]:
                return Response({
                    'code': 400,
                    'msg': '请求方式只能是0(post)或1(get)'
                }, status=status.HTTP_400_BAD_REQUEST)

            activate = int(activate)
            # 验证激活状态的值
            if activate not in [0, 1]:
                return Response({
                    'code': 400,
                    'msg': '激活状态只能是0或1'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取可选参数
            business_tag_id = request.data.get('business_tag')
            business_tag = None
            if business_tag_id:
                try:
                    business_tag = KgTag.objects.get(id=business_tag_id)
                except KgTag.DoesNotExist:
                    return Response({
                        'code': 400,
                        'msg': '业务标签不存在'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # 创建新数据接口
            model = DataModel(
                name=name,
                req_type=req_type,
                url=url,
                activate=activate,
                function=request.data.get('function'),
                desc=request.data.get('desc'),
                version=request.data.get('version'),
                business_tag=business_tag,  # 添加 business_tag
                no=request.data.get('no'),
                create_time=request.data.get('create_time', datetime.now()),
                update_time=request.data.get('update_time', datetime.now())
            )
            model.save()

            serializer = self.get_serializer(model)
            return Response({
                'code': 200,
                'msg': '创建成功',
                'data': serializer.data
            })

        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DataModelListAPIView(generics.GenericAPIView):
    serializer_class = DataModelSerializer
    queryset = DataModel.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='获取所有数据接口信息',
        operation_description='GET /dataapp/datamodellist/',
        responses={
            200: DataModelSerializer(many=True),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):  # 修改为 get 方法
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'code': 200,
                'msg': '获取成功',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DataModelDeleteAPIView(generics.GenericAPIView):
    queryset = DataModel.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='删除数据接口',
        operation_description='DELETE /dataapp/datamodel/',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='数据接口ID'),
            },
            required=['id'],
        ),
        responses={
            204: "删除成功",
            400: "请求失败",
            404: "未找到该数据接口"
        },
        tags=['datamodel']
    )
    def delete(self, request, *args, **kwargs):
        try:
            # 从请求体获取 id
            id = request.data.get('id')
            if id is None:
                return Response({
                    'code': 400,
                    'msg': '缺少参数: id'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 查找所需的 DataModel 实例
            model = self.get_queryset().filter(id=id).first()
            if model is None:
                raise NotFound("未找到该数据接口")

            # 删除实例
            model.delete()

            return Response({
                'code': 204,
                'msg': '删除成功'
            }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DataModelBatchDeleteAPIView(generics.GenericAPIView):
    queryset = DataModel.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_summary='批量删除数据接口',
        operation_description='POST /dataapp/datamodel/batchdelete',
        manual_parameters=[
            openapi.Parameter(
                name='data',
                in_=openapi.IN_FORM,
                description='批量删除的接口ID列表',
                type=openapi.TYPE_STRING,
                example='{"data": [{"id": 1}, {"id": 2}]}'
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'msg': openapi.Schema(type=openapi.TYPE_STRING),
                    'details': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            ),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        reqdata = json.loads(request.data.get("data", "{}"))
        success_count = 0
        error_count = 0
        messages = []

        for item in reqdata.get('data', []):
            id = item.get("id")

            if id is None:
                error_count += 1
                messages.append("缺少必需的参数 id")
                continue

            try:
                data_model = DataModel.objects.get(id=id)
                data_model.delete()
                success_count += 1
            except DataModel.DoesNotExist:
                error_count += 1
                messages.append(f"接口ID {id} 不存在")

        return Response({
            "code": 200,
            "msg": f"成功删除 {success_count} 个接口, 失败 {error_count} 个",
            "details": messages
        }, status=status.HTTP_200_OK)


class DataModelUpdateAPIView(generics.GenericAPIView):
    serializer_class = DataModelSerializer
    queryset = DataModel.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    # 现有的 GET 和 POST 方法...

    @swagger_auto_schema(
        operation_summary='更新数据',
        operation_description='PUT /dataapp/datamodel/',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_FORM,
                description='数据接口ID',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'name',
                openapi.IN_FORM,
                description='接口名称',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'req_type',
                openapi.IN_FORM,
                description='请求方式 0(post)|1(get)',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'url',
                openapi.IN_FORM,
                description='接口地址',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'activate',
                openapi.IN_FORM,
                description='激活状态 0|1',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'function',
                openapi.IN_FORM,
                description='功能介绍',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'desc',
                openapi.IN_FORM,
                description='接口描述',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'version',
                openapi.IN_FORM,
                description='版本号',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'no',
                openapi.IN_FORM,
                description='接口编号',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'user_id',
                openapi.IN_FORM,
                description='用户id',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'user_name',
                openapi.IN_FORM,
                description='用户名',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'update_time',
                openapi.IN_FORM,
                description='更新时间',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'create_time',
                openapi.IN_FORM,
                description='创建时间',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'kgTag_id',
                openapi.IN_FORM,
                description='业务标签ID',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: DataModelSerializer,
            400: "请求失败",
            404: "未找到该数据接口"
        },
        tags=['datamodel']
    )
    def put(self, request, *args, **kwargs):
        try:
            # 获取必需参数
            id = request.data.get('id')
            name = request.data.get('name')
            req_type = request.data.get('req_type')
            url = request.data.get('url')
            activate = request.data.get('activate')

            # 验证必需参数
            if not all([id, name, req_type is not None, url, activate is not None]):
                return Response({
                    'code': 400,
                    'msg': '缺少必要参数：id、接口名称、请求方式、接口地址和激活状态为必填项'
                }, status=status.HTTP_400_BAD_REQUEST)

            req_type = int(req_type)
            activate = int(activate)

            # 验证请求方式和激活状态的值
            if req_type not in [0, 1]:
                return Response({
                    'code': 400,
                    'msg': '请求方式只能是0(post)或1(get)'
                }, status=status.HTTP_400_BAD_REQUEST)

            if activate not in [0, 1]:
                return Response({
                    'code': 400,
                    'msg': '激活状态只能是0或1'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 查找要更新的接口实例
            model = self.get_queryset().filter(id=id).first()
            if model is None:
                raise NotFound("未找到该数据接口")

            # 更新接口字段
            model.name = name
            model.req_type = req_type
            model.url = url
            model.activate = activate
            model.function = request.data.get('function', model.function)  # 保持原值如未提供
            model.desc = request.data.get('desc', model.desc)  # 保持原值如未提供
            model.version = request.data.get('version', model.version)  # 保持原值如未提供
            model.no = request.data.get('no', model.no)  # 保持原值如未提供
            model.update_time = datetime.now()  # 更新当前时间
            # 更新业务标签
            kgTag_id = request.data.get('kgTag_id')
            if kgTag_id is not None:
                try:
                    model.business_tag = KgTag.objects.get(id=kgTag_id)
                except KgTag.DoesNotExist:
                    return Response({
                        'code': 400,
                        'msg': '指定的业务标签ID不存在'
                    }, status=status.HTTP_400_BAD_REQUEST)
            # 保存更新
            model.save()

            serializer = self.get_serializer(model)
            return Response({
                'code': 200,
                'msg': '更新成功',
                'data': serializer.data
            })

        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DataModelRetrieveAPIView(generics.GenericAPIView):
    queryset = DataModel.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='查询数据接口',
        operation_description='GET /dataapp/datamodel/',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description='数据接口ID',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: DataModelSerializer,
            400: "请求失败",
            404: "未找到该数据接口"
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        try:
            # 从查询参数获取 id
            id = request.query_params.get('id')
            if id is None:
                return Response({
                    'code': 400,
                    'msg': '缺少参数: id'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 查找所需的 DataModel 实例
            model = self.get_queryset().filter(id=id).first()
            if model is None:
                raise NotFound("未找到该数据接口")

            # 序列化数据
            serializer = DataModelSerializer(model)
            response_data = serializer.data
            response_data['kgTag_id'] = response_data.get('kgTag_id', None)  # 确保返回字段中包含 kgTag_id
            return Response({
                'code': 200,
                'msg': '查询成功',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DataModelSearchAPIView(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):
    serializer_class = DataModelSerializer  # 假设您已经定义了 DataModelSerializer

    @swagger_auto_schema(
        operation_description='GET /datamodel/list/',
        operation_summary="获取数据模型列表",
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间'),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间'),
        ],
        responses={
            200: DataModelSerializer(many=True),  # 返回多个数据模型的序列化结果
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        querySet = DataModel.objects.all()  # 获取所有数据模型
        if keyword:
            querySet = querySet.filter(name__icontains=keyword)  # 使用不区分大小写的匹配
        if start_time:
            querySet = querySet.filter(create_time__gte=start_time)  # 包含开始时间
        if end_time:
            querySet = querySet.filter(create_time__lte=end_time)  # 包含结束时间
        querySet = querySet.order_by('-update_time')  # 按更新时间降序排列

        data['total'] = querySet.count()  # 获取总记录数
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(querySet, pageSize)

        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)

        serializer = DataModelSerializer(objs, many=True)  # 序列化数据
        data['data'] = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class DataModelParamAPIView(generics.GenericAPIView):
    queryset = DataModel.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='获取数据模型所包含的参数',
        operation_description='GET /dataapp/datamodel/params/',
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True,
                              description='数据模型ID'),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_INTEGER, description='响应状态码'),
                    'data': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='参数ID'),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='参数名称'),
                                'type': openapi.Schema(type=openapi.TYPE_STRING, description='参数类型'),
                                'default': openapi.Schema(type=openapi.TYPE_STRING, description='默认值'),
                                'desc': openapi.Schema(type=openapi.TYPE_STRING, description='参数说明'),
                                'necessary': openapi.Schema(type=openapi.TYPE_INTEGER, description='是否为必须参数'),
                                'activate': openapi.Schema(type=openapi.TYPE_INTEGER, description='激活状态'),
                                'kg_model_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='关联模型ID'),
                                'update_time': openapi.Schema(type=openapi.TYPE_STRING, description='更新时间'),
                                'create_time': openapi.Schema(type=openapi.TYPE_STRING, description='创建时间'),
                            }
                        )
                    )
                }
            ),
            400: "请求失败",
            404: "未找到该数据模型"
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        data_model_id = request.query_params.get('id')

        if not data_model_id:
            return Response({
                'code': 400,
                'msg': '缺少参数: id'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 查找所需的 DataModel 实例
            model = self.get_queryset().filter(id=data_model_id).first()
            if model is None:
                raise NotFound("未找到该数据模型")

            # 获取与该模型相关的所有参数
            params = DataModelParam.objects.filter(kg_model_id=model)

            # 构建返回数据
            param_list = [
                {
                    'id': param.id,
                    'name': param.name,
                    'type': param.type,
                    'default': param.default or '',
                    'desc': param.desc or '',
                    'necessary': param.necessary,
                    'activate': param.activate,
                    'kg_model_id': param.model_id,  # 使用 model_id 属性
                    'update_time': param.update_time.isoformat() if param.update_time else None,
                    'create_time': param.create_time.isoformat() if param.create_time else None,
                }
                for param in params
            ]

            return Response({
                'code': 200,
                'data': param_list
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DataModelTestAPIView(generics.GenericAPIView):
    queryset = DataModel.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='测试接口功能',
        operation_description='GET /dataapp/datamodelretrive/',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='接口名称',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'req_type',
                openapi.IN_QUERY,
                description='请求方式 1代表GET，0代表POST',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'url',
                openapi.IN_QUERY,
                description='API地址',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'activate',
                openapi.IN_QUERY,
                description='激活状态 0或1',
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'params',
                openapi.IN_QUERY,
                description='请求参数（JSON格式）',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'headers',
                openapi.IN_QUERY,
                description='请求头（JSON格式）',
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'code': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'msg': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'curl_command': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: "请求失败",
            404: "未找到该数据接口"
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        req_type = request.query_params.get('req_type')
        # url = request.query_params.get('url')
        url = ''.join(char for char in request.query_params.get('url') if ord(char) >= 32 and ord(char) <= 126)
        activate = request.query_params.get('activate')
        params = request.query_params.get('params', '{}')  # 默认空参数
        headers = request.query_params.get('headers', '{}')  # 默认空头

        # 设置默认请求头
        if headers == '{}':
            headers = {'Content-Type': 'application/json'}
        else:
            try:
                headers = json.loads(headers)  # 尝试将 JSON 字符串解析为字典
            except json.JSONDecodeError:
                return Response({
                    'code': 400,
                    'msg': "请求头格式错误",
                    'curl_command': ''
                }, status=status.HTTP_400_BAD_REQUEST)

        # 尝试解析 params
        try:
            params = json.loads(params) if params else {}
        except json.JSONDecodeError:
            return Response({
                'code': 400,
                'msg': "请求参数格式错误",
                'curl_command': ''
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证输入
        if not all([name, req_type is not None, url, activate is not None]):
            raise ValidationError("缺少必要参数：接口名称、请求方式、API地址和激活状态为必填项")

        req_type = int(req_type)
        activate = int(activate)

        # 验证请求方式和激活状态
        if req_type not in [0, 1]:
            raise ValidationError("请求方式只能是0（POST）或1（GET）")
        if activate not in [0, 1]:
            raise ValidationError("激活状态只能是0或1")

        # 构造 curl 命令
        if req_type == 1:  # GET 请求
            query_string = urlencode(params)  # 将参数转换为查询字符串
            print("########query_string############", query_string)
            curl_command = f'curl -X GET "{url}?{query_string}"'
        else:  # POST 请求
            curl_command = f'curl -X POST "{url}"'
            curl_command += f' -d \'{json.dumps(params)}\''

        for key, value in headers.items():
            curl_command += f' -H "{key}: {value}"'

        # 根据请求方式发送请求
        try:
            if req_type == 1:  # GET 请求
                print("这是一个get请求：", params, headers)
                if params != {}:
                    print("参数不为空")
                    response = requests.get(url, params=params, headers=headers if headers else None)
                else:
                    print("没有参数的情况：headers:", headers, "url:", url)
                    print("url类型:", type(url))
                    response = requests.get(url, headers={'Content-Type': 'application/json'})

                    print("response:", response)
            else:  # POST 请求
                # response = requests.post(url, json=params, headers=headers)
                try:
                    response = requests.post(url, json=params, headers=headers)
                    response.raise_for_status()  # 检查请求是否成功
                except requests.exceptions.RequestException:
                    # 如果 json 请求失败，尝试使用 data 请求
                    response = requests.post(url, data=params, headers=headers)
            # 返回实际响应内容
            return Response({
                'code': response.status_code,
                'msg': '测试成功',
                'data': response.json(),  # 假设响应是 JSON 格式
                'curl_command': curl_command
            }, status=response.status_code)

        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e),
                'curl_command': curl_command
            }, status=status.HTTP_400_BAD_REQUEST)


class DataParamAddApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    parser_classes = (FormParser, MultiPartParser)

    @swagger_auto_schema(
        operation_summary='[可用] 新增参数功能',
        operation_description='POST /dataapp/datamodelparam/add',
        manual_parameters=[
            openapi.Parameter(name='mid', in_=openapi.IN_FORM, description='数据接口ID', type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='name', in_=openapi.IN_FORM, description='参数名称', type=openapi.TYPE_STRING),
            openapi.Parameter(name='type', in_=openapi.IN_FORM, description='参数类型', type=openapi.TYPE_STRING),
            openapi.Parameter(name='desc', in_=openapi.IN_FORM, description='参数说明', type=openapi.TYPE_STRING),
            openapi.Parameter(name='default', in_=openapi.IN_FORM, description='默认值', type=openapi.TYPE_STRING),
            openapi.Parameter(name='necessary', in_=openapi.IN_FORM, description='必须 0|1', type=openapi.TYPE_STRING),
        ],
        responses={
            200: DataModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def post(self, request, *args, **kwargs):
        mid = request.data.get("mid")
        name = request.data.get("name")
        type = request.data.get("type")
        desc = request.data.get("desc")
        default = request.data.get("default")
        necessary = request.data.get("necessary")

        if mid is None or name is None:
            return Response({"code": 201, "msg": "请求参数错误, 缺少参数！！！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_model = DataModel.objects.get(id=mid)
        except DataModel.DoesNotExist:
            return Response({"code": 201, "msg": "模型ID不存在！！！"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建参数
        data_model_param, created = DataModelParam.objects.get_or_create(name=name, type=type, kg_model_id=data_model)

        if created:
            data_model_param.desc = desc
            data_model_param.necessary = necessary
            data_model_param.activate = 0
            data_model_param.default = default
            data_model_param.create_time = datetime.now()
            data_model_param.update_time = datetime.now()
            data_model_param.save()
            serializer = DataModelParamSerializer(data_model_param)
            return Response({"code": 200, "msg": "参数创建成功", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"code": 201, "msg": "该参数已存在~~~"}, status=status.HTTP_400_BAD_REQUEST)


class DataParamBatchAddApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 批量新增参数功能',
        operation_description='POST /dataapp/datamodelparam/batchadd',
        manual_parameters=[
            openapi.Parameter(name='data', in_=openapi.IN_FORM, description='批量参数', type=openapi.TYPE_OBJECT),
        ],
        responses={
            200: DataModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def post(self, request, *args, **kwargs):
        reqdata = json.loads(request.data.get("data", {}))
        error_cnt = 0
        error_mid_cnt = 0
        success_cnt = 0
        exist_cnt = 0

        if reqdata:
            values = reqdata.get('data', [])
            for entry in values:
                mid = entry.get("mid")
                name = entry.get("name")
                type = entry.get("type")
                desc = entry.get("desc")
                default = entry.get("default")
                necessary = entry.get("necessary")

                if mid is None:
                    error_mid_cnt += 1
                    continue

                try:
                    data_model = DataModel.objects.get(id=mid)
                except DataModel.DoesNotExist:
                    error_mid_cnt += 1
                    continue

                if name is None or type is None:
                    error_cnt += 1
                    continue

                data_model_param, created = DataModelParam.objects.get_or_create(name=name, type=type,
                                                                                 kg_model_id=data_model)
                if created:
                    data_model_param.desc = desc
                    data_model_param.necessary = necessary
                    data_model_param.activate = 0
                    data_model_param.default = default
                    data_model_param.create_time = datetime.now()
                    data_model_param.update_time = datetime.now()
                    data_model_param.save()
                    success_cnt += 1
                else:
                    exist_cnt += 1

        msg = f"成功添加{success_cnt}, 已存在{exist_cnt}, 添加失败{error_cnt}, 模型ID错误 {error_mid_cnt}。"
        return Response({"code": 200, "msg": msg}, status=status.HTTP_200_OK)


class DataParamUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 更新参数功能',
        operation_description='POST /dataapp/datamodelparam/update/',
        manual_parameters=[
            openapi.Parameter(name='mid', in_=openapi.IN_FORM, description='数据接口ID', type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='pid', in_=openapi.IN_FORM, description='参数ID', type=openapi.TYPE_INTEGER),
            openapi.Parameter(name='name', in_=openapi.IN_FORM, description='参数名称', type=openapi.TYPE_STRING),
            openapi.Parameter(name='type', in_=openapi.IN_FORM, description='参数类型', type=openapi.TYPE_STRING),
            openapi.Parameter(name='desc', in_=openapi.IN_FORM, description='参数说明', type=openapi.TYPE_STRING),
            openapi.Parameter(name='default', in_=openapi.IN_FORM, description='默认参数值', type=openapi.TYPE_STRING),
            openapi.Parameter(name='necessary', in_=openapi.IN_FORM, description='必须 0|1', type=openapi.TYPE_STRING),
        ],
        responses={
            200: DataModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        mid = request.data.get("mid")
        pid = request.data.get("pid")
        name = request.data.get("name")
        type = request.data.get("type")
        desc = request.data.get("desc")
        default = request.data.get("default")
        necessary = request.data.get("necessary")

        if mid is None or pid is None:
            return Response({"code": 201, "msg": "请求参数错误, 缺少参数！！！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_model_param = DataModelParam.objects.get(id=pid)
            if name is not None:
                data_model_param.name = name
            if type is not None:
                data_model_param.type = type
            if desc is not None:
                data_model_param.desc = desc
            if default is not None:
                data_model_param.default = default
            if necessary is not None:
                data_model_param.necessary = necessary
            data_model_param.update_time = datetime.now()
            data_model_param.save()

            return Response({"code": 200, "msg": "参数更新成功"}, status=status.HTTP_200_OK)
        except DataModelParam.DoesNotExist:
            return Response({"code": 201, "msg": "参数ID不存在！！！"}, status=status.HTTP_400_BAD_REQUEST)


class DataParamBatchUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 批量更新参数功能',
        operation_description='POST /dataapp/datamodelparam/batchupdate',
        manual_parameters=[
            openapi.Parameter(name='data', in_=openapi.IN_FORM, description='批量更新参数', type=openapi.TYPE_STRING),
        ],
        responses={
            200: DataModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        reqdata = json.loads(request.data.get("data", "{}"))
        success_count = 0
        error_count = 0
        messages = []

        for item in reqdata.get('data', []):
            mid = item.get("mid")
            pid = item.get("pid")
            name = item.get("name")
            type = item.get("type")
            desc = item.get("desc")
            default = item.get("default")
            necessary = item.get("necessary")

            if mid is None or pid is None:
                error_count += 1
                messages.append("缺少必需的参数 mid 或 pid")
                continue

            try:
                data_model_param = DataModelParam.objects.get(id=pid)
                data_model_param.name = name if name is not None else data_model_param.name
                data_model_param.type = type if type is not None else data_model_param.type
                data_model_param.desc = desc if desc is not None else data_model_param.desc
                data_model_param.default = default if default is not None else data_model_param.default
                data_model_param.necessary = necessary if necessary is not None else data_model_param.necessary
                data_model_param.update_time = datetime.now()
                data_model_param.save()
                success_count += 1
            except DataModelParam.DoesNotExist:
                error_count += 1
                messages.append(f"参数ID {pid} 不存在")

        return Response(
            {"code": 200, "msg": f"成功更新 {success_count} 个参数, 失败 {error_count} 个", "details": messages},
            status=status.HTTP_200_OK)


class DataParamDeleteApiView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description="删除模型参数",
        operation_summary="[可用] 删除模型参数",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['pid'],
            properties={
                'pid': openapi.Schema(type=openapi.TYPE_INTEGER, description="模型参数ID"),
            },
        ),
        responses={
            200: DataModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    @csrf_exempt
    def post(self, request):
        pid = request.data.get("pid")
        if pid is None:
            return Response({"code": 201, "msg": "请求参数错误...."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            param = DataModelParam.objects.get(id=pid)
            param.delete()
            return Response({"code": 200, "msg": "模型参数删除成功"}, status=status.HTTP_200_OK)
        except DataModelParam.DoesNotExist:
            return Response({"code": 201, "msg": "模型参数不存在"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"code": 202, "msg": "系统错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataParamDetailApiView(generics.GenericAPIView):
    serializer_class = DataModelParamDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='获取单个模型参数详情',
        operation_summary="获取单个模型参数详情",
        manual_parameters=[
            openapi.Parameter(
                name="pid",
                in_=openapi.IN_QUERY,
                description="模型参数ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: DataModelParamDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        pid = request.GET.get("pid", None)
        if pid:
            try:
                param = DataModelParam.objects.get(id=pid)
                data = model_to_dict(param)
                return Response({"code": 200, "data": data}, status=status.HTTP_200_OK)
            except DataModelParam.DoesNotExist:
                return Response({"code": 201, "msg": "模型参数不存在"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"code": 202, "msg": "系统错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"code": 201, "msg": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)


# class OpenapiFormatAPI(generics.GenericAPIView):
#     serializer_class = DataModelSerializer
#
#     @swagger_auto_schema(
#         operation_description='GET /dataapp/format/',
#         operation_summary="生成 OpenAPI 格式文档",
#         manual_parameters=[
#             openapi.Parameter('data_model_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True, description='数据模型ID'),
#         ],
#         responses={
#             200: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'swagger': openapi.Schema(type=openapi.TYPE_STRING),
#                 }
#             ),
#             400: "请求失败",
#             404: "数据模型未找到",
#         },
#         tags=['datamodel']
#     )
#     def get(self, request, *args, **kwargs):
#         data_model_id = request.query_params.get('data_model_id')
#
#         if not data_model_id:
#             return Response({"error": "缺少数据模型ID"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             data_model = DataModel.objects.get(id=data_model_id)
#             params = data_model.params  # 获取参数
#
#             # 调用 generate_swagger 函数生成 OpenAPI 文档
#             swagger_json = self.generate_swagger(data_model)
#             return Response(json.loads(swagger_json), status=status.HTTP_200_OK)
#
#         except DataModel.DoesNotExist:
#             return Response({"error": "数据模型未找到"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#     def generate_swagger(self, data_model):
#         # 从完整 URL 中分割出服务器地址和路径
#         full_url = data_model.url
#         url_parts = full_url.split('/', 3)  # 分割出协议、主机和路径
#         server_url = f"{url_parts[0]}//{url_parts[2]}"  # server 是协议和主机部分
#         path = f"/{url_parts[3]}" if len(url_parts) > 3 else "/"
#
#         # 填充 OpenAPI 文档
#         openapi_doc = {
#             "openapi": "3.0.1",
#             "info": {
#                 "title": "Swagger",
#                 "description": "外部数据接口API",
#                 "version": "1.0.0"
#             },
#             "tags": [
#                 {
#                     "name": data_model.name,
#                     "description": data_model.desc
#                 }
#             ],
#             "servers": [
#                 {
#                     "url": server_url,
#                     "description": "本地开发服务器"
#                 }
#             ],
#             "paths": {
#                 path: {
#                     self.get_request_method(data_model.req_type): {
#                         "summary": data_model.name,
#                         "deprecated": False,
#                         "description": data_model.function or "",
#                         "tags": [data_model.name],
#                         "parameters": [],
#                         "responses": {
#                             "200": {
#                                 "description": "成功响应",
#                                 "content": {
#                                     "application/json": {
#                                         "schema": {
#                                             "type": "object",
#                                             "properties": {
#                                                 "code": {
#                                                     "type": "integer",
#                                                     "description": "响应状态码"
#                                                 },
#                                                 "message": {
#                                                     "type": "string",
#                                                     "description": "响应信息"
#                                                 },
#                                                 "data": {
#                                                     "type": "object",
#                                                     "description": "返回的数据",
#                                                     "additionalProperties": True  # 允许任意属性
#                                                 }
#                                             },
#                                             "required": ["code", "data"]
#                                         },
#                                         "examples": {
#                                             "example1": {
#                                                 "summary": "成功示例",
#                                                 "value": {
#                                                     "code": 200,
#                                                     "message": "请求成功",
#                                                     "data": {
#                                                         "exampleField1": "exampleValue1",
#                                                         "exampleField2": 123
#                                                     }
#                                                 }
#                                             }
#                                         }
#                                     }
#                                 },
#                                 "security": []
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#
#         # 获取相关参数
#         params = data_model.params.all()
#         for param in params:
#             openapi_doc["paths"][path][self.get_request_method(data_model.req_type)]["parameters"].append({
#                 "name": param.name,
#                 "in": "query",
#                 "description": param.desc or "",
#                 "required": param.necessary == 1,
#                 "schema": {
#                     "type": param.type if param.type else "string"
#                 }
#             })
#
#         return json.dumps(openapi_doc, ensure_ascii=False, indent=4)
#
#     def get_request_method(self, req_type):
#         # 将整数请求方式转换为字符串
#         return 'post' if req_type == 0 else 'get' if req_type == 1 else None

# class OpenapiFormatAPI(generics.GenericAPIView):
#     serializer_class = DataModelSerializer

#     @swagger_auto_schema(
#         operation_description='GET /dataapp/format/',
#         operation_summary="生成 OpenAPI 格式文档",
#         manual_parameters=[
#             openapi.Parameter('data_model_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True, description='数据模型ID'),
#         ],
#         responses={
#             200: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'swagger': openapi.Schema(type=openapi.TYPE_STRING),
#                 }
#             ),
#             400: "请求失败",
#             404: "数据模型未找到",
#         },
#         tags=['datamodel']
#     )
#     def get(self, request, *args, **kwargs):
#         data_model_id = request.query_params.get('data_model_id')

#         if not data_model_id:
#             return Response({"error": "缺少数据模型ID"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             data_model = DataModel.objects.get(id=data_model_id)
#             # if not data_model.params.exists():
#             #     return Response({"error": "模型参数未关联"}, status=status.HTTP_400_BAD_REQUEST)
#             # 调用 generate_swagger 函数生成 OpenAPI 文档
#             swagger_json = self.generate_swagger(data_model)
#             return Response(json.loads(swagger_json), status=status.HTTP_200_OK)

#         except DataModel.DoesNotExist:
#             return Response({"error": "数据模型未找到"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     def generate_swagger(self, data_model):
#         # 从完整 URL 中分割出服务器地址和路径
#         full_url = data_model.url
#         url_parts = full_url.split('/', 3)
#         server_url = f"{url_parts[0]}//{url_parts[2]}"
#         path = f"/{url_parts[3]}" if len(url_parts) > 3 else "/"

#         # 填充 OpenAPI 文档
#         openapi_doc = {
#             "openapi": "3.0.1",
#             "info": {
#                 "title": "Swagger",
#                 "description": "外部数据接口API",
#                 "version": "1.0.0"
#             },
#             "tags": [
#                 {
#                     "name": data_model.name,
#                     "description": data_model.desc or None
#                 }
#             ],
#             "servers": [
#                 {
#                     "url": server_url,
#                     "description": "本地开发服务器"
#                 }
#             ],
#             "paths": {
#                 path: {
#                     self.get_request_method(data_model.req_type): {
#                         "summary": data_model.name,
#                         "deprecated": False,
#                         "description": data_model.function or "",
#                         "tags": [data_model.name],
#                         "requestBody": {
#                             "required": True,
#                             "content": {
#                                 "application/json": {
#                                     "schema": {
#                                         "type": "object",
#                                         "properties": {},
#                                         "required": []
#                                     }
#                                 }
#                             }
#                         },
#                         "responses": {
#                             "200": {
#                                 "description": "成功响应",
#                                 "content": {
#                                     "application/json": {
#                                         "schema": {
#                                             "type": "object",
#                                             "properties": {
#                                                 "code": {
#                                                     "type": "integer",
#                                                     "description": "响应状态码"
#                                                 },
#                                                 "message": {
#                                                     "type": "string",
#                                                     "description": "响应信息"
#                                                 },
#                                                 "data": {
#                                                     "type": "object",
#                                                     "description": "返回的数据",
#                                                     "additionalProperties": True
#                                                 }
#                                             },
#                                             "required": ["code", "data"]
#                                         },
#                                         "examples": {
#                                             "example1": {
#                                                 "summary": "成功示例",
#                                                 "value": {
#                                                     "code": 200,
#                                                     "message": "请求成功",
#                                                     "data": {
#                                                         "exampleField1": "exampleValue1",
#                                                         "exampleField2": 123
#                                                     }
#                                                 }
#                                             }
#                                         }
#                                     }
#                                 },
#                                 "security": []
#                             }
#                         }
#                     }
#                 }
#             }
#         }

#         # 获取相关参数
#         params = data_model.params.all()
#         if params:
#             for param in params:
#                 # 添加到请求体的 properties
#                 openapi_doc["paths"][path][self.get_request_method(data_model.req_type)]["requestBody"]["content"]["application/json"]["schema"]["properties"][param.name] = {
#                     "type": param.type if param.type else "string"
#                 }

#                 # 如果该参数是必要的，则添加到 required 列表
#                 if param.necessary == 1:
#                     openapi_doc["paths"][path][self.get_request_method(data_model.req_type)]["requestBody"]["content"]["application/json"]["schema"]["required"].append(param.name)

#         return json.dumps(openapi_doc, ensure_ascii=False, indent=4)

#     def get_request_method(self, req_type):
#         return 'post' if req_type == 0 else 'get' if req_type == 1 else None

class OpenapiFormatAPI(generics.GenericAPIView):
    serializer_class = DataModelSerializer

    @swagger_auto_schema(
        operation_description='GET /dataapp/format/',
        operation_summary="生成 OpenAPI 格式文档",
        manual_parameters=[
            openapi.Parameter('data_model_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True,
                              description='数据模型ID'),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'swagger': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: "请求失败",
            404: "数据模型未找到",
        },
        tags=['datamodel']
    )
    def get(self, request, *args, **kwargs):
        data_model_id = request.query_params.get('data_model_id')

        if not data_model_id:
            return Response({"error": "缺少数据模型ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_model = DataModel.objects.get(id=data_model_id)
            # 打印模型信息
            # print("模型信息:")
            # print(f"ID: {data_model.id}")
            # print(f"名称: {data_model.name}")
            # print(f"编号: {data_model.no}")
            # print(f"功能: {data_model.function}")
            # print(f"描述: {data_model.desc}")
            # print(f"URL: {data_model.url}")
            # print(f"业务标签: {data_model.business_tag}")
            # print(f"版本号: {data_model.version}")
            # print(f"请求方式: {data_model.req_type}")
            # print(f"激活状态: {data_model.activate}")
            # print(f"创建作者ID: {data_model.user_id}")
            # print(f"创建作者名称: {data_model.user_name}")
            # print(f"更新时间: {data_model.update_time}")
            # print(f"创建时间: {data_model.create_time}")
            # 调用 generate_swagger 函数生成 OpenAPI 文档
            swagger_json = self.generate_swagger(data_model)
            return Response(json.loads(swagger_json), status=status.HTTP_200_OK)

        except DataModel.DoesNotExist:
            return Response({"error": "数据模型未找到"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def generate_swagger(self, data_model):
        # 从完整 URL 中分割出服务器地址和路径
        full_url = data_model.url
        url_parts = full_url.split('/', 3)
        # 确保 URL 部分有足够的元素
        if len(url_parts) < 3:
            raise ValueError("URL 格式不正确，无法解析服务器地址和路径")
        server_url = f"{url_parts[0]}//{url_parts[2]}"
        path = f"/{url_parts[3]}" if len(url_parts) > 3 else "/"

        # 填充 OpenAPI 文档
        openapi_doc = {
            "openapi": "3.0.1",
            "info": {
                "title": "Swagger",
                "description": "外部数据接口API",
                "version": "1.0.0"
            },
            "tags": [
                {
                    "name": data_model.name,
                    "description": data_model.desc or None
                }
            ],
            "servers": [
                {
                    "url": server_url,
                    "description": "本地开发服务器"
                }
            ],
            "paths": {
                path: {
                    self.get_request_method(data_model.req_type): {
                        "summary": data_model.name,
                        "deprecated": False,
                        "description": data_model.function or "",
                        "tags": [data_model.name],
                        "responses": {
                            "200": {
                                "description": "成功响应",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "code": {
                                                    "type": "integer",
                                                    "description": "响应状态码"
                                                },
                                                "message": {
                                                    "type": "string",
                                                    "description": "响应信息"
                                                },
                                                "data": {
                                                    "type": "array" if self.get_request_method(
                                                        data_model.req_type) == 'get' else "object",
                                                    "description": "返回的数据",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "integer",
                                                                "description": "数据模型ID"
                                                            },
                                                            "name": {
                                                                "type": "string",
                                                                "description": "数据模型名称"
                                                            },
                                                            "desc": {
                                                                "type": "string",
                                                                "description": "数据模型描述"
                                                            }
                                                        },
                                                        "required": [
                                                            "id",
                                                            "name"
                                                        ]
                                                    } if self.get_request_method(data_model.req_type) == 'get' else {}
                                                }
                                            },
                                            "required": ["code", "data"]
                                        },
                                        "examples": {
                                            "example1": {
                                                "summary": "成功示例",
                                                "value": {
                                                    "code": 200,
                                                    "message": "请求成功",
                                                    "data": [
                                                        {
                                                            "id": 1,
                                                            "name": "模型1",
                                                            "desc": "这是第一个数据模型"
                                                        },
                                                        {
                                                            "id": 2,
                                                            "name": "模型2",
                                                            "desc": "这是第二个数据模型"
                                                        }
                                                    ]
                                                }
                                            }
                                        }
                                    }
                                },
                                "security": []
                            }
                        },
                        "parameters": []  # 初始化参数列表
                    }
                }
            }
        }

        # 获取相关参数
        params = data_model.params.all()
        for param in params:
            if self.get_request_method(data_model.req_type) == 'get':
                # 添加到 GET 请求的参数列表
                openapi_doc["paths"][path][self.get_request_method(data_model.req_type)]["parameters"].append({
                    "name": param.name,
                    "in": "query",
                    "required": param.necessary == 1,
                    "schema": {
                        "type": param.type if param.type else "string"
                    }
                })
            elif self.get_request_method(data_model.req_type) == 'post':
                # 添加到 POST 请求体的 properties
                openapi_doc["paths"][path][self.get_request_method(data_model.req_type)]["requestBody"]["content"][
                    "application/json"]["schema"]["properties"][param.name] = {
                    "type": param.type if param.type else "string"
                }

                # 如果该参数是必要的，则添加到 required 列表
                if param.necessary == 1:
                    openapi_doc["paths"][path][self.get_request_method(data_model.req_type)]["requestBody"]["content"][
                        "application/json"]["schema"]["required"].append(param.name)

        return json.dumps(openapi_doc, ensure_ascii=False, indent=4)

    def get_request_method(self, req_type):
        return 'post' if req_type == 0 else 'get' if req_type == 1 else None
    






class AppAPIList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = KgBaseResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /dataapp/appapilist',
        operation_summary="获取应用功能列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "keyword",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="关键词模糊搜索",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='结束时间', ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgBaseResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        
        querySet = AppAPIModel.objects
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(appname__contains="{}".format(keyword))
        if start_time:
            querySet = querySet.filter(create_time__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(create_time__lt="{}".format(end_time))
        querySet = querySet.all().order_by('-update_time')
        # querySet = KgDoc.objects.all()
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
        
        retData = []
        for obj in objs:
            retObj = model_to_dict(obj, exclude=['toolapis'])
            retObj['toollist'] = obj.toollist
            retData.append(retObj)
        data['data'] = retData
        data['code'] = 200
        data['total'] = len(querySet)
        serializers = KgBaseResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)



class AppAPIAddView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)

    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 新增应用接口功能',
        operation_description='GET /dataapp/appapiadd',
        manual_parameters=[
            openapi.Parameter(
                name='appname',
                in_=openapi.IN_FORM,
                description='应用名称',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='appdesc',
                in_=openapi.IN_FORM,
                description='应用描述',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='appurl',
                in_=openapi.IN_FORM,
                description='应用URL',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='appkey',
                in_=openapi.IN_FORM,
                description='应用APPKEY',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='tip_type',
                in_=openapi.IN_FORM,
                description='0(查询分析)|1（其他）',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='tip_ctt',
                in_=openapi.IN_FORM,
                description='提示词描述',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='toolids',
                in_=openapi.IN_FORM,
                items=openapi.Items(openapi.TYPE_INTEGER),
                description='工具接口IDs',
                type=openapi.TYPE_ARRAY
            ),
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_FORM,
                description='创建作者',
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: KgBaseResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['datamodel']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200}
        appname = request.data.get("appname", None)
        appdesc = request.data.get("appdesc", None)
        appurl = request.data.get("appurl", None)
        appkey = request.data.get("appkey", None)
        tip_type = request.data.get("tip_type", None)
        tip_ctt = request.data.get("tip_ctt", None)
        toolids = request.data.get("toolids", None)
        user_id = request.data.get("user_id", None)

        if appname is None or appkey is None or appdesc is None or appurl is None or tip_type is None or tip_ctt is None or toolids is None or user_id is None or not isinstance(toolids, list):
            data["code"] = 201
            data["msg"] = "参数错误"
            serializers = KgBaseResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data["code"] = 201
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 201, "msg": "用户ID不存在！！！"}
            serializers = KgBaseResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        tmpapp = AppAPIModel.objects.create(
            appname=appname,
            appdesc=appdesc,
            appurl=appurl,
            appkey=appkey,
            tip_type=tip_type,
            tip_ctt=tip_ctt,
            kg_user_id=tmpuser
        )
        for t in toolids:
            tmptool = DataModel.objects.get(id=t)
            if tmptool:
                tmpapp.toolapis.add(tmptool)
        tmpapp.save()
        data = {"code": 200, "msg": "应用工具创建成功"}
        serializers = KgBaseResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
