import hashlib
import time
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
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
from langchain.vectorstores import FAISS
import os
import collections

from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)
from apiapp.serializers import ApiAppResponseSerializer
from yunheKGPro import CsrfExemptSessionAuthentication
from yunheKGPro.settings import embedding

# Create your views here.

class KnowledgeAddApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 增加知识库',
        operation_description='POST /knowledge/add',
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_FORM,
                description='知识库名称',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='desc',
                in_=openapi.IN_FORM,
                description='知识库描述',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200}
        kgname = request.data.get("name", None)
        kgdesc = request.data.get("desc", None)

        if not kgname:
            data = {"code": 201, "msg": "参数错误！"}
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        

        hashid = str(hashlib.md5(kgname.encode('utf-8')).hexdigest())

        if Knowledge.objects.filter(hashid=hashid).exists():
            data = {"code": 202, "msg": "知识库已经存在"}
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)

        try:
            hashid = str(hashlib.md5(kgname.encode('utf-8')).hexdigest())
            kg = Knowledge.objects.create(name=kgname, desc=kgdesc, hashid=hashid)
            data = {"code": 200, "msg": "success", "data": model_to_dict(kg)}
        except Exception as e:
            data = {"code": 203, "msg": "知识库创建失败"}
            
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KnowledgeListApiView(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_description='GET /knowledge/list',
        operation_summary="[可用] 获取知识库列表",
        # 接口参数 GET请求参数
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('pageSize', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api'])
    def get(self, request, *args, **kwargs):
        
        keyword = request.GET.get("keyword", None)
        page = request.GET.get("page", 1)
        pageSize = request.GET.get("pageSize", 5)
        KnowledgeListApiView.queryset = Knowledge.objects

        if keyword:
            KnowledgeListApiView.queryset = KnowledgeListApiView.queryset.filter(name__icontains=keyword).order_by('-created_at').all()
        else:
            KnowledgeListApiView.queryset = KnowledgeListApiView.queryset.order_by('-created_at').all()

        paginator = Paginator(KnowledgeListApiView.queryset, pageSize)
        try:
            ptList = paginator.page(page)
        except PageNotAnInteger:
            ptList = paginator.page(1)
        except EmptyPage:
            ptList = paginator.page(paginator.num_pages)

        results = []
        for tmp in ptList:
            tmpdict = model_to_dict(tmp)
            tmpdict['created_at'] = tmp.created_at.strftime("%Y-%m-%d %H:%M:%S")
            results.append(tmpdict)

        data = {"code": 200, "msg": "success", "data": results, "success": True, "total": paginator.count, "page": paginator.num_pages, "pageSize": paginator.per_page}
        bars = ApiAppResponseSerializer(data=data, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)


class KnowledgeDeleteApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 删除知识库操作',
        operation_description='POST /knowledge/del',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID"),
            },
        ),
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        kgId = request.data.get("id", None)
        try:
            kg = Knowledge.objects.get(id=kgId)
            kg.delete()
            data = {"code": 200, "data": {}, "msg": "删除成功！", "success": True}
        except:
            data = {"code": 202, "data": {}, "msg": "系统不存在该数据", "success": False}

        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class KnowledgeRetrieval(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer

    @swagger_auto_schema(
        operation_summary='[可用] Defy知识库节点挂接',
        operation_description='POST /knowledge/retrieval',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'knowledge_id': openapi.Schema(type=openapi.TYPE_STRING, description="知识库ID"),
                'query': openapi.Schema(type=openapi.TYPE_STRING, description="查询问题"),
                'retrieval_setting': openapi.Schema(type=openapi.TYPE_OBJECT, description="检索条件"),
            },
        ),
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        print("TemplateAddOrUpdateNode:", request.data)
        kgHashId = request.data.get("knowledge_id", None)
        query = request.data.get("query", None)
        retrieval_setting = request.data.get("retrieval_setting", {})
        top_k = retrieval_setting.get("top_k", 10)
        score_threshold = retrieval_setting.get("score_threshold", 0.3)

        
        kgdir = f"data/knowledges/{kgHashId}"
        if not os.path.exists(kgdir):
            os.makedirs(kgdir)
        index_path = os.path.join(kgdir, "faiss.index")

        if not os.path.exists(index_path):
            print("❌ 不存在向量库，开始创建向量库...")
            data = {"code": 201, "records": [], "msg": "未找到任何对应的知识片段"}
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        print("✅ 加载 embedding 模型")
        db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        print("✅ 已加载现有向量库")
        # 1. 向量检索
        fragpacks = db.similarity_search_with_score(query, top_k)
        print("✅ 向量检索完成")
        # 2. 从向量库中获取对应的知识片段
        print("🔄 从向量库中获取对应的知识片段...")
        if not fragpacks:
            print("❌ 未找到任何对应的知识片段")
            data = {"code": 202, "records": [], "msg": "参数错误"}
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        print("✅ 已获取知识片段")
        # 3. 获取知识片段对应的知识
        records = []
        for frag, score in fragpacks:
            # print("🔄 从向量库中获取对应的知识片段...", frag, score)
            if score < score_threshold:
                continue
            ctt = frag.page_content
            fragid = frag.metadata['id']
            docid = frag.metadata['docid']
            try:
                tmpdoc = KgDoc.objects.get(id=docid)
                tmpfrag = KgDocFragmentation.objects.get(id=fragid)
                tmpfrag.recall_cnt += 1
                tmpfrag.save()
                records.append({"title": tmpdoc.title, 
                                "content": ctt, 
                                "score": score, 
                                "metadata":{
                                    'path': tmpdoc.filepath,
                                    'description': tmpdoc.desc,
                                }
                            })
            except Exception as e:
                print("❌ 未找到对应的知识片段", e)
        
        print("✅ 已获取知识片段对应的知识")
        data = {"code": 200, "msg": "success", "records": records}
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KnowledgeUploadApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = ApiAppResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
        operation_summary='[可用] 新增知识库文档上传功能',
        operation_description='POST /knowledge/upload',
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                description='上传的文件',
                type=openapi.TYPE_FILE
            ),
            openapi.Parameter(
                name='knowledge_id',
                in_=openapi.IN_FORM,
                description='知识库ID',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        data = {"code": 200}
        tmpfile = request.data.get("file", None)
        knowledge_id = request.data.get("knowledge_id", None)
        tagstr = request.data.get("tags", None)
        tags = tagstr.split(',') if tagstr else []

        if tmpfile is None or knowledge_id is None: 
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        filename = str(tmpfile)
        filetype = filename.split(".")[-1]
        new_filename = str(abs(hash(filename + str(time.time())))) + "." + filetype
        local_dir = os.path.join("media", "knowledges", knowledge_id)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            print("create", local_dir, "!!!")
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
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        filepath = os.path.join("knowledges", knowledge_id, new_filename)
        tmpctt, _ = KgTableContent.objects.get_or_create(parent_id=0, name="RAG知识库")
        tmpKg = Knowledge.objects.filter(hashid=knowledge_id).first()
        target_ctt, _ = KgTableContent.objects.get_or_create(parent_id=tmpctt.id, name=tmpKg.name)

        print("target_ctt:", target_ctt, "target_ctt.id:", target_ctt.id, "tmpKg:", tmpKg, "title:", filename)
        tmpdoc = KgDoc.objects.create(title=filename, kg_table_content_id=target_ctt, kg_knowledge_id=tmpKg)
        tmpdoc.star = 0
        tmpdoc.path = filepath
        tmpdoc.type = filetype
        tmpdoc.size = os.stat(new_path).st_size
        if tags:
            for t in tags:
                tmptag, tmptagbool = KgTag.objects.get_or_create(name=t)
                if tmptagbool:
                    tmptag.save()
                tmpdoc.tags.add(tmptag)
        # tmpdoc.filename = filename
        tmpdoc.save()
        data = {"code": 200, "msg": "文档保存成功"}
        data['data'] = model_to_dict(tmpdoc, exclude=['path', 'tags'])
        data['data']['filepath'] = tmpdoc.filepath
        data['data']['tag_list'] = tmpdoc.tag_list
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)
    

class KnowledgeTrainTaskApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 知识库训练Faiss',
        operation_description='POST /knowledge/train',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                'knowledge_id': openapi.Schema(type=openapi.TYPE_STRING, description="知识库ID"),
                'taskType': openapi.Schema(type=openapi.TYPE_INTEGER, description="生产类型 0(知识导入)|1(自动生成)|2(全文生产)|3(图谱导入)|4(图谱自动生产)|5(预案生成)|6(文档解析)|7(训练Faiss)"),
            },
        ),
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        user_id = request.data.get("user_id", 1)
        knowledge_id = request.data.get("knowledge_id", None)
        taskType = int(request.data.get("taskType", 7))
        if not knowledge_id:
            data['code'] = 201
            data['msg'] = '请求知识库参数错误, 缺少参数！！！'
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 202, "msg": "用户ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
            
        try:
            tmpKg = Knowledge.objects.filter(hashid=knowledge_id).first()
        except:
            data = {"code": 203, "msg": "知识库ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        
        kgname = tmpKg.name if tmpKg.name else '默认知识库训练Faiss任务'
        tmptask = KgProductTask()
        tmptask.name = kgname
        tmpdesc = kgname + "- 训练任务"
        tmptask.desc = tmpdesc
        tmptask.task_type = taskType
        tmptask.kg_user_id = tmpuser
        tmptask.task_status = 0  #### 0 未执行,  1 任务开启, 执行数据装载, 2 数据装载完成, 3 比对任务开启, 4 比对任务完成, 5 最终任务完成, -1 任务失败
        tmptask.save()

        from yunheKGPro.celery import knowledgeTrainFaissTask
        param_dict = model_to_dict(tmptask, exclude=['kg_doc_ids'])
        param_dict['task_id'] = tmptask.id
        param_dict['knowledge_id'] = knowledge_id

        result = knowledgeTrainFaissTask.delay(param_dict)
        # 记录 celery id 入库 
        subtask, tmpbool = KgTask.objects.get_or_create(kg_prod_task_id=tmptask, task_step=1, celery_id=result.id)
        if tmpbool:
            print("知识库训练Faiss任务创建成功...", subtask)
        data = {"code": 200, "msg": "知识库训练Faiss新建成功", "success": True, "data": model_to_dict(subtask)}
        data['data'] = model_to_dict(subtask)
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KnowledgeDocParseTaskApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 知识库文档解析操作',
        operation_description='POST /knowledge/parse',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID"),
                'knowledge_id': openapi.Schema(type=openapi.TYPE_STRING, description="知识库ID"),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                'taskType': openapi.Schema(type=openapi.TYPE_INTEGER, description="生产类型 0(知识导入)|1(自动生成)|2(全文生产)|3(图谱导入)|4(图谱自动生产)|5(预案生成)|6(文档解析)"),
            
            },
        ),
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        kgdocid = request.data.get("id", None)
        user_id = request.data.get("user_id", 1)
        knowledge_id = request.data.get("knowledge_id", None)
        taskType = int(request.data.get("taskType", 6))
        if kgdocid is None or not knowledge_id:
            data['code'] = 201
            data['msg'] = '请求参数错误, 缺少参数！！！'
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data,  status=status.HTTP_200_OK)
        
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 202, "msg": "用户ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
            
        try:
            tmpKg = Knowledge.objects.filter(hashid=knowledge_id).first()
        except:
            data = {"code": 203, "msg": "知识库ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        try:
            tmpDoc = KgDoc.objects.get(id=kgdocid)
        except:
            data = {"code": 204, "msg": "文档ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        kgname = tmpKg.name if tmpKg.name else '默认文档解析任务'
        tmptask = KgProductTask()
        tmptask.name = kgname
        tmpdesc = kgname + "-" + tmpDoc.title + "-" + "文档解析任务"
        tmptask.desc = tmpdesc
        tmptask.task_type = taskType
        tmptask.kg_user_id = tmpuser
        tmptask.task_status = 0  #### 0 未执行,  1 任务开启, 执行数据装载, 2 数据装载完成, 3 比对任务开启, 4 比对任务完成, 5 最终任务完成, -1 任务失败
        tmptask.save()

        from yunheKGPro.celery import knowledgeParseTask
        param_dict = model_to_dict(tmptask, exclude=['kg_doc_ids'])
        param_dict['task_id'] = tmptask.id
        param_dict['kg_doc_ids'] = [kgdocid]
        param_dict['knowledge_id'] = knowledge_id

        result = knowledgeParseTask.delay(param_dict)
        # 记录 celery id 入库 
        subtask, tmpbool = KgTask.objects.get_or_create(kg_prod_task_id=tmptask, task_step=1, celery_id=result.id)
        if tmpbool:
            print("ProductTask 任务创建成功...", subtask)
        data = {"code": 200, "msg": "预案生产任务新建成功", "success": True, "data": model_to_dict(subtask)}
        data['data'] = model_to_dict(subtask)
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class KnowledgeDocBatchParseTaskApiView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 知识库批量文档解析操作',
        operation_description='POST /knowledge/batchparse',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['knowledge_id'],
            properties={
                'knowledge_id': openapi.Schema(type=openapi.TYPE_STRING, description="知识库ID"),
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="创建作者ID"),
                'taskType': openapi.Schema(type=openapi.TYPE_INTEGER, description="生产类型 0(知识导入)|1(自动生成)|2(全文生产)|3(图谱导入)|4(图谱自动生产)|5(预案生成)|6(文档解析)"),
            },
        ),
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api']
    )
    @csrf_exempt
    def post(self, request, *args, **krgs):
        user_id = request.data.get("user_id", 1)
        knowledge_id = request.data.get("knowledge_id", None)
        taskType = int(request.data.get("taskType", 6))
        try:
            tmpuser = User.objects.get(id=user_id)
        except:
            data = {"code": 202, "msg": "用户ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
            
        try:
            tmpKg = Knowledge.objects.filter(hashid=knowledge_id).first()
        except:
            data = {"code": 203, "msg": "知识库ID不存在！！！" }
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        kgname = tmpKg.name if tmpKg.name else '默认文档解析任务'
        tmptask = KgProductTask()
        tmptask.name = kgname
        tmpdesc = kgname + "-" + "批量文档解析任务"
        tmptask.desc = tmpdesc
        tmptask.task_type = taskType
        tmptask.kg_user_id = tmpuser
        tmptask.task_status = 0  #### 0 未执行,  1 任务开启, 执行数据装载, 2 数据装载完成, 3 比对任务开启, 4 比对任务完成, 5 最终任务完成, -1 任务失败
        tmptask.save()

        from yunheKGPro.celery import knowledgeParseTask
        param_dict = model_to_dict(tmptask, exclude=['kg_doc_ids'])
        param_dict['task_id'] = tmptask.id
        param_dict['knowledge_id'] = knowledge_id

        result = knowledgeParseTask.delay(param_dict)
        # 记录 celery id 入库 
        subtask, tmpbool = KgTask.objects.get_or_create(kg_prod_task_id=tmptask, task_step=1, celery_id=result.id)
        if tmpbool:
            print("ProductTask 任务创建成功...", subtask)
        data = {"code": 200, "msg": "预案生产任务新建成功", "success": True, "data": model_to_dict(subtask)}
        data['data'] = model_to_dict(subtask)
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)