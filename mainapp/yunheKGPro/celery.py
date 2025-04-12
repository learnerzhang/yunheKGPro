import collections
import pprint
from datetime import datetime
import os
import random
from typing import List

from celery import Celery
from celery import shared_task
import time
import jieba
import jieba.analyse
import codecs
import re
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, JSONLoader, UnstructuredExcelLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from yunheKGPro.settings import MODEL_PATH
from yunheKGPro.neo import Neo4j

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
# 实例化
app = Celery('yunheKGPro')
app.config_from_object('django.conf:settings', namespace='CELERY')
# celery.py
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],  # Replace 'json' with ['json', 'msgpack'] if you use msgpack.
    result_backend='django-db',
    task_result_expires=3600,  # 设置任务结果过期时间
)
app.autodiscover_tasks()

from django.forms.models import model_to_dict


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@shared_task
def add(x, y):
    time.sleep(10)
    return x + y


@shared_task
def importGraphKgByCelery(paramdict):
    """知识图Excel谱导入"""
    from kgapp.models import KgTask, KgEntity, KgProductTask, KgEntityAtt, KgRelation,KgTag
    from celery.result import AsyncResult
    results = {}
    prodtaskid = paramdict['id']
    ent_ids = paramdict['ent_ids']
    replace_id_pairs = paramdict['replace_id_pairs']

    tmptask = KgProductTask.objects.get(id=prodtaskid)
    # 图谱构建中....
    tmptask.task_status = 10
    tmptask.save()
    datatask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).first()
    if datatask is None:
        results = {"code": 202, "msg": "暂无生产子任务失败"}
        return results

    res = AsyncResult(datatask.celery_id)  # 参数为task id
    if not res:
        return results
    print("res.result:", res.result)
    graphPool = res.result['data']
    # 新增实体
    success_cnt = 0
    replace_cnt = 0
    relation_cnt = 0

    neo_ent_cnt = 0
    neo_rel_cnt = 0
    neo_client = None
    try:
        neo_client = Neo4j()
    except:
        print("neo4j 客户端连接出错...")
        pass

    for entType, nodes in dict(graphPool).items():
        for ent in nodes:
            tmpid = int(ent['id'])
            tmpname = ent['name']
            tmptype = ent['entityType']
            tmpattrs = ent['attrs']
            tmptags = ent['tags']
            tmpTaskId = ent['taskId']
            tmprels = ent['relations']
            tmpattvals = ent['attValues']
            if tmpid not in ent_ids:
                continue
            if tmpid in replace_id_pairs:
                # 执行替换属性功能
                repid = replace_id_pairs[tmpid]
                tmp = KgEntity.objects.get(id=repid)
                tmp.name = tmpname
                tmp.save()
                replace_cnt += 1
            else:
                # 新增实体
                tmpTask = KgProductTask.objects.get(id=tmpTaskId)
                tmp, tmpb = KgEntity.objects.get_or_create(name=tmpname, type=tmptype, task=tmpTask)
                if tmpb:
                    success_cnt += 1
                    tmp.created_at = datetime.now()
                    tmp.updated_at = datetime.now()
                    tmp.save()

                # 入库操作
                try:
                    if not neo_client.searchNode(name=tmpname, node_type=tmptype, task_id=tmpTaskId):
                        neo_client.createNode(name=tmpname, node_type=tmptype, task_id=tmpTaskId)
                        neo_ent_cnt += 1
                except:
                    print("neo4j 操作异常...")

            # 增加属性
            if tmpattrs:
                tmp.atts.clear()
                for att in tmpattrs:
                    try:
                        tmpatt, tmpattb = KgEntityAtt.objects.get_or_create(attname=att['attName'],
                                                                            atttvalue=att['attvalue'])
                        if tmpattb:
                            tmpatt.created_at = datetime.now()
                            tmpatt.updated_at = datetime.now()
                            tmpatt.save()
                        tmp.atts.add(tmpatt)
                    except:
                        pass
                tmp.save()
            # 增加实体标签
            if tmptags:
                tmp.tags.clear()
                for tag in tmptags:
                    tmptag, tmptagb = KgTag.objects.get_or_create(name=tag['name'])
                    if tmptagb:
                        tmptag.created_at = datetime.now()
                        tmptag.updated_at = datetime.now()
                        tmptag.save()
                    tmp.tags.add(tmptag)
                tmp.save()
    # 新增关系
    for entType, nodes in dict(graphPool).items():
        for ent in nodes:
            tmpid = int(ent['id'])
            tmpname = ent['name']
            tmptype = ent['entityType']
            tmprels = ent['relations']
            tmpTaskId = ent['taskId']
            if tmpid not in ent_ids:
                continue
            if tmpid in replace_id_pairs:
                # 执行替换属性功能
                repid = replace_id_pairs[tmpid]
                tmp = KgEntity.objects.get(id=repid)
            else:
                tmpTask = KgProductTask.objects.get(id=tmpTaskId)
                tmp, tmpb = KgEntity.objects.get_or_create(name=tmpname, type=tmptype, task=tmpTask)

            for relEnt in tmprels:
                try:
                    relname = relEnt['rel']
                    toName = relEnt['toNodeName']
                    toEnt = KgEntity.objects.filter(name=toName, task=tmpTask).first()
                    tmprel, tmprelb = KgRelation.objects.get_or_create(from_nodeid=tmp.id, name=relname,
                                                                       to_nodeid=toEnt.id, task=tmpTask)
                    if tmprelb:
                        tmprel.created_at = datetime.now()
                        tmprel.updated_at = datetime.now()
                        relation_cnt += 1
                    else:
                        print("KgRel 已经存在", tmprel)

                    try:
                        if not neo_client.searchNodeRelationNode(name1=tmpname, name_type1=tmptype, rel_type=relname,
                                                                 name2=toEnt.name, name_type2=toEnt.type,
                                                                 task_id=tmpTaskId):
                            neo_client.createNodeRelationNode(name1=tmpname, name_type1=tmptype, rel_type=relname,
                                                              name2=toEnt.name, name_type2=toEnt.type,
                                                              task_id=tmpTaskId)
                            neo_rel_cnt += 1
                    except:
                        print("neo4j 操作异常...")
                except:
                    print("数据库 操作异常...")

    # 图谱构建完成....
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    tmptask.task_status = 5
    tmptask.save()
    results = {"code": 200, "msg": f"图谱导入成功 新增实体数量：{success_cnt}, 替换实体：{replace_cnt}, 新增关系：{relation_cnt}, neo4j 入库实体:{neo_ent_cnt}, 入库关系:{neo_rel_cnt}"}
    print("结束处理", tmptask)
    return results


