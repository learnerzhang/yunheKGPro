from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import DataModel  # 确保导入您的接口
from userapp.models import User
from .serializers import DataModelSerializer
from django.utils import timezone
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import NotFound, ValidationError
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
import json
import datetime
import requests
from yunheKGPro import CsrfExemptSessionAuthentication


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
            openapi.Parameter(
                'id',
                openapi.IN_FORM,
                description='接口id',
                type=openapi.TYPE_STRING,
                required=False
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
                'user_id',
                openapi.IN_FORM,
                description='创建作者ID',
                type=openapi.TYPE_INTEGER,
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
                'user_name',
                openapi.IN_FORM,
                description='创建用户名称',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'update_time',
                openapi.IN_FORM,
                description='更新时间',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'create_time',
                openapi.IN_FORM,
                description='创建时间',
                type=openapi.TYPE_STRING,
                required=False
            ),
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
            activate= int(activate)
            # 验证激活状态的值
            if activate not in [0, 1]:
                return Response({
                    'code': 400,
                    'msg': '激活状态只能是0或1'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取可选参数
            # user_id = request.data.get('user_id')
            # if user_id:
            #     try:
            #         user = User.objects.get(id=user_id)
            #     except User.DoesNotExist:
            #         return Response({
            #             'code': 400,
            #             'msg': '用户不存在'
            #         }, status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     user = None

            # 创建新数据接口
            model = DataModel(
                name=name,
                req_type=req_type,
                url=url,
                activate=activate,
                function=request.data.get('function'),
                desc=request.data.get('desc'),
                version=request.data.get('version'),
                #kg_user_id=user,
                no=request.data.get('no'),  # 可选
                create_time=request.data.get('create_time', datetime.datetime.now()),
                update_time=request.data.get('update_time', datetime.datetime.now())
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
            model.update_time = datetime.datetime.now()  # 更新当前时间

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
        curl_command = ''
        try:
            name = request.query_params.get('name')
            req_type = request.query_params.get('req_type')
            url = request.query_params.get('url')
            activate = request.query_params.get('activate')
            params = request.query_params.get('params', '{}')  # 默认空参数
            headers = request.query_params.get('headers', '{}')  # 默认空头

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
            # 查找对应数据接口
            # model = self.get_queryset().filter(name=name, req_type=req_type, url=url, activate=activate).first()
            # if model is None:
            #     raise NotFound("未找到该数据接口")
            # 解析请求参数和请求头
            params = json.loads(params) if params else {}
            headers = json.loads(headers) if headers else {}
            print("###############################",headers)
            # 构造 curl 命令
            curl_command = f'curl -X {"GET" if req_type == 1 else "POST"} "{url}" -H "accept: application/json"'
            for key, value in headers.items():
                curl_command += f' -H "{key}: {value}"'
            #if req_type == 0:  # POST 请求，添加参数
            curl_command += f' -d \'{json.dumps(params)}\''

            # 根据请求方式发送请求
            if req_type == 1:  # GET 请求
                response = requests.get(url, params=params, headers=headers)
            else:  # POST 请求
                response = requests.post(url, data=params, headers=headers)

            # 返回实际响应内容
            return Response({
                'code': response.status_code,
                'msg': '测试成功',
                'data': response.json(),  # 假设响应是 JSON 格式
                'curl_command': curl_command
            }, status=response.status_code)

        except ValidationError as e:
            return Response({
                'code': 400,
                'msg': str(e),
               'curl_command': curl_command
            }, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({
                'code': 404,
                'msg': str(e),
                'curl_command': curl_command
            }, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({
                'code': 400,
                'msg': "请求参数或请求头格式错误",
                'curl_command': curl_command
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'code': 400,
                'msg': str(e),
                'curl_command': curl_command
            }, status=status.HTTP_400_BAD_REQUEST)