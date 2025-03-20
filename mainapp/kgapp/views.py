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
from dateutil import relativedelta

from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from modelapp.models import KgModel
from yunheKGPro import CsrfExemptSessionAuthentication


# Create your views here.
class BusinessList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgBaseResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /businesslist',
            operation_summary="",
            # 接口参数 GET请求参数
            manual_parameters=[
            ],
            responses={
                200: KgBaseResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        bus_list = Business.objects.all()
        data['data'] = [model_to_dict(b) for b in bus_list]
        serializers = KgBaseResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)
    
class RecomQAList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    serializer_class = KgBaseResponseSerializer
    @swagger_auto_schema(
            operation_description='GET /recomqalist',
            operation_summary="业务问题推荐",
            # 接口参数 GET请求参数
            manual_parameters=[
                openapi.Parameter('code', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='业务编号'),
            ],
            responses={
                200: KgBaseResponseSerializer(many=False),
                400: "请求失败",
            },
            tags = ['task'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        business_code = request.GET.get("code", None)
        if business_code is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgBaseResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        try:
            tmpBusiness = Business.objects.filter(code=business_code).first()
        except:
            data = {"code": 201, "msg": "业务不存在！！！" }
            serializers = KgBaseResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        disQuestions = DisplayQuestion.objects.filter(business=tmpBusiness).all()
        result = collections.defaultdict(list)
        for disQuestion in disQuestions:
            cate = disQuestion.category.name
            result[cate].append(model_to_dict(disQuestion, exclude=['business', 'category']))
        data['data'] = result
        serializers = KgBaseResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data,  status=status.HTTP_200_OK)

class KgDataIndexApiView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = KgDataIndexResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /dataIndex',
        operation_summary="获取数据指数",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的结束时间', ),
            openapi.Parameter('size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='取值数量'),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='查询条件  0(分钟)|1(小时)|2(日级别)|3(月级别)'),
        ],
        responses={
            200: KgDataIndexResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['index'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200, "msg": "请求数据成功!"}

        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        span_type = int(request.GET.get("type", 0))
        size = request.GET.get("size", 1024)
        querySet = KgDataIndex.objects
        if span_type is not None:
            querySet = querySet.filter(span_type=span_type)
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lte="{}".format(end_time))
        querySet = querySet.all().order_by('created_at')
        dataList = collections.defaultdict(list)
        attrs = ['template_num', 'qa_num', 'rel_num', 'doc_num', 'ent_num']
        spans = []
        for e in querySet:
            for att in attrs:
                dataList[att].append(e.__getattribute__(att))
            # dataList["{}_spans".format(att)].append(e.span_value)
            spans.append(e.span_value)
        # querySet = KgDoc.objects.all()
        ## 查询条件  0(分钟)|1(小时)|2(日级别)|3(月级别)
        tmp_end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') if end_time else datetime.now()
        template_num = len(KgTemplates.objects.all())
        qa_num = len(KgQA.objects.all())
        rel_num = len(KgRelation.objects.all())
        ent_num = len(KgEntity.objects.all())
        doc_num = len(KgDoc.objects.all())
        tmpnow = datetime.now()
        print("dataList:", dataList)
        if span_type == 4:
            if tmp_end_time + relativedelta.relativedelta(years=+1) > tmpnow:
                dataList['template_num'].append(template_num)
                dataList['qa_num'].append(qa_num)
                dataList['ent_num'].append(ent_num)
                dataList['rel_num'].append(rel_num)
                dataList['doc_num'].append(doc_num)
                spans.append("{}年".format(tmpnow.year))

        if span_type == 3:
            # 2024-07-31 00:00:00
            if tmp_end_time + relativedelta.relativedelta(months=+1) > tmpnow:
                dataList['template_num'].append(template_num)
                dataList['qa_num'].append(qa_num)
                dataList['ent_num'].append(ent_num)
                dataList['rel_num'].append(rel_num)
                dataList['doc_num'].append(doc_num)
                spans.append("{}年{}月".format(tmpnow.year, tmpnow.month))

        if span_type == 2:
            # 2024-07-31 00:00:00
            if tmp_end_time + relativedelta.relativedelta(days=+1) > tmpnow:
                dataList['template_num'].append(template_num)
                dataList['qa_num'].append(qa_num)
                dataList['ent_num'].append(ent_num)
                dataList['rel_num'].append(rel_num)
                dataList['doc_num'].append(doc_num)
                spans.append("{}月{}日".format(tmpnow.month, tmpnow.day))

        if span_type == 1:
            # 2024-07-31 00:00:00
            if tmp_end_time + relativedelta.relativedelta(hours=+1) > tmpnow:
                dataList['template_num'].append(template_num)
                dataList['qa_num'].append(qa_num)
                dataList['ent_num'].append(ent_num)
                dataList['rel_num'].append(rel_num)
                dataList['doc_num'].append(doc_num)
                spans.append("{}日{}时".format(tmpnow.day, tmpnow.hour))

        modelGroup = collections.defaultdict(int)
        for km in KgModel.objects.filter(activate=1).all():
            modelGroup[km.function] = modelGroup[km.function] + 1
        dataList['modelGroup'] = modelGroup
        dataList['spans'] = spans
        data["data"] = dataList
        data['total'] = len(querySet)
        # data = {"code": 201, "msg": "请求出错误!"}

        serializers = KgDataIndexResponseSerializer(data=data)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgDocList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgdoc/',
        operation_summary="获取所有文档列表",
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
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "taglist",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="标签",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        tagstr = request.GET.get("taglist", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        if tagstr is not None:
            taglist = str(tagstr).split(",")
            querySet = []
            for tag in taglist:
                tmpTag = KgTag.objects.filter(name=tag).first()
                if tmpTag:
                    if keyword:
                        querySet.extend([doc for doc in list(tmpTag.kgdoc_set.all()) if '{}'.format(keyword) in doc.title])
                    else:
                        querySet.extend(list(tmpTag.kgdoc_set.all()))
        else:
            if keyword:
                querySet = KgDoc.objects.filter(title__contains="{}".format(keyword)).order_by('-star')
            else:
                querySet = KgDoc.objects.all().order_by('-star')

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
        if keyword:
            for o in objs:
                o.highlight_title = str(o.title).replace(f"{keyword}",
                                                         f"<span style=\"color:#F56C6C;\">{keyword}</span>")
                # o.title = str(o.title).replace(f"{keyword}", f"<span>{keyword}</span>")
        kds = KgDocSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgDocSearch(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/search',
        operation_summary="文档ES检索",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "query",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="关键词模糊搜索",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "taglist",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="标签",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc'])
    def get(self, request, *args, **kwargs):
        from elasticsearch_dsl import Q
        from elasticsearch_dsl.query import MultiMatch
        from django.core.paginator import Paginator
        from kgapp.documents import KgDocInfDocument

        query = request.GET.get("query", None)
        tagstr = request.GET.get("taglist", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        taglist = []

        if tagstr:
            taglist = str(tagstr).split(",")

        if query and taglist:
            tag_queries = [Q('term', **{'tags.name': tag_key }) for tag_key in taglist]
            tag_query = Q('bool', should=tag_queries, minimum_should_match=1)
            search_query = Q('bool', should=[
                            Q('match', title=query),
                            Q('match', desc=query)
                        ], minimum_should_match=1)
            print("tag_queries:", tag_queries)
            print("search_query:", search_query)
            main_query = Q('bool', must=[tag_query, search_query])
        elif query:
            main_query = MultiMatch(query=query, fields=['title', 'desc'])
        elif taglist:
            tag_queries = [Q('term', **{'tags.name': tag_key }) for tag_key in taglist]
            print("tag_queries:", tag_queries)
            main_query = Q('bool', should=tag_queries, minimum_should_match=1)
        else:
            main_query = Q('match_all')
        # 执行搜索
        search = KgDocInfDocument.search().query(main_query)
        print("search:", search.aggs)
        # 分页
        paginator = Paginator(range(search.count()), pageSize)  # 每页10条记录
        try:
            page_obj = paginator.page(page)
        except Exception as e:
            page_obj = paginator.page(1)
        # 计算Elasticsearch的from值
        from_value = (int(page) - 1) * paginator.per_page

        # 执行搜索时使用from和size参数
        search = search[from_value:from_value + paginator.per_page]
        response = search.execute()
        # 处理响应
        results = []
        for hit in response:
            results.append(hit.to_dict())
        
        bars = BaseApiResponseSerializer(data={
            'success': True, 
            'total': search.count(),
            'pageNum': page_obj.paginator.num_pages,
            "code": 200, 
            "msg": "success", 
            "data":results,
        }, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)



class KgDocByCttList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgdoc/listByCtt',
        operation_summary="获取目录下所有文档列表",
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
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "cid",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="目录的ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "prodflag",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="生产状态",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的结束时间', ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        cid = request.GET.get("cid", None)
        prodflag = request.GET.get("prodflag", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        querySet = KgDoc.objects
        if cid is not None and len(cid) > 0:
            querySet = querySet.filter(kg_table_content_id__id="{}".format(cid))
        if keyword is not None and len(keyword) > 0:
            querySet = querySet.filter(title__contains="{}".format(keyword))
        if prodflag:
            querySet = querySet.filter(prodflag=1)
        if start_time:
            querySet = querySet.filter(created_at__gt="{}".format(start_time))
        if end_time:
            querySet = querySet.filter(created_at__lt="{}".format(end_time))
        querySet = querySet.all().order_by('-star')
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
        kds = KgDocSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class DocAllIdListApiView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    serializer_class = KgDocIdListResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgdoc/allDocIds',
        operation_summary="获取目录下所有稳定IDs",
        # 接口参数 GET请求参数
        manual_parameters=[
        ],
        responses={
            200: KgDocIdListResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        querySet = KgDoc.objects.all()
        data['data'] = [doc.id for doc in querySet]
        serializers = KgDocIdListResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class DocDetailApiView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    serializer_class = KgDocDetailResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgdoc/detail',
        operation_summary="获取单个文档详情",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "docid",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="文档ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: KgDocDetailResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        docid = request.GET.get("docid", None)
        if docid:
            try:
                doc = KgDoc.objects.get(id=docid)
                data['data'] = model_to_dict(doc, exclude=['path', 'tags'])
                data['data']['filepath'] = doc.filepath
                data['data']['tag_list'] = doc.tag_list
                serializers = KgDocDetailResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgDocDetailResponseSerializer(data={"code": 201, "msg": "不存在该文档"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgDocDetailResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class DocAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)

    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 新增文件功能',
        operation_description='POST /kgapp/kgdoc/add',
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                description='上传的文件',
                type=openapi.TYPE_FILE
            ),
            openapi.Parameter(
                name='title',
                in_=openapi.IN_FORM,
                description='文件标题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='desc',
                in_=openapi.IN_FORM,
                description='文件标题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='dflag',
                in_=openapi.IN_FORM,
                description='同名字段处理方式 0(覆盖)|1（保留）',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='cid',
                in_=openapi.IN_FORM,
                description='所属目录ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='star',
                in_=openapi.IN_FORM,
                description='星指数',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_FORM,
                description='创建作者',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='tags',
                in_=openapi.IN_FORM,
                items=openapi.Items(openapi.TYPE_STRING),
                description='标签',
                type=openapi.TYPE_ARRAY
            ),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200}
        tmpfile = request.data.get("file", None)
        title = request.data.get("title", None)
        dflag = int(request.data.get("dflag", 0))
        desc = request.data.get("desc", None)
        star = request.data.get("star", 0)
        cid = request.data.get("cid", None)
        user_id = request.data.get("user_id", None)
        tagstr = request.data.get("tags", None)
        tags = tagstr.split(',') if tagstr else []

        if tmpfile is None or cid is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            filename = str(tmpfile)
            filetype = filename.split(".")[-1]
            new_filename = str(abs(hash(filename + str(time.time())))) + "." + filetype
            local_dir = os.path.join("media", "docs")
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
                print(f"File successfully written to {new_path}")
            except Exception as e:
                print(f"Error writing file: {e}")
                data = {"code": 201, "msg": "文件写入错误..."}
                serializers = KgDocResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            filepath = os.path.join("docs", new_filename)

            try:
                tmpuser = User.objects.get(id=user_id)
            except:
                data = {"code": 201, "msg": "用户ID不存在！！！"}
                serializers = KgDocResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            if title is None:
                title = filename

            tmpctc = KgTableContent.objects.get(id=cid)
            if dflag == 0:
                tmpdoc, _ = KgDoc.objects.get_or_create(title=title, kg_table_content_id=tmpctc)
            else:
                tmpdoc = KgDoc.objects.create(title=title, kg_table_content_id=tmpctc)

            if desc:
                tmpdoc.desc = desc
            tmpdoc.star = star
            tmpdoc.created_at = datetime.now()
            tmpdoc.updated_at = datetime.now()
            tmpdoc.path = filepath
            tmpdoc.type = filetype
            tmpdoc.size = os.stat(new_path).st_size
            tmpdoc.kg_user_id = tmpuser
            if tags:
                for t in tags:
                    tmptag, tmptagbool = KgTag.objects.get_or_create(name=t)
                    if tmptagbool:
                        tmptag.save()
                    tmpdoc.tags.add(tmptag)
            # tmpdoc.filename = filename
            tmpdoc.save()
            data = {"code": 200, "msg": "文档保存成功", "data": {"url":f"/media/docs/{new_filename}"}}
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class DocBatchAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)

    serializer_class = KgDocResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 批量新增文件功能',
        operation_description='POST /kgapp/kgdoc/batchadd',
        manual_parameters=[
            openapi.Parameter(
                name='filenum',
                in_=openapi.IN_FORM,
                description='文件数量',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='title',
                in_=openapi.IN_FORM,
                description='文件标题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='desc',
                in_=openapi.IN_FORM,
                description='文件标题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='dflag',
                in_=openapi.IN_FORM,
                description='同名字段处理方式 0(覆盖)|1（保留）',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='cid',
                in_=openapi.IN_FORM,
                description='所属目录ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='star',
                in_=openapi.IN_FORM,
                description='星指数',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_FORM,
                description='创建作者',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='tagids',
                in_=openapi.IN_FORM,
                description='标签ID',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200}
        filenum = int(request.data.get("filenum", 0))
        dflag = int(request.data.get("dflag", 0))
        desc = request.data.get("desc", None)
        star = request.data.get("star", 0)
        cid = request.data.get("cid", None)
        user_id = request.data.get("user_id", None)

        tagidstr = request.data.get('tagids', None)
        tagids = [int(i) for i in str(tagidstr).split(",")] if tagidstr is not None and len(tagidstr) > 0 else []
        print("batch add request.data", tagidstr, tagids)

        if cid is None:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            cnt = 0
            error = 0
            try:
                tmpuser = User.objects.get(id=user_id)
            except:
                data = {"code": 201, "msg": "用户ID不存在！！！"}
                serializers = KgDocResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            if tagids:
                tmptags = KgTag.objects.filter(id__in=tagids).all()
            else:
                tmptags = []
            print("tmptags", tmptags)
            tmpctc = KgTableContent.objects.get(id=cid)
            for i in range(filenum):
                tmp = request.data.get(f"file{i}", None)
                print("-->", i, tmp)
                if tmp is None:
                    continue
                print("-->", tmp)
                filename = str(tmp)
                filetype = filename.split(".")[-1]
                new_filename = str(abs(hash(filename + str(time.time())))) + "." + filetype
                local_dir = os.path.join("media", "docs")
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                    print("create", local_dir, "!!!")
                else:
                    print("subdir", local_dir, "exist!!!")
                new_path = os.path.join(local_dir, new_filename)
                try:
                    f = open(new_path, "wb+")
                    for chunk in tmp.chunks():
                        f.write(chunk)
                    f.close()
                except:
                    error += 1
                    continue
                filepath = os.path.join("docs", new_filename)
                tmpdoc = KgDoc.objects.filter(title=filename, kg_table_content_id=tmpctc).first()
                if dflag == 0 and tmpdoc is not None:
                    tmpdoc.created_at = datetime.now()
                    tmpdoc.updated_at = datetime.now()
                    tmpdoc.path = filepath
                    tmpdoc.type = filetype
                    tmpdoc.star = star
                    tmpdoc.size = os.stat(new_path).st_size
                    tmpdoc.kg_user_id = tmpuser
                    tmpdoc.desc = filename
                if tmpdoc is None:
                    tmpdoc = KgDoc.objects.create(title=filename, kg_table_content_id=tmpctc, desc=filename, path=filepath, type=filetype, star=star, size=os.stat(new_path).st_size, kg_user_id=tmpuser)   

                for t in tmptags:
                    tmpdoc.tags.add(t)
                tmpdoc.save()
                cnt += 1
            data = {"code": 200, "msg": f"{cnt}个文档保存成功"}
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class DocAddTagApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    # serializer_class = KgFileResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgFileResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 文件新增标签',
        operation_description='POST /kgapp/kgdoc/addtag',
        manual_parameters=[
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_FORM,
                description='创建作者ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='doc_id',
                in_=openapi.IN_FORM,
                description='文档ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='tagids',
                in_=openapi.IN_FORM,
                items=openapi.Items(openapi.TYPE_INTEGER),
                description='标签ID',
                type=openapi.TYPE_ARRAY
            ),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200}
        user_id = request.data.get("user_id", None)
        doc_id = request.data.get("doc_id", None)
        tagids = request.data.get("tagids[]", None)

        if doc_id is None or user_id is None:
            data = {"code": 201, "msg": "参数错误！！！"}
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 202, "msg": "用户ID不存在！！！"}
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        try:
            tmpdoc = KgDoc.objects.get(id=doc_id)
        except:
            data = {"code": 202, "msg": "文档ID不存在！！！"}
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if tagids:
            for tid in tagids:
                tmptag, tmptagbool = KgTag.objects.get(id=tid)
                if tmptagbool:
                    tmptag.save()
                tmpdoc.tags.add(tmptag)
            tmpdoc.save()
            data = {"code": 200, "msg": "标签添加成功！！！"}
        else:
            data = {"code": 201, "msg": "标签传递为空"}
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class DocUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)

    # serializer_class = KgDocResponseSerializer
    # def get_serializer_class(self):
    #     if self.action == 'post':
    #         return KgDocResponseSerializer
    #     return self.serializer_class
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 更新文件功能',
        operation_description='[可用] 更新文件功能',
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                description='上传的文件',
                type=openapi.TYPE_FILE
            ),
            openapi.Parameter(
                name='title',
                in_=openapi.IN_FORM,
                description='文件标题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='desc',
                in_=openapi.IN_FORM,
                description='文档摘要',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='star',
                in_=openapi.IN_FORM,
                description='星指数',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='prodflag',
                in_=openapi.IN_FORM,
                description='取消生产标识',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='ctt_id',
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
            openapi.Parameter(
                name='doc_id',
                in_=openapi.IN_FORM,
                description='文档',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='tagids',
                in_=openapi.IN_FORM,
                description='标签ids',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    def post(self, request):
        data = {"code": 200}
        tmpfile = request.data.get("file", None)
        title = request.data.get("title", None)
        desc = request.data.get("desc", None)
        star = request.data.get("star", None)
        prodflag = request.data.get("prodflag", None)
        ctt_id = request.data.get("ctt_id", None)
        user_id = request.data.get("user_id", None)
        doc_id = request.data.get("doc_id", None)
        tagidstr = request.data.get('tagids', None)
        tagids = [int(i) for i in str(tagidstr).split(",")] if tagidstr is not None and len(tagidstr) > 0 else []
        print("update request.data", tagidstr, tagids)
        if tagids:
            tmptags = KgTag.objects.filter(id__in=tagids).all()
        else:
            tmptags = []
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 201, "msg": "用户ID不存在！！！"}
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if doc_id is None:
            data['code'] = 201
            data['msg'] = '文档ID参数不能为空！！！'
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        tmpdoc = KgDoc.objects.get(id=doc_id)
        if tmpfile:
            filename = str(tmpfile)
            filetype = filename.split(".")[-1]
            # new_filename = str(abs(hash(filename + str(time.time())))) + "." + filetype
            local_dir = os.path.join("media", "docs")
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
                data = {"code": 201, "msg": "文件写入错误..."}
                serializers = KgDocResponseSerializer(data=data, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            filepath = os.path.join("docs", filename)
            tmpdoc.path = filepath
            # tmpdoc.filename = filename
        if desc:
            tmpdoc.desc = desc

        if title:
            tmpdoc.title = title

        if prodflag is not None:
            tmpdoc.prodflag = prodflag

        if star is not None:
            tmpdoc.star = star

        if tmptags:
            tmpdoc.tags.clear()
            for t in tmptags:
                tmpdoc.tags.add(t)
        if ctt_id:
            try:
                tmpctc = KgTableContent.objects.get(id=ctt_id)
                if tmpctc:
                    tmpctc_size = len(KgTableContent.objects.all())
                    tmpctc.order_no = tmpctc_size
                    tmpctc.kg_user_id = tmpuser
                    tmpctc.save()
                tmpdoc.kg_table_content_id = tmpctc
            except:
                pass
        tmpdoc.updated_at = datetime.now()
        tmpdoc.save()
        data = {"code": 200, "msg": "文档更新成功"}
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class DocBatchUpdateApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_summary='[可用] 批量更新文件生产状态',
        operation_description='[可用] 批量更新文件生产状态',
        manual_parameters=[
            openapi.Parameter(
                name='docidstr',
                in_=openapi.IN_FORM,
                description='文档IDS',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    def post(self, request):
        data = {"code": 200}
        docidstr = request.data.get("docidstr", None)
        if docidstr is None:
            data['code'] = 201
            data['msg'] = '文档ID参数不能为空！！！'
            serializers = KgDocResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        doc_ids = str(docidstr).split(",")
        tmpdocs = KgDoc.objects.filter(id__in=doc_ids).all()
        if tmpdocs:
            for td in tmpdocs:
                td.prodflag = 0
                td.desc = ""
                td.updated_at = datetime.now()
                td.save()
            data = {"code": 200, "msg": "文档删除成功"}
        else:
            data = {"code": 200, "msg": "暂无发现文档"}
        serializers = KgDocResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class DocDelApiView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = KgDocResponseSerializer

    @swagger_auto_schema(
        operation_description="文档删除",
        operation_summary="[可用] 文档删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="文件ID"),
            },
        ),
        responses={
            200: KgDocResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['doc']
    )
    @csrf_exempt
    def post(self, request):
        import platform
        data = {"code": 200}

        docid = None
        if request.POST:
            docid = request.POST["id"]
        if docid is None:
            docid = request.data["id"]
        if docid is None:
            serializers = KgDocResponseSerializer(data={"code": 201, "msg": "请求参数错误...."}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgDoc.objects.get(id=docid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgDocResponseSerializer(data={"code": 200, "msg": "文档删除成功"}, many=False)
            else:
                serializers = KgDocResponseSerializer(data={"code": 201, "msg": "文档不存在"}, many=False)
        except:
            serializers = KgDocResponseSerializer(data={"code": 202, "msg": "系统错误"}, many=False)

        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgQAList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = KgDoc.objects.all()
    serializer_class = KgDocSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgqa/',
        operation_summary="获取所有问题列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                # 参数描述
                description="问题模糊搜索",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        tags=['kg'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description='GET /kgapp/kgqa/', operation_summary="新建问题", tags=['kg'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# class KgHotSearchList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):

#     serializer_class = KgHotSearchResponseSerializer
#     @swagger_auto_schema(
#             operation_description='GET /kgapp/kghotqa/',
#             operation_summary="获取所有Hot问题列表",
#             # 接口参数 GET请求参数
#             manual_parameters=[
#                 # 声明参数
#                 openapi.Parameter(
#                     "keyword", 
#                     openapi.IN_QUERY, 
#                     # 参数描述
#                     description="问题模糊搜索", 
#                     # 参数字符类型
#                     type=openapi.TYPE_STRING
#                 ),
#                 openapi.Parameter(
#                     "top", 
#                     openapi.IN_QUERY, 
#                     # 参数描述
#                     description="获取前TOP热搜", 
#                     # 参数字符类型
#                     type=openapi.TYPE_STRING
#                 ),
#                 openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
#                 openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
#             ],
#             tags = ['kg'])
#     def get(self, request, *args, **kwargs):
#         data = {"code": 200 }
#         keyword = request.GET.get('keyword', None)
#         top = int(request.GET.get('top', 10))
#         if keyword:
#             values = KgHotSearch.objects.filter(content__contain=keyword).order_by("-cnt")
#         else:
#             values = KgHotSearch.objects.order_by("-cnt").all()
#         data['data'] = [model_to_dict(e) for e in values[:top]]
#         serializers = KgHotSearchResponseSerializer(data=data, many=False)
#         serializers.is_valid()
#         return Response(serializers.data,  status=status.HTTP_200_OK)

#     @swagger_auto_schema(operation_description='GET /kgapp/kghotqa/',operation_summary="新建hot问题", tags = ['kg'])
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class KgTabTagList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    serializer_class = KgTagResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtabtag/',
        operation_summary="获取所有标签目录列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                # 参数描述
                description="标签模糊搜索",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        tags=['tag'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        keyword = request.GET.get('keyword', None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        if keyword:
            values = KgTabTag.objects.filter(name__icontains=keyword).all().order_by('-updated_at')
        else:
            values = KgTabTag.objects.all()

        data['total'] = len(values)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(values, pageSize)
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)

        data['data'] = [e.toJson() for e in objs]
        serializers = KgTagResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTagByTabList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = KgTagResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgdoc/listByTab',
        operation_summary="获取目录下所有标签列表",
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
            # 声明参数
            openapi.Parameter(
                # 参数名称
                "tabtag_id",
                # 参数类型为query
                openapi.IN_QUERY,
                # 参数描述
                description="目录的ID",
                # 参数字符类型
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter('start_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的开始时间', ),
            openapi.Parameter('end_time', openapi.IN_QUERY, type=openapi.FORMAT_DATE, description='文本的结束时间', ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgTagResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['tag'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        tabtag_id = request.GET.get("tabtag_id", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)

        if tabtag_id:
            try:
                tabtag = KgTabTag.objects.get(id=tabtag_id)
            except:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "当前标签目录ID不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            querySet = []
            for t in tabtag.tags.all():
                if keyword:
                    if keyword not in t.name:
                        continue
                if start_time and end_time:
                    if start_time < t.created_at < end_time:
                        querySet.append(t)
                elif start_time:
                    if start_time < t.created_at:
                        querySet.append(t)
                elif end_time:
                    if t.created_at < end_time:
                        querySet.append(t)
                else:
                    querySet.append(t)
        else:
            querySet = KgTag.objects
            if keyword is not None and len(keyword) > 0:
                querySet = querySet.filter(name__contains="{}".format(keyword))
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
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:
            objs = paginator.page(paginator.num_pages)
        kds = KgTagSerializer(data=objs, many=True)
        kds.is_valid()
        data['data'] = kds.data
        serializers = KgTagResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TabTagAddApiView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtabtag/add',
        operation_summary="新增一级目录标签",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签目录名称"),
            },
        ),
        tags=['tag'])
    def post(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        print(request.data)
        if name:
            try:
                tmptag, tmpbool = KgTabTag.objects.get_or_create(name=name)
                if tmpbool:
                    tmptag.created_at = datetime.now()
                    tmptag.updated_at = datetime.now()
                    tmptag.save()
                    serializers = KgTagResponseSerializer(data={"code": 200, "msg": "新建标签成功", "data": tmptag.toJson()},
                                                          many=False)
                else:
                    serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签已存在", "data": tmptag.toJson()},
                                                          many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "系统错误"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgTagResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TabTagUpdateApiView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    serializer_class = KgTagResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtabtag/update',
        operation_summary="更新标签目录名称",
        # 接口参数 GET请求参数

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['tag_id'],
            properties={
                'tabtag_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="标签ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签"),
            },
        ),
        tags=['tag'])
    def post(self, request, *args, **kwargs):
        tag_id = request.data.get('tabtag_id', None)
        name = request.data.get('name', None)
        if tag_id is None:
            serializers = KgTagResponseSerializer(data={"code": 201, "msg": "标签目录ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if name:
            try:
                tmptag = KgTabTag.objects.get(id=tag_id)
                tmptag.name = name
                tmptag.save()
                serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签目录更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "用户不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
        serializers = KgTagResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TabTagAddTagApiView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtabtag/batchaddtags',
        operation_summary="目录下新增标签",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="标签目录名称"),
                'tags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_STRING),
                                       description="子标签"),
                'descs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_STRING),
                                        description="描述"),
            },
        ),
        tags=['tag'])
    def post(self, request, *args, **kwargs):
        tabtagid = request.data.get('id', None)
        tags = request.data.get('tags', [])
        descs = request.data.get('descs', [])
        if tags and descs:
            try:
                tmptabtag = KgTabTag.objects.get(id=tabtagid)
                for tmpstr, desc in zip(tags, descs):
                    tt, tb = KgTag.objects.get_or_create(name=tmpstr)
                    if tb:
                        tt.desc = desc
                        tt.created_at = datetime.now()
                        tt.updated_at = datetime.now()
                        tt.save()
                    tmptabtag.tags.add(tt)
                tmptabtag.save()
                serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签添加成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "标签目录ID不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgTagResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TabTagDelApiView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgTagResponseSerializer

    @swagger_auto_schema(
        operation_description="标签目录删除",
        operation_summary="[可用] 标签目录删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="目录ID"),
            },
        ),
        responses={
            200: KgTagResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['tag']
    )
    @csrf_exempt
    def post(self, request):
        data = {"code": 200}
        tagid = request.data["id"]
        if tagid is None:
            serializers = KgTagResponseSerializer(data={"code": 201, "msg": "请求参数错误...."}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgTabTag.objects.get(id=tagid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签目录删除成功"}, many=False)
            else:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "标签目录不存在"}, many=False)
        except:
            serializers = KgTagResponseSerializer(data={"code": 202, "msg": "系统错误"}, many=False)

        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTagList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtag/',
        operation_summary="获取所有标签列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                # 参数描述
                description="标签模糊搜索",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        tags=['tag'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        keyword = request.GET.get('keyword', None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10)
        if keyword:
            values = KgTag.objects.filter(name__icontains=keyword).all().order_by('-updated_at')
        else:
            values = KgTag.objects.all()

        data['total'] = len(values)
        data['page'] = page
        data['pageSize'] = pageSize
        paginator = Paginator(values, pageSize)
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except:

            objs = paginator.page(paginator.num_pages)

        data['data'] = [e.toJson() for e in objs]
        serializers = KgTagResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TagAddApiView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtag/add',
        operation_summary="新增标签",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="描述"),
            },
        ),
        tags=['tag'])
    def post(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        desc = request.data.get('desc', '')
        print(request.data)
        if name:
            try:
                tmptag, tmpbool = KgTag.objects.get_or_create(name=name)
                if tmpbool:
                    tmptag.desc = desc
                    tmptag.created_at = datetime.now()
                    tmptag.updated_at = datetime.now()
                    tmptag.save()
                    serializers = KgTagResponseSerializer(data={"code": 200, "msg": "新建标签成功", "data": tmptag.toJson()},
                                                          many=False)
                else:
                    serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签已存在", "data": tmptag.toJson()},
                                                          many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

        serializers = KgTagResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TagUpdateApiView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    serializer_class = KgTagResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtag/update',
        operation_summary="获取所有标签列表",
        # 接口参数 GET请求参数

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['tag_id'],
            properties={
                'tag_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="标签ID"),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="标签"),
                'desc': openapi.Schema(type=openapi.TYPE_STRING, description="描述"),
            },
        ),
        tags=['tag'])
    def post(self, request, *args, **kwargs):
        tag_id = request.data.get('tag_id', None)
        name = request.data.get('name', None)
        desc = request.data.get('desc', None)
        if tag_id is None:
            serializers = KgTagResponseSerializer(data={"code": 201, "msg": "标签ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if name:
            try:
                tmptag = KgTag.objects.get(id=tag_id)
                tmptag.name = name
                if desc is not None:
                    tmptag.desc = desc
                tmptag.save()
                serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "用户不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
        serializers = KgTagResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TagDelApiView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    serializer_class = KgTagResponseSerializer

    @swagger_auto_schema(
        operation_description="标签删除",
        operation_summary="[可用] 标签删除",
        # request_body is used to specify parameters
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description="标签ID"),
            },
        ),
        responses={
            200: KgTagResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['tag']
    )
    @csrf_exempt
    def post(self, request):
        import platform
        tagid = request.data["id"]
        if tagid is None:
            serializers = KgTagResponseSerializer(data={"code": 201, "msg": "请求参数错误...."}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            tmpkg = KgTag.objects.get(id=tagid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgTagResponseSerializer(data={"code": 200, "msg": "标签删除成功"}, many=False)
            else:
                serializers = KgTagResponseSerializer(data={"code": 201, "msg": "标签不存在"}, many=False)
        except:
            serializers = KgTagResponseSerializer(data={"code": 202, "msg": "系统错误"}, many=False)

        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TagDetailApiView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgtag/detail',
        operation_summary="获取所有标签列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                # 参数描述
                description="标签模糊搜索",
                # 参数字符类型
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        tags=['tag'])
    def get(self, request, *args, **kwargs):
        data = {"code": 200}
        keyword = request.GET.get('keyword', None)
        if keyword:
            values = KgTag.objects.filter(content__contain=keyword).all()
        else:
            values = KgTag.objects.all()
        data['data'] = [model_to_dict(e) for e in values]
        serializers = KgTagResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTabCTTList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    serializer_class = KgTabCTTResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgctt/',
        operation_summary="获取目录列表",
        # 接口参数 GET请求参数
        manual_parameters=[
        ],
        tags=['ctt'])
    def get(self, request, *args, **kwargs):

        def arr2tree(source, parent):
            tree = []
            for item in source:
                if item['parent_id'] == parent:
                    item['children'] = arr2tree(source, item['id'])
                    tree.append(item)
            return tree

        data = {"code": 200}
        ctts = KgTableContent.objects.all().order_by('-updated_at')

        tmpctts = [model_to_dict(ctt) for ctt in ctts]
        data['tabctt'] = arr2tree(tmpctts, 0)
        serializers = KgTabCTTResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTabCTTAddAPIList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = KgTabCTTResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgctt/add',
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
        tags=['ctt'])
    def post(self, request, *args, **kwargs):
        data = {"code": 200, "msg": "目录创建成功"}
        parent_id = int(request.data.get('parent_id', 0))
        user_id = request.data.get('user_id', None)
        name = request.data.get('name', None)
        if name is None or len(name) == 0:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        if user_id:
            tmpUser = User.objects.get(id=user_id)
        else:
            tmpUser = None
        tmpctt, tmpbool = KgTableContent.objects.get_or_create(parent_id=parent_id, name=name)
        if tmpbool:
            if tmpUser:
                tmpctt.kg_user_id = tmpUser
                tmpctt.save()
            data['msg'] = "创建成功"
        else:
            data = {"code": 202, "msg": "已经存在该目录"}

        data['data'] = model_to_dict(tmpctt, exclude=[''])
        serializers = KgTabCTTResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


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
        tags=['ctt']
    )
    @csrf_exempt
    def post(self, request):
        cctid = None
        if request.POST:
            cctid = request.POST["id"]
        if cctid is None:
            cctid = request.data["id"]
        if cctid is None:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "请求参数错误...."}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        try:
            querySet = KgDoc.objects.filter(kg_table_content_id__id="{}".format(cctid))
            if len(querySet) > 0:
                serializers = KgTabCTTResponseSerializer(data={"code": 202, "msg": "该文件夹下存在文件，不能直接删除"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)

            tmpkg = KgTableContent.objects.get(id=cctid)
            if tmpkg:
                tmpkg.delete()
                serializers = KgTabCTTResponseSerializer(data={"code": 200, "msg": "当前目录删除成功"}, many=False)
            else:
                serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "目录不存在"}, many=False)
        except:
            serializers = KgTabCTTResponseSerializer(data={"code": 202, "msg": "系统错误"}, many=False)

        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KgTabCTTUpdateAPIList(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = KgTag.objects.all()
    serializer_class = KgTagResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @swagger_auto_schema(
        operation_description='GET /kgapp/kgctt/update',
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
        tags=['ctt'])
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)
        ctt_id = request.data.get('id', None)
        name = request.data.get('name', None)
        if ctt_id is None:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "文档ID错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        if user_id:
            tmpuser = User.objects.get(id=user_id)
        else:
            tmpuser = None

        if ctt_id and name:
            try:
                tmpcct = KgTableContent.objects.get(id=ctt_id)
                if tmpuser:
                    tmpcct.kg_user_id = tmpuser
                tmpcct.name = name
                tmpcct.save()
                serializers = KgTabCTTResponseSerializer(data={"code": 200, "msg": "目录更新成功"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
            except:
                serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "目录ID不存在"}, many=False)
                serializers.is_valid()
                return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            serializers = KgTabCTTResponseSerializer(data={"code": 201, "msg": "参数错误"}, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)


class KgText2SqlList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = KgDocResponseSerializer

    @swagger_auto_schema(
        operation_description='GET /kgapp/t2slist/',
        operation_summary="获取所有text2sql数据",
        # 接口参数 GET请求参数
        manual_parameters=[
            # 声明参数
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                description="关键词模糊搜索",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: KgText2SQLResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api'])
    def get(self, request, *args, **kwargs):

        data = {"code": 200}
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 10000)

        if keyword:
            querySet = KgText2SQL.objects.filter(query__contains="{}".format(keyword)).order_by('-updated_at')
        else:
            querySet = KgText2SQL.objects.all().order_by('-updated_at')
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
        data['data'] = [model_to_dict(obj) for obj in objs]
        ser = KgText2SQLResponseSerializer(data=data, many=False)
        ser.is_valid()
        return Response(ser.data, status=status.HTTP_200_OK)