@shared_task
def loadGraphKgFromDoc(paramdict):
    print("开始处理", """知识图Excel谱导入""", paramdict)
    from kgapp.models import KgEntityScheme, KgRelationScheme, KgTask, KgEntity, KgProductTask, KgDoc, KgTmpQA, \
        KgEntityAtt, KgRelation, KgEntityAttrScheme

    results = {}
    if paramdict['doc_ids']:
        tmpdocid = paramdict['doc_ids'][0]
    else:
        return results

    graphPool = collections.defaultdict(list)
    tmpdoc = KgDoc.objects.get(id=tmpdocid)
    prodtaskid = paramdict['id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    print("开始读取t图谱文件:", paramdict)
    if tmpdoc.type == 'xlsx' or tmpdoc.type == 'xls':
        sheets = pd.read_excel(io=tmpdoc.filepath[1:], sheet_name=None, keep_default_na=False)
        cur = 0
        for kEntType, vDat in sheets.items():
            # -> KgEntityScheme 增加实体约束
            tmpEnt, tmpBool = KgEntityScheme.objects.get_or_create(name=kEntType)
            if tmpBool:
                tmpEnt.created_at = datetime.now()
                tmpEnt.updated_at = datetime.now()
                tmpEnt.save()

            rels = [rel.name for rel in KgRelationScheme.objects.all()]
            # vDat = vDat.fillna('')
            vRecords = vDat.to_dict(orient='records')
            attNames = set()
            att2Ent = {}
            # print(kEntType, vRecords)
            for record in vRecords:
                # print("task record:", record)
                tmpRels = []
                tmpTags = []
                attName2Values = {}
                tmpAttrs = []
                tmpNodeName = None
                for attName, attValue in record.items():
                    if attName in rels:
                        for v in str(attValue).split(','):
                            tmpRels.append({'rel': attName, 'toNodeName': v})
                    elif attName == "tag" or attName == "TAG":
                        tmpTags.append({"name": attValue})
                    elif attName == "名称":
                        tmpNodeName = attValue
                    else:
                        try:
                            float(attValue)
                            atttype = "number"
                        except:
                            atttype = "string"
                        attNames.add(attName)
                        attName2Values[attName] = attValue
                        tmpAttrs.append({"attName": attName, "atttype": atttype, "attmulti": 0, "attvalue": attValue})
                        att2Ent[attName] = {"attName": attName, "atttype": atttype, "attmulti": 0}

                if tmpNodeName:
                    cur += 1

                    r2d = collections.defaultdict(list)
                    for tmpRel in tmpRels:
                        r2d[tmpRel['rel']].append(tmpRel['toNodeName'])

                    r2dstr = collections.defaultdict(str)
                    for k, v in r2d.items():
                        r2dstr[k] = ",".join(v)

                    node = {"name": tmpNodeName,
                            "entityType": kEntType,
                            "attrNames": list(attNames),
                            "attValues": attName2Values,
                            "attrs": tmpAttrs,
                            "relations": tmpRels,
                            "groupRelations": r2dstr,
                            "taskId": prodtaskid,
                            "tags": tmpTags, "id": cur
                            }
                    graphPool[kEntType].append(node)


            for k, ent in att2Ent.items():
                tmeas, tmab = KgEntityAttrScheme.objects.get_or_create(attname=ent['attName'], atttype=ent['atttype'], attmulti=0, attdesc=ent['attName'])
                if tmab:
                    tmeas.created_at = datetime.now()
                    tmeas.updated_at = datetime.now()
                    tmeas.save()
                tmpEnt.attrs.add(tmeas)
                tmpEnt.save()

        # 数据导入任务完成
    ##########################################################################
    # pprint.pprint(graphPool)
    # 数据导入任务完成
    tmptask.task_status = 2
    tmptask.save()
    results['data'] = graphPool
    print("结束处理", tmptask)
    return results


def basesim(single, pools, topK=3, alpha=0.6):
    results = []
    for tmp in pools:
        tmpsim = 1.0 * len(set(tmp.question) & set(single.question)) / len(set(tmp.question) | set(single.question))
        # print(tmpsim, len(set(tmp.question) & set(single.question)) , len(set(tmp.question) | set(single.question)))
        if tmpsim > alpha:
            results.append((tmp, tmpsim))
    ret = sorted(results, key=lambda x: x[1], reverse=True)[:topK]
    data = []
    for ent, sim in ret:
        tmp = model_to_dict(ent)
        tmp['doc'] = ent.doc
        tmp['sim'] = sim
        data.append(tmp)
    return data


def topkSimEntiy(single, pools, topK=3, alpha=0.8):

    results = []
    for tmp in pools:
        tmpsim = 1.0 * len(set(tmp.name) & set(single['name'])) / len(set(tmp.name) | set(single['name']))
        # print(tmpsim, len(set(tmp.question) & set(single.question)) , len(set(tmp.question) | set(single.question)))
        if tmpsim > alpha:
            results.append((tmp, tmpsim))
    data = []
    if results:
        ret = sorted(results, key=lambda x: x[1], reverse=True)[:topK]
        for ent, sim in ret:
            tmp = model_to_dict(ent, exclude=['atts', 'tags'])
            tmp['sim'] = sim
            tmp['attlist'] = ent.attlist
            tmp['taglist'] = ent.taglist
            tmp['tagliststr'] = ent.tagliststr
            tmp['relations'] = ent.relations
            tmp["groupRelations"] = ent.groupRelations
            data.append(tmp)
    return data


@shared_task
def importKgGraphSimTask(paramdict):
    """
        手动导入知识图谱实体相似比对
    """
    from kgapp.models import KgEntityScheme, KgRelationScheme, KgTask, KgEntity, KgProductTask, KgDoc, KgTmpQA, \
        KgEntityAtt, KgRelation

    print("开始相似比对生产任务", paramdict)
    results = {}
    docids = paramdict['doc_ids']
    prodtaskid = paramdict['id']
    try:
        tmptask = KgProductTask.objects.get(id=prodtaskid)
    except:
        results['data'] = {}
        return results

    datatask = KgTask.objects.filter(kg_prod_task_id=tmptask, task_step=0).first()
    from celery.result import AsyncResult
    res = AsyncResult(datatask.celery_id)  # 参数为task id
    if not res:
        # 数据导入任务完成
        results['data'] = {}
        return results
    graphPool = res.result['data']
    # node = {"name": tmpNodeName,
    #         "entityType": kEntType,
    #         "attrNames": list(attNames),
    #         "attValues": attName2Values,
    #         "attrs": tmpAttrs,
    #         "relations": tmpRels,
    #         "tags": tmpTags}
    # graphPool[kEntType].append(node)
    simGraphPool = collections.defaultdict(list)
    for kEntType, kNodes in dict(graphPool).items():
        # 限制同类型比较
        baseEntList = KgEntity.objects.filter(type=kEntType).all()
        if not baseEntList:
            continue
        for node in kNodes:
            tmpsims = topkSimEntiy(node, baseEntList)
            print("比对-->", node, baseEntList, tmpsims)
            if tmpsims:
                node['siments'] = tmpsims
                simGraphPool[kEntType].append(node)

    results['data'] = simGraphPool
    tmptask.task_status = 4
    tmptask.save()
    return results

@shared_task
def loadKgFromDoc(paramdict):
    from kgapp.models import KgEntityScheme, KgRelationScheme, KgTask, KgEntity, KgProductTask, KgDoc, KgTmpQA, \
        KgEntityAtt, KgRelation

    results = {}
    if paramdict['doc_ids']:
        tmpdocid = paramdict['doc_ids'][0]
    else:
        return results
    
    tmpdoc = KgDoc.objects.get(id=tmpdocid)
    prodtaskid = paramdict['id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    print("开始读取文件", paramdict)

    data = []
    if tmpdoc.type == 'txt':
        with codecs.open(tmpdoc.filepath[1:], mode='r', encoding="utf8") as f:
            cur = 0
            tmp_qest = None
            tmp_answ = None
            for line in f:
                line = line.strip()
                cur += 1
                if line.startswith("指令"):
                    tmp_qest = re.split(":|：", line)[-1]
                if line.startswith("回复"):
                    tmp_answ = re.split(":|：", line)[-1]
                if cur%2 == 0 and tmp_qest and tmp_answ:
                    tmpqa, tmpb = KgTmpQA.objects.get_or_create(task_id=tmptask, doc_id=tmpdoc, question=tmp_qest, answer=tmp_answ)
                    if tmpb:
                        tmpqa.updated_at = datetime.now()
                        tmpqa.created_at = datetime.now()
                        tmpqa.save()
                        print(f"入临时库成功==> [{tmp_qest}, {tmp_answ}]",)
                    else:
                        print(f"已经存在==> [{tmp_qest}, {tmp_answ}]",)

                    data.append(dict(task_id=prodtaskid, 
                                     doc_id=tmpdocid,
                                     question=tmp_qest, 
                                     answer=tmp_answ, 
                                     id=tmpqa.id, 
                                     doc=tmpdoc.title,
                                     simqas=[]))
                    
    if tmpdoc.type == 'xlsx' or  tmpdoc.type == 'xls' or  tmpdoc.type == 'csv':
        if tmpdoc.type == 'csv':
            tmpdf = pd.read_csv(tmpdoc.filepath[1:], encoding="gbk")
        else:
            tmpdf = pd.read_excel(io=tmpdoc.filepath[1:])
        
        tmpdf = tmpdf.fillna('')
        for _, row in tmpdf.iterrows():
            tmp_qest = row[r'指令']
            tmp_answ = row[r'回复']
            tmpqa, tmpb = KgTmpQA.objects.get_or_create(task_id=tmptask, doc_id=tmpdoc, question=tmp_qest, answer=tmp_answ)
            if tmpb:
                tmpqa.created_at = datetime.now()
                tmpqa.updated_at = datetime.now()
                tmpqa.save()
                print(f"入临时库成功==> [{tmp_qest}, {tmp_answ}]",)
            else:
                print(f"已经存在==> [{tmp_qest}, {tmp_answ}]",)
            data.append(dict(task_id=prodtaskid, 
                                     doc_id=tmpdocid,
                                     question=tmp_qest, 
                                     answer=tmp_answ, 
                                     id=tmpqa.id, 
                                     doc=tmpdoc.title,
                                     simqas=[]))
    ##########################################################################
    # 数据导入任务完成
    tmptask.task_status = 2
    tmptask.save()
    print("结束处理", tmptask)
    results['data'] = data
    return results


@shared_task
def productKgSimTask(paramdict):
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from django.forms.models import model_to_dict

    print("开始生产任务", paramdict)
    results = {}
    if paramdict['doc_ids']:
        tmpdocid = paramdict['doc_ids'][0]
    else:
        return results
    results = {}
    prodtaskid = paramdict['id']

    try:
        tmptask = KgProductTask.objects.get(id=prodtaskid)
    except:
        results['code'] = 201
        results['msg'] = "生产任务不存在"
        results['data'] = []
        return results
    try:
        tmpdoc = KgDoc.objects.get(id=tmpdocid)
    except:
        results['code'] = 202
        results['msg'] = "生产文档不存在"
        results['data'] = []
        return results
    # 真实库的数据
    qaliblist = KgQA.objects.all()
    tmpqalist = KgTmpQA.objects.filter(task_id=tmptask, doc_id=tmpdoc)
    
    data = []
    if qaliblist:
        for tmpq in tmpqalist:
            tmpdict = model_to_dict(tmpq)
            simqas = basesim(tmpq, qaliblist)
            tmpdict['doc'] = tmpq.doc
            tmpdict['simqas'] = simqas
            data.append(tmpdict)
    else:
        for tmpq in tmpqalist:
            tmpdict = model_to_dict(tmpq)
            tmpdict['doc'] = tmpq.doc
            tmpdict['simqas'] = []
            data.append(tmpdict)
    results['data'] = data

    tmptask.task_status = 4
    tmptask.save()
    return results


def req_auto_extract_qas(iptdoc, timeout=6000):
    import requests
    filepath = iptdoc.filepath[1:]
    filetype = iptdoc.type
    print("开始生产--->", filepath, filetype)
    tag_list = ",".join([tag.name for tag in iptdoc.tags.all()])
    url = "http://10.4.145.209:8000/qa/Extract_QA_pairs/"
    payload = {"type_word": filetype, "tag_list": tag_list, "filepath": iptdoc.filepath, "filename": iptdoc.title}
    files = {"text_file": open(filepath, mode='rb')}
    headers = {}
    # response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=timeout)
    # retJson = response.json()
    # if 'code' in retJson and 'data' in retJson and  retJson['code'] == 200:
    #     return retJson['data']
    # else:
    #     return []
    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=timeout)
        retJson = response.json()
        if 'code' in retJson and 'data' in retJson and  retJson['code'] == 200:
            return retJson['data']
        else:
            return []
    except:
        return []


def req_full_extract(iptdoc, timeout=6000):
    import requests
    filepath = iptdoc.filepath[1:]
    filetype = iptdoc.type
    print("全文开始生产--->", filepath, filetype)
    url = "http://10.4.145.209:8000/qa/Texts_reading/"
    # files = {"text_file": open(filepath, mode='rb')}
    files = [
        ('files_texts', open(filepath, mode='rb')),
    ]
    headers = {}
    payload = {}
    try:
        response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=timeout)
        retJson = response.json()
        if 'code' in retJson and 'data' in retJson and  retJson['code'] == 200:
            return retJson['data']
        else:
            return []
    except:
        return []

