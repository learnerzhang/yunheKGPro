from django.contrib.auth.hashers import check_password, make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
from yunheKGPro import settings
from userapp.serializers import *
from userapp.models import User, Menu, Role
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import BasicAuthentication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from yunheKGPro import CsrfExemptSessionAuthentication
from django.utils import timezone
from django.core.cache import cache
import PIL
import random
import string
import os
import io
from PIL import ImageDraw, ImageFont, ImageFilter
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

class KgUserList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    serializer_class = KgUserResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapp/userlist/',
        operation_summary="获取所有用户列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgUserResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)

        querySet = User.objects.all()

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
        kds = UserSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgUserResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class UserDetailApiView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    serializer_class = KgUserResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapp/Detail',
        operation_summary="获取用户详细信息",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "uid",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="用户ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        uid = request.GET.get("uid", None)
        if uid:
            try:
                tmpuser = User.objects.get(id=uid)
                data['data'] = {'id': tmpuser.id, 'username': tmpuser.username, 'telephone': tmpuser.telephone,
                                'email': tmpuser.email}
                serializers = KgUserDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgUserDetailResponseSerializer(data={"code": 201, "msg": "不存在该用户"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgUserDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class UserRegistApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 用户注册接口',
        operation_description='POST /userapi/regist',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="用户名"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="密码"),
                'telephone': openapi.Schema(type=openapi.TYPE_NUMBER, description="电话"),
            },
        ),
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):
        print("regist:", request.data)
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        telephone = request.data.get("telephone", None)
        captcha = request.data.get('captcha', None)
        
        if username is None or password is None:
            serializers = KgUserDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        cache_key = 'captcha_'
        ck = cache.get(cache_key)
        print("captcha:", ck)
        if str(ck).lower() != str(captcha).lower():
            data = {'success': False, 'msg': '验证码错误', "code": 201}
            serializers = KgUserDetailResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        

        user = User.objects.filter(username=username).first()
        if not user:
            tmpuser = User.objects.create(username=username, password=make_password(password), telephone=telephone)
            tmpuser.save()
            serializers = KgUserDetailResponseSerializer(
                data={"code": 200, "msg": "注册成功", "data": model_to_dict(tmpuser)},
                many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            serializers = KgUserDetailResponseSerializer(
                data={"code": 201, "msg": "用户名已经存在!", },
                many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class UserDeleteApiView(generics.GenericAPIView):

    @swagger_auto_schema(
        operation_summary='[可用] 删除用户',
        operation_description='POST /userapi/delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_INTEGER, description="用户ID"),
            },
        ),
        responses={
            200: BaseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):

        uid = request.data.get("uid", None)
        if uid:
            try:
                User.objects.get(id=uid).delete()
                serializers = BaseSerializer(data={"code": 200, "msg": "删除用户成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = BaseSerializer(data={"code": 201, "msg": "不存在该用户"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = BaseSerializer(data={"code": 202, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class UserAddorUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新增or更新用户单元',
        operation_description='POST /userapi/AddorUpdate',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_INTEGER, description="用户ID"),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="用户名"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="密码"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="姓氏"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="名字"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="名字"),
                'sex': openapi.Schema(type=openapi.TYPE_INTEGER, description="性别"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="邮箱"),
                'telephone': openapi.Schema(type=openapi.TYPE_NUMBER, description="电话"),
                'icon': openapi.Schema(type=openapi.TYPE_STRING, description="头像"),
                'role': openapi.Schema(type=openapi.TYPE_INTEGER, description="角色"),
                'is_staff': openapi.Schema(type=openapi.TYPE_INTEGER, description="是否可以登录到此管理站点"),
                'is_active': openapi.Schema(type=openapi.TYPE_INTEGER, description="是否启用"),
            },
        ),
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):
        uid = request.data.get("uid", None)
        username = request.data.get("username", None)
        last_name = request.data.get("lastname", None)
        first_name = request.data.get("firstname", None)
        password = request.data.get("password", None)
        name = request.data.get("name", None)
        sex = request.data.get("sex", None)
        email = request.data.get("email", None)
        telephone = request.data.get("telephone", None)
        icon = request.data.get("icon", None)
        role = request.data.get("role", None)
        is_staff = request.data.get("isstaff", None)
        is_active = request.data.get("isactive", None)
        data = {}

        def setAttrs(user: User):
            """
                属性赋值
            """
            for key in request.data:
                if key in ['sex', 'role', 'isstaff', 'isactive']:
                    user.__setattr__(key, int(request.data[key]))
                elif key in ['password']:
                    user.__setattr__(key, make_password(request.data[key]))
                else:
                    user.__setattr__(key, request.data[key])
        try:
            if uid is None:
                if username and password:
                    tmp = User.objects.create(username=username, password=make_password(password))
                    setAttrs(tmp)
                    tmp.save()
                    data['data']=model_to_dict(tmp)
                    data['code'] = 200
                    data['msg'] = "新增成功..."
                else:
                    data['code'] = 201
                    data['msg'] = "新增参数错误！！！"
            else:
                try:
                    tmp = User.objects.get(id=uid)
                    setAttrs(tmp)
                    tmp.save()
                    data['data']=model_to_dict(tmp)
                    data['code'] = 200
                    data['msg'] = "更新成功.."
                except:
                    data['code'] = 201
                    data['msg'] = "不存在该用户！！！"
        except:
            data['code'] = 202
            data['msg'] = "参数错误！！！"

        UserSer = KgUserDetailResponseSerializer(data=data, many=False)
        UserSer.is_valid()
        return Response(UserSer.data, status=status.HTTP_200_OK)


class UserLoginApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 用户登录接口',
        operation_description='POST /userapi/login',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="用户名"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="密码"),
            },
        ),
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):

        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or password is None:
            serializers = KgUserDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        user = User.objects.filter(username=username).first()
        if not user:
            serializers = KgUserDetailResponseSerializer(data={"code": 202, "msg": "用户名不存在"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            if check_password(password, user.password):
                request.session["username"] = username
                request.session["uid"] = user.id
                login(request, user)
                serializers = KgUserDetailResponseSerializer(data={'success': True, 'msg': '登录成功', "code": 200, 'data': 
                                                            {
                                                                "uid": request.session['_auth_user_id'], 
                                                                "username": username, 
                                                                "superuser": user.is_superuser, 
                                                                "token": request.session['_auth_user_hash'], 
                                                            }}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                serializers = KgUserDetailResponseSerializer(data={"code": 202, "msg": "密码错误!"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)


class UserLogoutApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 用户注销登录接口',
        operation_description='POST /userapi/logout',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={

            },
        ),
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):
        if request.session.get("username"):
            del request.session["username"]
            del request.session["uid"]
            request.session.flush()
        serializers = KgUserDetailResponseSerializer(data={"code": 200, "msg": "退出登录成功!"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class UserLoginStatusApiView(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapi/status/',
        operation_summary="获取用户的登录状态",
        # 接口参数 GET请求参数
        manual_parameters=[
        ],
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        if request.session.get("uid"):
            uid = request.session.get("uid")
            user = User.objects.get(id=uid)
            data['data'] = model_to_dict(user, fields=['id', 'username'])
        else:
            data = {"code": 201, "msg": "用户未登录"}

        serializers = KgUserDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class RoleList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    serializer_class = KgUserResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapp/RoleList/',
        operation_summary="获取所有角色列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgRoleResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)

        temRoles = Role.objects.all()
        
        data['total'] = len(temRoles)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(temRoles, pageSize)
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)

        kds = RoleSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgRoleResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class RoleDetailApiView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    serializer_class = KgUserResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapp/roleDetail',
        operation_summary="获取角色详细信息",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "rid",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="角色ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: KgRoleDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request):

        data = {"code": 200}
        rid = request.GET.get("rid", None)
        if rid:
            try:
                tmpRole = Role.objects.get(id=rid)
                role = model_to_dict(tmpRole)

                menus = KgMenuSerializer(data=tmpRole.menus_list, many=True)
                menus.is_valid()
                role['menus'] = menus.data

                data['data'] = role
                serializers = KgRoleDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgRoleDetailResponseSerializer(data={"code": 201, "msg": "不存在该角色"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgRoleDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class RoleDeleteApiView(generics.GenericAPIView):

    @swagger_auto_schema(
        operation_summary='[可用] 删除角色',
        operation_description='POST /userapi/roleDelete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'rid': openapi.Schema(type=openapi.TYPE_INTEGER, description="角色ID"),
            },
        ),
        responses={
            200: KgRoleDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):

        rid = request.data.get("rid", None)
        if rid:
            try:
                Role.objects.get(id=rid).delete()
                serializers = KgRoleDetailResponseSerializer(data={"code": 200, "msg": "删除角色成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgRoleDetailResponseSerializer(data={"code": 201, "msg": "不存在该角色"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgRoleDetailResponseSerializer(data={"code": 202, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class RoleAddorUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgRoleDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新增or更新角色',
        operation_description='POST /userapi/roleAddorUpdate',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'rid': openapi.Schema(type=openapi.TYPE_INTEGER, description="角色ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="角色名"),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="用户ID"),
                'remark': openapi.Schema(type=openapi.TYPE_STRING, description="备注"),
                'activate': openapi.Schema(type=openapi.TYPE_INTEGER, description="激活状态"),
                'updated_at': openapi.Schema(type=openapi.FORMAT_DATETIME, description="更新时间"),
                'created_at': openapi.Schema(type=openapi.FORMAT_DATETIME, description="创建时间"),
            },
        ),
        responses={
            200: KgRoleDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):
        rid = request.data.get("rid", None)
        name = request.data.get("username", None)
        user_id = request.data.get("lastname", None)
        remark = request.data.get("firstname", None)
        activate = request.data.get("password", None)
        updated_at = request.data.get("name", None)
        created_at = request.data.get("sex", None)

        data = {}

        def setAttrs(user: User):
            """
                属性赋值
            """
            for key in request.data:
                if key in ['rid', 'user_id', 'activate']:
                    user.__setattr__(key, int(request.data[key]))
                else:
                    user.__setattr__(key, request.data[key])
        try:
            if rid is None:
                if name:
                    tmp = Role.objects.create(name=name)
                    setAttrs(tmp)
                    tmp.save()
                    data['data']=model_to_dict(tmp)
                    data['code'] = 200
                    data['msg'] = "新增成功..."
                else:
                    data['code'] = 201
                    data['msg'] = "新增参数错误！！！"
            else:
                try:
                    tmp = Role.objects.get(id=rid)
                    setAttrs(tmp)
                    tmp.save()

                    role = model_to_dict(tmp)
                    menus = KgMenuSerializer(data=tmp.menus_list, many=True)
                    menus.is_valid()
                    role['menus'] = menus.data

                    data['data'] = role
                    data['code'] = 200
                    data['msg'] = "更新成功.."
                except:
                    data['code'] = 201
                    data['msg'] = "不存在该角色！！！"
        except:
            data['code'] = 202
            data['msg'] = "参数错误！！！"

        RoleSer = KgRoleDetailResponseSerializer(data=data, many=False)
        RoleSer.is_valid()
        return Response(RoleSer.data, status=status.HTTP_200_OK)


class KgMenuList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    serializer_class = KgMenuResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapi/menus',
        operation_summary="获取默认菜单列表",
        # 接口参数 GET请求参数
        manual_parameters=[
        ],
        tags=['appuser'])
    def get(self, request, *args, **kwargs):
        def arr2tree(source, parent):
            tree = []
            for item in source:
                if item['father_id'] == parent:
                    item['children'] = arr2tree(source, item['id'])
                    tree.append(item)
            return tree

        data = {"code": 200}
        menus = Menu.objects.all().order_by('-updated_at')
        tmpms = [model_to_dict(m) for m in menus]
        data['menus'] = arr2tree(tmpms, 0)
        serializers = KgMenuResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgMenuByUserList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    serializer_class = KgMenuResponseSerializer

    @swagger_auto_schema(
        operation_description='GET userapi/menusByUser',
        operation_summary="[可用] 获取用户授权的菜单列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "uid",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="用户ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
        ],
        tags=['appuser'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        uid = request.GET.get("uid", None)
        if uid is None:
            data = {"code": 201, "msg": "用户参数错误！", "menus": []}
            serializers = KgMenuResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        try:
            tmpRole = Role.objects.filter(user_id=uid).first()
        except:
            data = {"code": 202, "msg": "系统错误！", "menus": []}
            serializers = KgMenuResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        def arr2tree(source, parent):
            tree = []
            for item in source:
                if item['father_id'] == parent:
                    item['children'] = arr2tree(source, item['id'])
                    tree.append(item)
            return tree

        if tmpRole:
            data['menus'] = arr2tree(tmpRole.menus_list, 0)
            serializers = KgMenuResponseSerializer(data=data, many=False)
            serializers.is_valid()
        else:
            data = {"code": 200, "msg": "该用户不存在角色权限！", "menus": []}
            serializers = KgMenuResponseSerializer(data=data, many=False)
            serializers.is_valid()

        return Response(serializers.data, status=status.HTTP_200_OK)

class KgMenuAddByUser(generics.GenericAPIView):
    serializer_class = KgMenuResponseSerializer  # 如果需要，可以创建另一个序列化器

    @swagger_auto_schema(
        operation_description='POST userapi/menusByUser',
        operation_summary="[可用] 为用户添加菜单",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uid', 'title', 'menu_type'],  # 必填项
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户ID'),
                'menu_type': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='菜单类型 0=目录, 1=菜单, 2=按钮',
                    enum=[0, 1, 2],
                    default=0  # 假设默认是菜单
                ),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='路由名称'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='菜单名称'),
                'auth_ctt': openapi.Schema(type=openapi.TYPE_STRING, description='权限标识', blank=True),
                'icon': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='菜单图标',
                    default="ant-design:fund-projection-screen-outlined",
                    blank=True
                ),
                'img': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='菜单图片',
                    default="/resource/image/menu/default.png",
                    blank=True
                ),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description='路由地址', blank=True),
                'redirect': openapi.Schema(type=openapi.TYPE_STRING, description='重定向', blank=True),
                'component': openapi.Schema(type=openapi.TYPE_STRING, description='组件地址', blank=True),
                'rank': openapi.Schema(type=openapi.TYPE_INTEGER, description='排序', default=0, blank=True),
                'father_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='父级菜单ID', default=0),
                'activate': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='激活状态 0=非激活, 1=激活',
                    enum=[0, 1],
                    default=1
                ),
                'hideMenu': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='是否显示 0=隐藏, 1=显示',
                    enum=[0, 1],
                    default=1
                ),
                'updated_at': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='更新时间',
                    format=openapi.FORMAT_DATETIME,
                    default=timezone.now().isoformat()
                ),
                'created_at': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='创建时间',
                    format=openapi.FORMAT_DATETIME,
                    default=timezone.now().isoformat()
                ),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description='菜单描述', blank=True),
            },
        ),
        tags=['appuser']
    )
    def post(self, request, *args, **kwargs):
        # 获取请求数据
        uid = request.data.get("uid")
        menu_type = request.data.get("menu_type", 0)
        title = request.data.get("title")
        desc = request.data.get("desc", "")
        father_id = request.data.get("father_id", 0)
        auth_ctt = request.data.get("auth_ctt", "")
        icon = request.data.get("icon", "ant-design:fund-projection-screen-outlined")
        img = request.data.get("img", "/resource/image/menu/default.png")
        path = request.data.get("path", "")
        redirect = request.data.get("redirect", "")
        component = request.data.get("component", "")
        rank = request.data.get("rank", 0)
        activate = request.data.get("activate", 1)
        hideMenu = request.data.get("hideMenu", 1)
        updated_at = request.data.get("updated_at", timezone.now().isoformat())
        created_at = request.data.get("created_at", timezone.now().isoformat())

        if uid is None or title is None or menu_type is None:
            return Response({"code": 400, "msg": "缺少必要参数！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 添加新菜单
            new_menu = Menu.objects.create(
                name=title,
                desc=desc,
                father_id=father_id,
                menu_type=menu_type,  # 使用传入的菜单类型
                title=title,
                auth_ctt=auth_ctt,
                icon=icon,
                img=img,
                path=path,
                redirect=redirect,
                component=component,
                rank=rank,
                activate=activate,
                hideMenu=hideMenu,
                created_at=created_at,
                updated_at=updated_at
            )

            # 将新菜单添加到用户的角色中
            tmpRole = Role.objects.filter(user_id=uid).first()
            if tmpRole:
                tmpRole.menus.add(new_menu)

            return Response({"code": 200, "msg": "菜单添加成功！", "menu_id": new_menu.id},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"code": 500, "msg": "系统错误！", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KgMenuDeleteByUser(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_description='POST userapi/deleteMenu',
        operation_summary="[可用] 删除菜单",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户ID'),
                'menu_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='菜单ID'),
            },
        ),
        tags=['appuser']
    )
    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        menu_id = request.data.get("menu_id")

        if uid is None or menu_id is None:
            return Response({"code": 400, "msg": "缺少必要参数！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 查找用户角色
            role = Role.objects.filter(user_id=uid).first()
            if not role:
                return Response({"code": 403, "msg": "用户没有角色权限！"}, status=status.HTTP_403_FORBIDDEN)

            # 检查菜单是否在角色的菜单列表中
            if not role.menus.filter(id=menu_id).exists():
                return Response({"code": 403, "msg": "用户没有权限删除该菜单！"}, status=status.HTTP_403_FORBIDDEN)

            # 查找菜单并删除
            menu = role.menus.filter(id=menu_id).first()
            if not menu:
                return Response({"code": 404, "msg": "菜单不存在！"}, status=status.HTTP_404_NOT_FOUND)

            # 删除菜单
            menu.delete()

            return Response({"code": 200, "msg": "菜单已成功删除！"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": 500, "msg": "系统错误！", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KgMenuHideByUser(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_description='POST userapi/hideMenu',
        operation_summary="[可用] 隐藏菜单",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_INTEGER, description='用户ID'),
                'menu_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='菜单ID'),
            },
        ),
        tags=['appuser'])
    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        menu_id = request.data.get("menu_id")

        if uid is None or menu_id is None:
            return Response({"code": 400, "msg": "缺少必要参数！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 查找用户角色
            role = Role.objects.filter(user_id=uid).first()
            if not role:
                return Response({"code": 403, "msg": "用户没有角色权限！"}, status=status.HTTP_403_FORBIDDEN)

            # 检查菜单是否在角色的菜单列表中
            if not role.menus.filter(id=menu_id).exists():
                return Response({"code": 403, "msg": "用户没有权限隐藏该菜单！"}, status=status.HTTP_403_FORBIDDEN)

            # 查找菜单
            menu = role.menus.filter(id=menu_id).first()
            if not menu:
                return Response({"code": 404, "msg": "菜单不存在！"}, status=status.HTTP_404_NOT_FOUND)

            # 更新菜单的 hideMenu 状态
            menu.hideMenu = 0  # 设置为隐藏
            menu.save()

            return Response({"code": 200, "msg": "菜单已成功隐藏！"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": 500, "msg": "系统错误！", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class KgMenuUpdateByUser(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_description='PUT userapi/updateMenu',
        operation_summary="[可用] 更新用户菜单",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['uid', 'menu_id', 'menu_type', 'title', 'desc', 'icon', 'img', 'path',
                      'redirect', 'component', 'rank', 'father_id', 'activate', 'hideMenu',
                      'updated_at', 'created_at'],  # 所有字段均为必填项
            properties={
                'uid': openapi.Schema(type=openapi.TYPE_INTEGER, description="用户ID"),
                'menu_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="菜单ID"),
                'menu_type': openapi.Schema(type=openapi.TYPE_INTEGER, description="菜单类型",
                                            default=0, enum=[0, 1, 2]),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="菜单描述", default=""),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="路由名称", default=""),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="菜单名称"),
                'auth_ctt': openapi.Schema(type=openapi.TYPE_STRING, description="权限标识(菜单)", default=""),
                'icon': openapi.Schema(type=openapi.TYPE_STRING, description="菜单图标",
                                       default="ant-design:fund-projection-screen-outlined"),
                'img': openapi.Schema(type=openapi.TYPE_STRING, description="菜单图片",
                                      default="/resource/image/menu/default.png"),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description="路由地址", default=""),
                'redirect': openapi.Schema(type=openapi.TYPE_STRING, description="重定向", default=""),
                'component': openapi.Schema(type=openapi.TYPE_STRING, description="组件地址", default=""),
                'rank': openapi.Schema(type=openapi.TYPE_INTEGER, description="排序", default=0),
                'father_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="父级菜单ID", default=0),
                'activate': openapi.Schema(type=openapi.TYPE_INTEGER, description="激活状态 0|1",
                                           default=1, enum=[0, 1]),
                'hideMenu': openapi.Schema(type=openapi.TYPE_INTEGER, description="是否显示 0|1",
                                           default=1, enum=[0, 1]),
                'updated_at': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="更新时间",
                    format=openapi.FORMAT_DATETIME
                ),
                'created_at': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="创建时间",
                    format=openapi.FORMAT_DATETIME
                ),
            },
        ),
        responses={
            200: KgMenuDetailResponseSerializer(many=False),
            400: "请求失败",
            404: "菜单未找到",
            500: "系统错误",
        },
        tags=['appuser']
    )
    def put(self, request):
        data = request.data

        # 直接获取所有字段
        uid = data.get("uid")
        menu_id = data.get("menu_id")
        menu_type = data.get("menu_type", 0)
        title = data.get("title")
        desc = data.get("desc", "")
        name = data.get("name", "")
        auth_ctt = data.get("auth_ctt", "")
        icon = data.get("icon", "ant-design:fund-projection-screen-outlined")
        img = data.get("img", "/resource/image/menu/default.png")
        path = data.get("path", "")
        redirect = data.get("redirect", "")
        component = data.get("component", "")
        rank = data.get("rank", 0)
        father_id = data.get("father_id", 0)
        activate = data.get("activate", 1)
        hideMenu = data.get("hideMenu", 1)
        created_at = data.get("created_at")
        updated_at = timezone.now()  # 更新当前时间

        # 验证必填项
        if not uid or not title or not menu_id:
            return Response({"code": 400, "msg": "uid、menu_id 和 title 为必填项！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取用户角色
        role = Role.objects.filter(user_id=uid).first()
        if not role:
            return Response({"code": 404, "msg": "用户角色未找到！"}, status=status.HTTP_404_NOT_FOUND)
        if not role.menus.filter(id=menu_id).exists():
            return Response({"code": 403, "msg": "用户没有权限更新该菜单！"}, status=status.HTTP_403_FORBIDDEN)

        # 查找菜单
        try:
            # 更新菜单
            menu = role.menus.filter(id=menu_id).first()
            if not menu:
                return Response({"code": 404, "msg": "菜单未找到！"}, status=status.HTTP_404_NOT_FOUND)

            # 更新所有字段
            menu.menu_type = menu_type
            menu.title = title
            menu.desc = desc
            menu.name = name
            menu.auth_ctt = auth_ctt
            menu.icon = icon
            menu.img = img
            menu.path = path
            menu.redirect = redirect
            menu.component = component
            menu.rank = rank
            menu.father_id = father_id
            menu.activate = activate
            menu.hideMenu = hideMenu
            menu.created_at = created_at  # 如果需要更新创建时间
            menu.updated_at = updated_at  # 更新当前时间
            menu.save()  # 保存更改

            return Response({"code": 200, "msg": "菜单更新成功！"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": 500, "msg": "系统错误！", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KgMenuRetrieveByUser(generics.GenericAPIView):
    serializer_class = KgMenuResponseSerializer
    @swagger_auto_schema(
        operation_description='GET userapi/menusByUser',
        operation_summary="[可用] 根据用户ID和查询字段获取菜单",
        manual_parameters=[
            openapi.Parameter('uid', openapi.IN_QUERY, description='用户ID', type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('query', openapi.IN_QUERY, description='查询字段', type=openapi.TYPE_STRING, required=False),
        ],
        tags=['appuser']
    )
    def get(self, request, *args, **kwargs):
        uid = request.query_params.get("uid")
        query = request.query_params.get("query", "")

        if uid is None:
            return Response({"code": 400, "msg": "缺少用户ID！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取用户角色
            tmpRole = Role.objects.filter(user_id=uid).first()
            if not tmpRole:
                return Response({"code": 404, "msg": "用户角色未找到！"}, status=status.HTTP_404_NOT_FOUND)

            # 查询相关菜单
            menus = Menu.objects.filter(
                title__icontains=query,
                role__in=[tmpRole.id]  # 只获取该用户角色下的菜单
            ).distinct()
            menu_data = [model_to_dict(menu) for menu in menus]
            # 直接构建响应数据
            # menu_data = []
            # for menu in menus:
            #     menu_data.append({
            #         "id": menu.id,
            #         "title": menu.title,
            #         "desc": menu.desc,
            #         "icon": menu.icon,
            #         "img": menu.img,
            #         "path": menu.path,
            #         "redirect": menu.redirect,
            #         "component": menu.component,
            #         "rank": menu.rank,
            #         "father_id": menu.father_id,
            #         "activate": menu.activate,
            #         "hideMenu": menu.hideMenu,
            #         "created_at": menu.created_at,
            #         "updated_at": menu.updated_at,
            #     })

            response_data = {
                "code": 200,
                "msg": "查询成功！",
                "menus": menu_data
            }

            # 创建序列化器实例并验证
            serializer = KgMenuResponseSerializer(data=response_data)
            serializer.is_valid(raise_exception=True)  # 验证数据

            # 返回序列化后的数据
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"code": 500, "msg": "系统错误！", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MenuAddOrUpdateApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgMenuDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 新增or更新菜单单元',
        operation_description='POST /userapi/menuAddOrUpdate',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="菜单ID"),
                'menu_type': openapi.Schema(type=openapi.TYPE_INTEGER, description="菜单类型"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="菜单描述"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="路由名称"),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="菜单名称"),
                'auth_ctt': openapi.Schema(type=openapi.TYPE_STRING, description="权限标识"),
                'img': openapi.Schema(type=openapi.TYPE_STRING, description="菜单图片"),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description="路由地址"),
                'redirect': openapi.Schema(type=openapi.TYPE_STRING, description="重定向"),
                'component': openapi.Schema(type=openapi.TYPE_STRING, description="组件地址"),
                'rank': openapi.Schema(type=openapi.TYPE_INTEGER, description="排序"),
                'father_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="父级菜单目录ID"),
                'activate': openapi.Schema(type=openapi.TYPE_INTEGER, description="激活状态 0|1"),
                'hideMenu': openapi.Schema(type=openapi.TYPE_INTEGER, description="是否显示 0|1"),
            },
        ),
        responses={
            200: KgMenuDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):
        mid = request.data.get("id", None)
        father_id = request.data.get("father_id", None)
        rank = request.data.get("rank", None)
        menu_type = request.data.get("menu_type", None)
        desc = request.data.get("desc", None)
        name = request.data.get("name", None)
        title = request.data.get("title", None)
        auth_ctt = request.data.get("auth_ctt", None)
        img = request.data.get("img", None)
        path = request.data.get("path", None)
        redirect = request.data.get("redirect", None)
        component = request.data.get("component", None)
        activate = request.data.get("activate", None)
        hideMenu = request.data.get("hideMenu", None)
        data = {}

        def setAttrs(menu: Menu):
            """
                属性副职
            """
            for key in request.data:
                if key in ['father_id', 'rank', 'menu_type', 'activate', 'hideMenu']:
                    # print(key, request.data[key])
                    menu.__setattr__(key, int(request.data[key]))
                else:
                    menu.__setattr__(key, request.data[key])
        try:
            if mid is None:
                if title:
                    tmp = Menu.objects.create(title=title)
                    setAttrs(tmp)
                    tmp.save()
                    data['code'] = 200
                    data['msg'] = "新增成功..."
                else:
                    data['code'] = 201
                    data['msg'] = "新增参数错误！！！"
            else:
                try:
                    tmp = Menu.objects.get(id=mid)
                    setAttrs(tmp)
                    tmp.save()
                    data['code'] = 200
                    data['msg'] = "更新成功.."
                except:
                    data['code'] = 201
                    data['msg'] = "不存在该菜单单元！！！"
        except:
            data['code'] = 202
            data['msg'] = "参数错误！！！"

        kgMenuSer = KgMenuDetailResponseSerializer(data=data, many=False)
        kgMenuSer.is_valid()
        return Response(kgMenuSer.data, status=status.HTTP_200_OK)


class MenuDeleteApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgMenuDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] 删除菜单单元',
        operation_description='POST /userapi/menuDelete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="菜单ID"),
            },
        ),
        responses={
            200: KgMenuDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser']
    )
    def post(self, request):

        uid = request.data.get("id", None)
        if uid:
            try:
                Menu.objects.get(id=uid).delete()
                serializers = KgUserDetailResponseSerializer(data={"code": 200, "msg": "该菜单单元删除成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgUserDetailResponseSerializer(data={"code": 201, "msg": "不存在该菜单单元"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgMenuDetailResponseSerializer(data={"code": 202, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class MenuDetailApiView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    serializer_class = KgMenuDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /userapp/menuDetail',
        operation_summary="获取菜单详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "id",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="菜单ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: KgMenuDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200, "msg": "success"}
        mid = request.GET.get("id", None)

        if mid:
            try:
                tmpmenu = Menu.objects.get(id=mid)
                data['data'] = model_to_dict(tmpmenu)
                serializers = KgMenuDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgMenuDetailResponseSerializer(data={"code": 201, "msg": "不存在该菜单单元"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgMenuDetailResponseSerializer(data={"code": 200, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)



# Create your views here.
class CaptchaImageView(APIView):

    @swagger_auto_schema(
        operation_description='GET /userapp/captcha',
        operation_summary="获取登录验证码",
        # 接口参数 GET请求参数
        manual_parameters=[
        ],
        responses={
            200: BaseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, format=None):
        # 生成4位随机验证码  
        characters = string.ascii_uppercase + string.digits  
        captcha_text = ''.join(random.choice(characters) for i in range(4))  
        # 将验证码存储在缓存中（这里简单使用缓存，实际项目中可能需要更复杂的存储和验证逻辑）  
        cache_key = 'captcha_' + str(random.randint(1000, 9999))  
        cache_key = 'captcha_'
        cache.set(cache_key, captcha_text, timeout=300)  # 设置验证码有效期为5分钟  
        print("cache:", cache.get(cache_key))
        # 创建图片  
        width, height = 120, 40  
        image = PIL.Image.new('RGB', (width, height), (255, 255, 255))  

        # /usr/share/fonts/dejavu/DejaVuSans.ttf
        font = ImageFont.truetype(settings.TTF_PATH, 36)  # 注意：需要确保有这个字体文件，或者指定一个存在的字体路径  
        draw = ImageDraw.Draw(image)  
        
        # 绘制验证码文本  
        for i in range(4):  
            draw.text((10 + i*25, 5), captcha_text[i], font=font, fill=(0, 0, 0))  
        
        # 添加一些干扰元素（可选）  
        for _ in range(100):  
            x1 = random.randint(0, width)  
            y1 = random.randint(0, height)  
            draw.point((x1, y1), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  
        # 模糊处理（可选）  
        image = image.filter(ImageFilter.BLUR)  
        # 将图片序列化为字节流  
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')  
        byte_array.seek(0)  
        return HttpResponse(byte_array.getvalue(), content_type='image/png')



class UserApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET 用户详情',
        operation_summary="GET 标准接口",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('uid', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['appuser'])
    def get(self, request, *args, **kwargs):
        try:
            userId = request.GET.get("uid", None)
            tmpUser = User.objects.get(id=userId)
            userJson = model_to_dict(tmpUser, fields=['name', 'telephone', 'uid', 'is_superuser'])
            userJson['avatar'] = tmpUser.icon.url
            data = {"code": 200, 'success': True, 'msg': 'success', 'data': userJson}
        except:
            data = {"code": 201, 'success': False, 'msg': '用户不存在'}

        serializer = KgUserDetailResponseSerializer(data=data, many=False)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateUserApiPost(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgUserDetailResponseSerializer

    @swagger_auto_schema(
        operation_summary='POST',
        operation_description='POST 标准接口',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID"),
            },
        ),
        responses={
            200: KgUserDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['base_api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        params = request.data
        print("UpdateUserApiPost:", params)
        uid = params.get('uid', None)
        username = params.get('username', None)
        telephone = params.get('telephone', None)
        password = params.get('password', None)
        icon = params.get('avatar', None)
        
        if uid is None:
            return JsonResponse({'success': False, 'message': '无ID参数', "code": 201})
        
        tmpUser = User.objects.get(id=uid)
        if username:
            tmpUser.username = username
        
        if telephone:
            tmpUser.telephone = telephone

        if password:
            tmpUser.password = make_password(password)
        
        if icon:
            tmpUser.icon = str(icon).replace("/xapi", "").replace("media/", "")
        tmpUser.save()

        print("update:", tmpUser)
        data = {"code": 200, "data": {}, "msg": "success"}
        serializers = KgUserDetailResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class AvatarUpload(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = BaseSerializer

    @swagger_auto_schema(
        operation_summary='POST',
        operation_description='GET /userapi/uploadavatar',
        manual_parameters=[
            openapi.Parameter(
                name='files',
                in_=openapi.IN_FORM,
                description='上传的文件',
                type=openapi.TYPE_FILE
            ),
        ],
        responses={
            200: BaseSerializer(many=False),
            400: "请求失败",
        },
        tags=['base_api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        uploaded_file  = request.FILES['file']
        # 创建一个文件存储系统实例
        fs = FileSystemStorage()
        # 保存文件到MEDIA_ROOT目录，返回保存后的文件路径
        filename = fs.save("icon/" + uploaded_file.name, uploaded_file)  # 上传文件保存路径
        # 你可以通过fs.url(filename)获取文件的URL
        file_url = fs.url(filename)
        krrs = BaseSerializer(data={"code": 200, "msg": "success!", "data": file_url, "success": True}, many=False)
        krrs.is_valid()
        return Response(krrs.data, status=status.HTTP_200_OK)