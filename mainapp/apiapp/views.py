import codecs
import json
import logging
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
from apiapp import prod_outline, prod_qa, prod_abstract, prod_extend, prod_text2sql
from kgapp.models import KgText2SQL
from yaapp import getYuAnParamPath
from yaapp.plan import PlanFactory
from yaapp.models import PlanByUser
from userapp.models import User
from yunheKGPro import settings
from apiapp.serializers import *
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
logger = logging.getLogger('kgproj')

from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from apiapp.serializers import ApiAppResponseSerializer
from yunheKGPro import CsrfExemptSessionAuthentication

class YLHYuAnApiGet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    
    serializer_class = ApiAppResponseSerializer

    @swagger_auto_schema(
        operation_description='GET ///',
        operation_summary="[获取最新预案]  获取用户最近编辑的",
        # 接口参数 GET请求参数
        manual_parameters=[
        ],
        responses={
            200: ApiAppResponseSerializer(many=False),
            400: "请求失败",
        },
        tags=['api'])
    def get(self, request, *args, **kwargs):
        # 获取最近的ylh的调度方案单
        uid = request.GET.get("uid", None)
        try:
            tmpUser = User.objects.get(id=uid)
        except:
            tmpUser = None
        if tmpUser is None:
            YLHYuAnApiGet.queryset = PlanByUser.objects.filter(ctype=4)
        else:
            YLHYuAnApiGet.queryset = PlanByUser.objects.filter(user=tmpUser, ctype=4)
        userYuAnPlan = YLHYuAnApiGet.queryset.order_by('-created_at').first()
        if userYuAnPlan is None:
            data = {"code": 202, "data": {}, "msg": "系统不存在该数据", "success": False}
            bars = ApiAppResponseSerializer(data=data, many=False)
            bars.is_valid()
            return Response(bars.data, status=status.HTTP_200_OK)
        # result = model_to_dict(userYuAnPlan, exclude=["plan", "nodes"])
        # result['nodeOutlineList'] = userYuAnPlan.nodeOutlineList
        # result['created_at'] = userYuAnPlan.created_at.strftime("%Y-%m-%d %H:%M:%S")
        # 通用生成方法
        # node.result = qwty(node.description)
        tmp_param_path = getYuAnParamPath(userYuAnPlan.ctype, userYuAnPlan.yadate)
        if not os.path.exists(tmp_param_path):
            data = {"code": 201, "data": {}, "msg": "参数文件不存在, 请先搜集参数"}
            serializers = ApiAppResponseSerializer(data=data, many=False)
            serializers.is_valid()
            return Response(serializers.data, status=status.HTTP_200_OK)
        
        ctx = {
            "type": userYuAnPlan.ctype,
            "yadate": userYuAnPlan.yadate,
            "plan": model_to_dict(userYuAnPlan, exclude=["html_data", "html_data", "created_at", "updated_at", "nodes"]),
            "param_path": tmp_param_path,
            "results": {"apiname":"ylh_yadata"}
        }
        logger.info("预案参数:%s"% ctx)
        for node in userYuAnPlan.nodes.all():
            pf = PlanFactory(context=ctx, node=node)
            pf.make_context_api()

        data = {"code": 200, "msg": "success", "data": ctx['results'], "success": True}
        bars = ApiAppResponseSerializer(data=data, many=False)
        bars.is_valid()
        return Response(bars.data, status=status.HTTP_200_OK)


class OutlineApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = ApiAppResponseSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @swagger_auto_schema(
        operation_summary='[可用] 大纲生成',
        operation_description='POST /apiapp/api/outline/',
        manual_parameters=[
            openapi.Parameter(
                name='mid',
                in_=openapi.IN_FORM,
                description='模型ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='question',
                in_=openapi.IN_FORM,
                description='大纲描述',
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
        mid = request.data.get("mid", 0)
        question = request.data.get("question", None)
        histstr = request.data.get("history", None)
        print("histstr->", histstr)
        tmpmodel = None
        if mid is not None:
            try:
                tmpmodel = KgModel.objects.get(id=mid)
            except:
                pass
        if histstr:
            histstr = "[" + histstr + "]"
            try:
                histories = json.loads(histstr)
                history = [[ent['question'], ent['answer']] for ent in histories]
            except:
                history = []
        else:
            history = []

        payload = {"question": question, "history": history}
        print("OutlineApiView:", payload)
        if tmpmodel:
            outlinedata = prod_outline(payload, postmethod=tmpmodel.req_type, url=tmpmodel.url)
        else:
            outlinedata = prod_outline(payload)
        print("rt:", outlinedata)
        if not outlinedata:
            data = {"code": 201, "msg": "大模型解析出问题了","success": False,"data": None}
        else:
            data = {"code": 200, "msg": "成功","success": True,"data": outlinedata}
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class OlineQAApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 问答生产',
        operation_description='POST /apiapp/api/onlineqa/',
        manual_parameters=[
            openapi.Parameter(
                name='mid',
                in_=openapi.IN_FORM,
                description='模型ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='query',
                in_=openapi.IN_FORM,
                description='问题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='tag_list',
                in_=openapi.IN_FORM,
                description='标签列表, 英文逗号分隔',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='conversation_id',
                in_=openapi.IN_FORM,
                description='上个对话ID',
                type=openapi.TYPE_INTEGER,
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
        mid = request.data.get("mid", None)
        tag_list = request.data.get("tag_list", None)
        tmpmodel = None
        if mid is not None:
            try:
                tmpmodel = KgModel.objects.get(id=mid)
            except:
                pass
        payload = {key: request.data.get(key, None) for key in request.data}
        if tmpmodel:
            print("tmpmodel=>", tmpmodel, tmpmodel.req_type)
            for param in tmpmodel.params:
                print("single param:", param)
                if param.default and param.default != "None" and param.default != "none" and param.default != "":
                    payload[param.name] = param.default
                if param.necessary == 1 and param.name not in payload:
                    data = {"code": 201, "msg": f"缺少{param.name}必须的参数"}
                    serializers = ApiAppResponseSerializer(data=data, many=False)
                    serializers.is_valid()
                    return Response(serializers.data, status=status.HTTP_200_OK)
            print("OlineQAApiView:", payload)
            qa_result = prod_qa(payload, postmethod=tmpmodel.req_type, url=tmpmodel.url)
        else:
            qa_result = prod_qa(payload)
        if not qa_result:
            data = {"code": 201, "msg": "大模型问答出问题了"}
        else:
            data = {"code": 200, "data": qa_result}
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class OlineAbstractApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 摘要生成',
        operation_description='POST /apiapp/api/abstract/',
        manual_parameters=[
            openapi.Parameter(
                name='mid',
                in_=openapi.IN_FORM,
                description='模型ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='text',
                in_=openapi.IN_FORM,
                description='文档内容',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='filenum',
                in_=openapi.IN_FORM,
                description='解析文档个数',
                type=openapi.TYPE_INTEGER
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
        mid = request.data.get("mid", None)
        # query = request.data.get("text", None)
        filenum = int(request.data.get("filenum", 0))
        tmpmodel = None
        if mid is not None:
            try:
                tmpmodel = KgModel.objects.get(id=mid)
            except:
                pass
        payload = {key: request.data.get(key, None) for key in request.data}
        print("payload", payload)
        if tmpmodel:
            print("tmpmodel=>", tmpmodel, tmpmodel.req_type)
            for param in tmpmodel.params:
                if param.default and param.default != "None" and param.default != "none" and param.default != "":
                    payload[param.name] = param.default
                if param.necessary == 1 and param.name not in payload:
                    data = {"code": 201, "msg": f"缺少{param.name}必须的参数"}
                    serializers = ApiAppResponseSerializer(data=data, many=False)
                    serializers.is_valid()
                    return Response(serializers.data, status=status.HTTP_200_OK)
            print("OlineAbstractApiView:", payload)

        files = []
        for i in range(filenum):
            tmp = request.data.get(f"file{i}", None)
            print("-->", i, tmp)
            if tmp is None:
                continue
            local_dir = os.path.join("media", "temps")
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
                print("create", local_dir, "!!!")
            else:
                print("subdir", local_dir, "exist!!!")
            filename = str(tmp)
            new_path = os.path.join(local_dir, filename)
            try:
                f = open(new_path, "wb+")
                for chunk in tmp.chunks():
                    f.write(chunk)
                f.close()
            except:
                continue
            files.append(('files_texts', open(new_path, 'rb')))
        if tmpmodel:
            qa_result = prod_abstract(payload, files=files, postmethod=tmpmodel.req_type, url=tmpmodel.url)
        else:
            qa_result = prod_abstract(payload, files=files)
        if not qa_result:
            data = {"code": 201, "msg": "大模型问答出问题了"}
        else:
            data = {"code": 200, "data": qa_result}
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class TextExtentApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 文本扩写',
        operation_description='POST /apiapp/api/text_extends',
        manual_parameters=[
            openapi.Parameter(
                name='mid',
                in_=openapi.IN_FORM,
                description='模型ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='question',
                in_=openapi.IN_FORM,
                description='大纲描述',
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
        mid = request.data.get("mid", 0)
        question = request.data.get("question", None)
        tmpmodel = None
        if mid is not None:
            try:
                tmpmodel = KgModel.objects.get(id=mid)
            except:
                pass
        # payload = {"question": question}
        payload = {key: request.data.get(key, None) for key in request.data}
        print("TextExtentApiView:", payload)
        if tmpmodel:
            print("tmpmodel=>", tmpmodel, tmpmodel.req_type)
            for param in tmpmodel.params:
                if param.default and param.default != "None" and param.default != "none" and param.default != "":
                    payload[param.name] = param.default
                if param.necessary == 1 and param.name not in payload:
                    data = {"code": 201, "msg": f"缺少{param.name}必须的参数"}
                    serializers = ApiAppResponseSerializer(data=data, many=False)
                    serializers.is_valid()
                    return Response(serializers.data, status=status.HTTP_200_OK)
        print("TextExtentApiView:", payload)
        if tmpmodel:
            outlinedata = prod_extend(payload, postmethod=tmpmodel.req_type, url=tmpmodel.url)
        else:
            outlinedata = prod_extend(payload)
        print("rt:", outlinedata)
        if not outlinedata:
            data = {"code": 201, "msg": "大模型解析出问题了"}
        else:
            data = {"code": 200, "data": outlinedata}
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


class OlineText2SQLApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer
    @swagger_auto_schema(
        operation_summary='[可用] 文本转SQL',
        operation_description='POST /apiapp/api/text2sql/',
        manual_parameters=[
            openapi.Parameter(
                name='mid',
                in_=openapi.IN_FORM,
                description='模型ID',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='query',
                in_=openapi.IN_FORM,
                description='问题',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='conversation_id',
                in_=openapi.IN_FORM,
                description='上个对话ID',
                type=openapi.TYPE_INTEGER,
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
        mid = request.data.get("mid", None)
        tmpmodel = None
        if mid is not None:
            try:
                tmpmodel = KgModel.objects.get(id=mid)
            except:
                pass
        payload = {key: request.data.get(key, None) for key in request.data}
        print("OlineText2SQLApiView:", payload)
        if tmpmodel:
            print("tmpmodel=>", tmpmodel, tmpmodel.req_type)
            for param in tmpmodel.params:
                print("single param:", param)
                if param.default and param.default != "None" and param.default != "none" and param.default != "":
                    payload[param.name] = param.default
                if param.necessary == 1 and param.name not in payload:
                    data = {"code": 201, "msg": f"缺少{param.name}必须的参数"}
                    serializers = ApiAppResponseSerializer(data=data, many=False)
                    serializers.is_valid()
                    return Response(serializers.data, status=status.HTTP_200_OK)
            print("OlineText2SQLApiView:", payload)
            qa_result = prod_text2sql(payload, postmethod=tmpmodel.req_type, url=tmpmodel.url)
        else:
            qa_result = prod_text2sql(payload)

        if not qa_result:
            with codecs.open("text2sql.json", mode='rb') as f:
                qa_result = json.load(f)
            data = {"code": 200, "msg": "默认返回结果", "data": qa_result}
        else:
            if qa_result['code'] == 200 and 'query' in qa_result['data'] and 'sql_text' in qa_result['data']:
                query = qa_result['query']
                sql_text = qa_result['sql_text']
                tmpts, tmpb = KgText2SQL.objects.get_or_create(query=query)
                if tmpb:
                    tmpts.sql_ctt = sql_text
                    tmpts.created_at = datetime.now()
                    tmpts.updated_at = datetime.now()
                    tmpts.save()
                else:
                    print(f"问题 {query} 已经存在!")
            data = {"code": 200, "data": qa_result}
        serializers = ApiAppResponseSerializer(data=data, many=False)
        serializers.is_valid()
        return Response(serializers.data, status=status.HTTP_200_OK)


from langchain_community.graphs import Neo4jGraph
from langchain_community.llms import Ollama
from langchain.chains import GraphCypherQAChain

# class GraphQueryApiView(generics.GenericAPIView):
#     parser_classes = (FormParser, MultiPartParser)
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#
#     @swagger_auto_schema(
#         operation_summary='查询图谱数据',
#         operation_description='POST /apiapp/api/graphquery/',
#         manual_parameters=[
#             openapi.Parameter(
#                 name='query',
#                 in_=openapi.IN_FORM,
#                 description='Query string',
#                 type=openapi.TYPE_STRING
#             ),
#         ],
#         responses={
#             200: openapi.Response('Success', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
#                 'result': openapi.Schema(type=openapi.TYPE_STRING)})),
#             400: "Bad Request",
#         },
#         tags=['api']
#     )
#     def post(self, request, *args, **kwargs):
#         graph = Neo4jGraph(
#             'bolt://localhost:7687',
#             'neo4j',
#             'neo4jneo4j'
#         )
#         llm = Ollama(model="qwen2.5")
#         chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True,return_intermediate_steps=True,allow_dangerous_requests=True ) # 显式允许危险请求
#         query = request.data.get("query", None)
#
#         if not query:
#             return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # 运行查询
#         payload = {"query": query}
#         try:
#             response = chain.run(payload)  # 假设 chain 已在您的 Django 项目中定义
#             result = chain(query)
#             intermediate_steps = result['intermediate_steps'][0]['query']
#             lines = intermediate_steps.strip().splitlines()
#             cypher_statements = [line for line in lines if not line.startswith("cypher")]
#             # 连接剩余的行并输出
#             extracted_cypher = "\n".join(cypher_statements)
#             print("cypher:", extracted_cypher+";")
#         except Exception as e:
#             response = llm.invoke(query)
#             print("-------------------------------------")
#             result = chain(query)
#             intermediate_steps = result['intermediate_steps'][0]['query']
#             lines = intermediate_steps.strip().splitlines()
#             cypher_statements = [line for line in lines if not line.startswith("cypher")]
#             # 连接剩余的行并输出
#             extracted_cypher = "\n".join(cypher_statements)
#             print("cypher:", extracted_cypher+";")
#             #return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#             return Response({"result": response}, status=status.HTTP_200_OK)
#         if response:
#             return Response({"result": response, "cypher": extracted_cypher}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "No result found.", "cypher": extracted_cypher}, status=status.HTTP_404_NOT_FOUND)

# class GraphQueryApiView(generics.GenericAPIView):
#     parser_classes = (FormParser, MultiPartParser)
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#
#     @swagger_auto_schema(
#         operation_summary='查询图谱数据',
#         operation_description='POST /apiapp/api/graphquery/',
#         manual_parameters=[
#             openapi.Parameter(
#                 name='query',
#                 in_=openapi.IN_FORM,
#                 description='Query string',
#                 type=openapi.TYPE_STRING
#             ),
#         ],
#         responses={
#             200: openapi.Response('Success', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
#                 'result': openapi.Schema(type=openapi.TYPE_STRING)})),
#             400: "Bad Request",
#         },
#         tags=['api']
#     )
#     def post(self, request, *args, **kwargs):
#         graph = Neo4jGraph(
#             'bolt://localhost:7687',
#             'neo4j',
#             'neo4jneo4j'
#         )
#         llm = Ollama(model="qwen2.5")  # 使用 OllamaLLM 替代 Ollama
#         chain = GraphCypherQAChain.from_llm(
#             graph=graph,
#             llm=llm,
#             verbose=True,
#             return_intermediate_steps=True,
#             allow_dangerous_requests=True  # 显式允许危险请求
#         )
#         query = request.data.get("query", None)
#
#         if not query:
#             return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             # 使用 invoke 方法替代 run 和 __call__
#             result = chain.invoke({"query": query})
#             intermediate_steps = result['intermediate_steps'][0]['query']
#             lines = intermediate_steps.strip().splitlines()
#             cypher_statements = [line for line in lines if not line.startswith("cypher")]
#
#             # 检查生成的 Cypher 语句是否合法
#             extracted_cypher = "\n".join(cypher_statements)
#             if not extracted_cypher.strip().startswith(("MATCH", "CREATE", "RETURN", "WITH")):
#                 raise ValueError("生成的 Cypher 语句无效")
#
#             # 执行 Cypher 查询
#             response = graph.query(extracted_cypher)
#             if response:
#                 return Response({"result": response, "cypher": extracted_cypher}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "No result found.", "cypher": extracted_cypher}, status=status.HTTP_404_NOT_FOUND)
#
#         except Exception as e:
#             # 如果图数据库查询失败，直接调用大模型
#             print(f"图数据库查询失败: {e}")
#             response = llm.invoke(query)
#             return Response({"result": response}, status=status.HTTP_200_OK)


class GraphQueryApiView(generics.GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ApiAppResponseSerializer

    @swagger_auto_schema(
        operation_summary='查询图谱数据',
        operation_description='POST /apiapp/api/graphquery/',
        manual_parameters=[
            openapi.Parameter(
                name='query',
                in_=openapi.IN_FORM,
                description='Query string',
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response('Success', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'result': openapi.Schema(type=openapi.TYPE_STRING)})),
            400: "Bad Request",
        },
        tags=['api']
    )
    def post(self, request, *args, **kwargs):
        graph = Neo4jGraph(
            'bolt://localhost:7687',
            'neo4j',
            'neo4jneo4j'
        )
        llm = Ollama(model="qwen2.5")  # 使用 OllamaLLM 替代 Ollama
        chain = GraphCypherQAChain.from_llm(
            graph=graph,
            llm=llm,
            verbose=True,
            return_intermediate_steps=True,
            allow_dangerous_requests=True  # 显式允许危险请求
        )
        query = request.data.get("query", None)

        if not query:
            return Response({"error": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 使用 invoke 方法替代 run 和 __call__
            result = chain.invoke({"query": query})
            intermediate_steps = result['intermediate_steps'][0]['query']
            lines = intermediate_steps.strip().splitlines()
            cypher_statements = [line for line in lines if not line.startswith("cypher")]

            # 检查生成的 Cypher 语句是否合法
            extracted_cypher = "\n".join(cypher_statements)
            if not extracted_cypher.strip().startswith(("MATCH", "CREATE", "RETURN", "WITH")):
                raise ValueError("生成的 Cypher 语句无效")

            # 执行 Cypher 查询
            response = graph.query(extracted_cypher)
            if response:
                return Response({"result": response, "cypher": extracted_cypher}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No result found.", "cypher": extracted_cypher},
                                status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # 如果图数据库查询失败，直接调用大模型
            print(f"图数据库查询失败: {e}")
            response = llm.invoke(query)
            return Response({"result": response}, status=status.HTTP_200_OK)