@shared_task
def autoProWithLLM(paramdict):
    """
        自动抽取问答对，模型配置
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from django.forms.models import model_to_dict
    print("开始自动生产任务", paramdict)

    results = {}
    docids = paramdict['doc_ids']
    prodtaskid = paramdict['id']
    try:
        tmptask = KgProductTask.objects.get(id=prodtaskid)
    except:
        results['code'] = 201
        results['msg'] = "生产任务不存在"
        results['data'] = []
        return results
    try:
        tmpdocs = KgDoc.objects.filter(id__in=docids)
    except:
        results['code'] = 202
        results['msg'] = "生产文档不存在"
        results['data'] = []
        return results

    # alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
    data = []
    for tmpdoc in tmpdocs:
        qaparis = req_auto_extract_qas(tmpdoc)
        print(tmpdoc, "生产结果--->", qaparis)
        for ent in qaparis:
            if 'question' not in ent:
                continue
            if 'answer' not in ent:
                continue
            tmp_qest = ent['question']
            tmp_answ = ent['answer']
            print("生产Single结果-->", tmp_qest, tmp_answ)
            try:
                tmqa, _ = KgTmpQA.objects.get_or_create(task_id=tmptask, doc_id=tmpdoc, question=tmp_qest, answer=tmp_answ)
                tmqa.created_at = datetime.now()
                tmqa.updated_at = datetime.now()
                tmqa.save()
                data.append(dict(task_id=prodtaskid,
                                            doc_id=tmpdoc.id,
                                            question=tmp_qest,
                                            answer=tmp_answ,
                                            id=tmqa.id,
                                            doc=tmpdoc.title,
                                            simqas=[]))
            except:
                pass

    prodtaskid = paramdict['id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    tmptask.task_status = 2
    tmptask.save()
    print("结束处理", tmptask)
    results['data'] = data
    return results

@shared_task
def autoProSimQATask(paramdict):
    """
        自动抽取问答对
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from django.forms.models import model_to_dict
    print("开始自动生产任务", paramdict)
    results = {}
    docids = paramdict['doc_ids']
    prodtaskid = paramdict['id']
    try:
        tmptask = KgProductTask.objects.get(id=prodtaskid)
    except:
        results['code'] = 201
        results['msg'] = "生产任务不存在"
        results['data'] = []
        return results
    try:
        tmpdocs = KgDoc.objects.filter(id__in=docids)
    except:
        results['code'] = 202
        results['msg'] = "生产文档不存在"
        results['data'] = []
        return results
    data = []

    # 真实库的数据
    qaliblist = KgQA.objects.all()
    tmpqalist = KgTmpQA.objects.filter(task_id=tmptask, doc_id__in=tmpdocs)
    print("qa target:", len(tmpqalist))
    if qaliblist:
        for tmpq in tmpqalist:
            tmpdict = model_to_dict(tmpq)
            simqas = basesim(tmpq, qaliblist)
            tmpdict['doc'] = tmpq.doc
            tmpdict['simqas'] = simqas
            data.append(tmpdict)
    else:
        for tmpq in tmpqalist:
            tmpdict = model_to_dict(tmpq)
            tmpdict['doc'] = tmpq.doc
            tmpdict['simqas'] = []
            data.append(tmpdict)
    results['data'] = data
    tmptask.task_status = 4
    tmptask.save()
    return results


@shared_task
def autoFullProWithLLM(paramdict):
    """
        全文生产，模型配置
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from django.forms.models import model_to_dict
    print("开始自动生产任务", paramdict)

    results = {}
    docids = paramdict['doc_ids']
    prodtaskid = paramdict['id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    tmpdocs = KgDoc.objects.filter(id__in=docids).all()

    alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
    data = []
    for tmpdoc in tmpdocs:
        # tmp_desc = "".join(list(random.sample(alphabet, random.randint(10,30))))
        rt_descs = req_full_extract(tmpdoc)
        if rt_descs:
            tmp_desc = rt_descs[0]
        else:
            tmp_desc = ""
        tmpdict = model_to_dict(tmpdoc, exclude=['path', 'tags'])
        tmpdict['kg_user'] = tmpdoc.kg_user
        tmpdict['kg_ctt'] = tmpdoc.kg_ctt
        tmpdict['kg_ctt_id'] = tmpdoc.kg_ctt_id
        tmpdict['filepath'] = tmpdoc.filepath
        tmpdict['desc'] = tmp_desc
        data.append(tmpdict)
    
    prodtaskid = paramdict['id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    tmptask.task_status = 4
    tmptask.save()
    print("结束处理", tmptask)
    results['data'] = data
    return results


@shared_task
def autoFullProSimTask(paramdict):
    """
        全文抽取自动抽取问答
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from django.forms.models import model_to_dict
    print("开始自动生产任务", paramdict)
    results = {}
    docids = paramdict['doc_ids']
    prodtaskid = paramdict['id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    results['data'] = []
    tmptask.task_status = 4
    tmptask.save()
    return results



@shared_task
def LLMYuAnProdTask(paramdict):
    """
        预案生产
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from yaapp.models import PlanByUser
    from django.forms.models import model_to_dict
    from yaapp.plan import PlanFactory
    from yaapp import getYuAnParamPath
    
    print("开始自动生产任务", paramdict)
    planId = paramdict['planId']
    prodtaskid = paramdict['task_id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    userYuAnPlan = PlanByUser.objects.get(id=planId)
    print("userYuAnPlan:", userYuAnPlan)
    # 通用生成方法
    # node.result = qwty(node.description)
    results = {}
    tmp_param_path = getYuAnParamPath(userYuAnPlan.ctype, userYuAnPlan.yadate)
    print("预案参数文件路径:", tmp_param_path)
    if not os.path.exists(tmp_param_path):
        data = {"code": 201, "data": {}, "msg": "参数文件不存在, 请先搜集参数"}
        results['data'] = data
        tmptask.task_status = -1
        tmptask.save()
        return results
    
    ctx = {
        "type": userYuAnPlan.ctype,
        "yadate": userYuAnPlan.yadate,
        "plan": model_to_dict(userYuAnPlan, exclude=["html_data", "html_data", "created_at", "updated_at", "nodes"]),
        "param_path": tmp_param_path
    }
    try:
        for node in userYuAnPlan.nodes.all():
            pf = PlanFactory(context=ctx, node=node)
            pf.make_context()
    except Exception as e:
        data = {"code": 201, "data": {}, "msg": "生成失败！"}
        results['data'] = data
        tmptask.task_status = -1
    #### 0 未执行,  1 任务开启, 执行数据装载, 2 数据装载完成, 3 比对任务开启, 4 比对任务完成, 5 最终任务完成, -1 任务失败
    resultJson =  model_to_dict(userYuAnPlan, exclude=['parent', "nodes"])
    resultJson['nodeList'] = userYuAnPlan.nodeDetailList
    data = {"code": 200, "data": resultJson, "msg": "生成成功！"}
    results['data'] = data
    tmptask.task_status = 5
    tmptask.save()
    return results



@shared_task
def knowledgeExtractTask(paramdict):
    """
        知识库文档规则抽取
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgQA
    from yaapp.models import PlanByUser
    from django.forms.models import model_to_dict
    from yaapp.plan import PlanFactory
    from yaapp import getYuAnParamPath
    
    print("开始自动抽取任务", paramdict)
    results = {"code": 200, "data": [], "msg": "生成成功！"}
    return results

@shared_task
def knowledgeParseTask(paramdict):
    """
        知识库文档解析
    """
    from kgapp.models import KgProductTask, KgDoc, KgTmpQA, KgDocCttTag, KgDocFragmentation, Knowledge,KgTableContent
    from yaapp.models import PlanByUser
    from django.forms.models import model_to_dict
    from yaapp.plan import PlanFactory
    from yaapp import getYuAnParamPath
    
    print("开始自动解析任务", paramdict)
    prodtaskid = paramdict['task_id']
    knowledge_id = paramdict['knowledge_id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    tmptask.task_status = 1  # 开始执行
    tmptask.save()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)

    tmpKg = Knowledge.objects.filter(hashid=knowledge_id).first()
    docs = KgDoc.objects.filter(kg_knowledge_id=tmpKg).all()

    for tmpdoc in docs:
        filepath = os.path.join("media", tmpdoc.filepath)
        if filepath.startswith("/"):
            filepath = filepath[1:]
        print("Exist:", os.path.exists(filepath), "Path:", filepath)
        if not os.path.exists(filepath):
            continue
        # filepath="D://workspace//yunheKGProWH//data//tst.pdf"# Save the uploaded file to a temporary file
        file_extension = os.path.splitext(filepath)[1]
        if file_extension.lower() == ".pdf":
            docs = PyPDFLoader(file_path=filepath).load()
        elif file_extension.lower() == ".txt":
            docs = TextLoader(file_path=filepath).load()
        elif file_extension.lower() == ".docx":
            docs = Docx2txtLoader(file_path=filepath).load()
            # docs = UnstructuredExcelLoader(file_path=filepath).load()
        elif file_extension.lower() == '.json':
            docs = JSONLoader(file_path=filepath, jq_schema='.', text_content=False).load()
        else:
            continue
            # raise ValueError(f"Unsupported file type: {file_extension}")
        # 清空历史数据
        
        for kgfrag in KgDocFragmentation.objects.filter(kg_doc_id=tmpdoc).all():
            for tmptag in kgfrag.tags.all():
                tmptag.delete()
            kgfrag.delete()
        # KgDocCttTag.objects.all().delete()
        print("清空Fragment标签")
        chunks = text_splitter.split_documents(docs)
        start = time.time()
        for idx, chunk in enumerate(chunks):
            try:
                # print(f'第 {idx + 1} 个文档:', chunk.page_content)
                # keywords = jieba.analyse.extract_tags(chunk.page_content, topK=10, withWeight=True)
                keywords = jieba.analyse.textrank(chunk.page_content, topK=10, withWeight=True)
                tmpfrag = KgDocFragmentation.objects.create(no=idx+1, 
                                                kg_doc_id=tmpdoc, 
                                                kg_knowledge_id=tmpKg, 
                                                content=chunk.page_content,
                                                ctt_size=len(chunk.page_content),
                                                recall_cnt=0,
                                            )
                for keyword, weight in keywords:
                    tmpTag = KgDocCttTag.objects.create(weight=weight,name=keyword)
                    tmpfrag.tags.add(tmpTag)
                tmpfrag.save()
            except Exception as e:
                print(e)
        tmpdoc.parseflag = 1
        tmpdoc.save()
        print(f'处理完成，耗时: {time.time() - start} 秒')
    results = {"code": 200, "data": [], "msg": "生成成功！"}
    tmptask.task_status = 5
    tmptask.save()
    return results

@shared_task
def knowledgeTrainFaissTask(paramdict):
    """
        知识库文档规则抽取
    """
    from kgapp.models import KgProductTask, Knowledge
    from langchain.document_loaders import DirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    from transformers import AutoTokenizer, AutoModel
    from langchain_core.documents import Document
    
    print("开始训练知识库Faiss模型任务", paramdict)
    prodtaskid = paramdict['task_id']
    knowledge_id = paramdict['knowledge_id']
    tmptask = KgProductTask.objects.get(id=prodtaskid)
    tmptask.task_status = 1  # 开始执行
    tmptask.save()

    tmpKg = Knowledge.objects.filter(hashid=knowledge_id).first()
    if not tmpKg:
        errmsg = "❌ 未找到知识库!"
        print(errmsg)
        results = {"code": 201, "data": [], "msg": errmsg}
        tmptask.task_status = -1
        tmptask.save()
        return results

    # 加载本地 embedding 模型（启用 GPU 加速）
    kgdir = f"data/knowledges/{knowledge_id}"
    if not os.path.exists(kgdir):
        os.makedirs(kgdir)
    index_path = os.path.join(kgdir, "faiss.index")
    embedding = HuggingFaceEmbeddings(
        # model_name="BAAI/bge-small-zh-v1.5",
        model_name=MODEL_PATH,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={
            'batch_size': 64,
            'normalize_embeddings': True
        }
    )

    frags = tmpKg.kgdocfragmentation_set.all()
    if not frags:
        errmsg = "❌ 未找到任何对应的知识片段!"
        print(errmsg)
        results = {"code": 202, "data": [], "msg": errmsg}
        tmptask.task_status = -1
        tmptask.save()
        return results
    
    split_frags = []
    for idx, frag in enumerate(frags):
        split_frags.append(Document(frag.content, metadata={"id": frag.id, "docid": frag.kg_doc_id.id}))

    # 创建向量库
    print("🔄 创建新向量库...")
    # 分批次处理提升性能
    batch_size = 100
    for i in range(0, len(split_frags), batch_size):
        batch = split_frags[i:i+batch_size]
        if i == 0:
            db = FAISS.from_documents(batch, embedding)
        else:
            db.add_documents(batch)
        print(f"进度: {min(i+batch_size, len(split_frags))}/{len(split_frags)}")
    
    print("🔄 保存向量库...")
    db.save_local(index_path)
    print("✅ 向量库保存完成")
    results = {"code": 200, "data": [], "msg": "生成成功！"}
    tmptask.task_status = 5
    tmptask.save()
    return results
