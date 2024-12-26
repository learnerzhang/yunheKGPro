import collections

from django.db import models
from django.forms import model_to_dict

from userapp.models import User


# Create your models here.

class KgTableContent(models.Model):
    class Meta:
        verbose_name_plural = '知识库文档目录'
        db_table = 'kg_table_content'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="目录名称", help_text="目录名称", unique=False)
    no = models.IntegerField(verbose_name="目录编号", help_text="目录编号", unique=False, null=True)
    parent_id = models.IntegerField(verbose_name="父节点编号", help_text="父节点编号", unique=False, null=True, default=0)
    order_no = models.IntegerField(verbose_name="顺序编号", help_text="顺序编号", unique=False, null=True)
    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class KgTempTableContent(models.Model):
    class Meta:
        verbose_name_plural = '知识库模板目录'
        db_table = 'kg_temp_table_content'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="目录名称", help_text="目录名称", unique=False)
    no = models.IntegerField(verbose_name="目录编号", help_text="目录编号", unique=True, null=True)
    parent_id = models.IntegerField(verbose_name="父节点编号", help_text="父节点编号", unique=False, null=True, default=0)
    order_no = models.IntegerField(verbose_name="顺序编号", help_text="顺序编号", unique=False, null=True)
    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class KgTag(models.Model):
    class Meta:
        verbose_name_plural = '知识库标签'
        db_table = 'kg_tag'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="标签名称", help_text="标签名称", unique=True)
    desc = models.CharField(max_length=512, verbose_name="标签描述", help_text="标签描述", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)

    def toJson(self):
        return {"id": self.id, "name": self.name, "desc": self.desc, "update_time": self.update_time,
                "create_time": self.create_time}

    @property
    def tabctt(self):
        return ",".join([tt.name for tt in self.kgtabtag_set.all()])


class KgTabTag(models.Model):
    class Meta:
        verbose_name_plural = '一级目录标签'
        db_table = 'kg_tab_tag'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="一级标签名称", help_text="一级标签名称", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    tags = models.ManyToManyField(KgTag, verbose_name="关联标签", blank=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)

    @property
    def tag_list(self):
        # 编写方法 直接将需要的数据格式返回
        tags = []
        for tag in self.tags.all():
            tags.append({'id': tag.id, 'name': tag.name, "update_time": tag.update_time, "create_time": tag.create_time,
                         "tabctt": self.name, "tabctt_id": self.id})
        return tags

    def toJson(self):
        return {"id": self.id, "name": self.name, "tags": self.tag_list, "update_time": self.update_time,
                "create_time": self.create_time}


class KgDoc(models.Model):
    class Meta:
        verbose_name_plural = '知识库文档'
        db_table = 'kg_doc'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    title = models.CharField(max_length=200, verbose_name="文本标题", help_text="文本标题", unique=False)
    size = models.IntegerField(verbose_name="文本大小", help_text="文本大小", null=True)
    type = models.CharField(max_length=20, verbose_name="文本类型", help_text="文本类型", unique=False, null=True)
    desc = models.TextField(verbose_name="文件描述", help_text="文件描述", unique=False, null=True)
    path = models.FileField(upload_to='docs', verbose_name='关联文件')
    star = models.IntegerField(verbose_name="星指数", help_text="星指数", unique=False, null=True, default=0)
    isdelete = models.IntegerField(verbose_name="是否删除", help_text="是否删除", unique=False, null=True)
    prodflag = models.IntegerField(verbose_name="生产状态", help_text="生产状态", null=True, default=0)
    kg_table_content_id = models.ForeignKey(KgTableContent, verbose_name="所属目录", help_text="所属目录", blank=True,
                                            on_delete=models.CASCADE, null=True)
    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)
    tags = models.ManyToManyField(KgTag, verbose_name="文档关联标签", blank=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.title) + " #@ " + str(self.type)

    @property
    def tag_list(self):
        # 编写方法 直接将需要的数据格式返回
        tags = []
        for tag in self.tags.all():
            tags.append({'id': tag.id, 'name': tag.name, "desc": tag.desc})
        return tags

    @property
    def tagstr(self):
        # 编写方法 直接将需要的数据格式返回
        tags = []
        for tag in self.tags.all():
            tags.append(tag.name)
        return ",".join(tags)

    @property
    def filepath(self):
        # 编写方法 直接将需要的数据格式返回
        return self.path.url

    @property
    def kg_user(self):
        # 编写方法 直接将需要的数据格式返回
        return self.kg_user_id.username if self.kg_user_id else ""

    @property
    def kg_ctt(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_table_content_id:
            return self.kg_table_content_id.name
        else:
            return None

    @property
    def kg_ctt_id(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_table_content_id:
            return self.kg_table_content_id.id
        else:
            return None


class KgBusiness(models.Model):
    class Meta:
        verbose_name_plural = '知识库业务表'
        db_table = 'kg_business'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="业务名称", help_text="业务名称", unique=False)
    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)

    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class KgTemplates(models.Model):
    class Meta:
        verbose_name_plural = '知识库业务模板'
        db_table = 'kg_templates'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="模板名称", help_text="模板名称", unique=False)
    desc = models.TextField(verbose_name="模板描述", help_text="模板描述", unique=False, null=True)
    version = models.CharField(max_length=30, verbose_name="版本", help_text="版本", unique=False)
    activate = models.IntegerField(max_length=1, verbose_name="激活状态", help_text="激活状态", unique=False, null=True)
    kg_temp_content_id = models.ForeignKey(KgTempTableContent, verbose_name="所属目录", help_text="所属目录", blank=True,
                                           on_delete=models.CASCADE, null=True)
    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)
    kg_business_id = models.ForeignKey(KgBusiness, verbose_name="业务名称", help_text="业务名称", blank=True,
                                       on_delete=models.CASCADE, null=True)
    path = models.FileField(upload_to='temps', verbose_name='关联文件')

    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name) + " #@ " + str(self.kg_business_id)

    @property
    def kg_user(self):
        # 编写方法 直接将需要的数据格式返回
        return self.kg_user_id.username

    @property
    def kg_business(self):
        # 编写方法 直接将需要的数据格式返回
        return self.kg_business_id.name

    @property
    def filepath(self):
        # 编写方法 直接将需要的数据格式返回
        return self.path.url

    @property
    def kg_ctt(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_temp_content_id:
            return self.kg_temp_content_id.name
        else:
            return None

    @property
    def kg_ctt_id(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_temp_content_id:
            return self.kg_temp_content_id.id
        else:
            return None


class KgProductTask(models.Model):
    class Meta:
        verbose_name_plural = '知识生产'
        db_table = 'kg_product_task'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    name = models.CharField(max_length=200, verbose_name="任务名称", help_text="任务名称", unique=False)

    desc = models.CharField(max_length=512, verbose_name="任务描述", help_text="任务描述", unique=False)

    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)

    kg_doc_ids = models.ManyToManyField(KgDoc, verbose_name="文档关联", blank=True)

    task_type = models.IntegerField(max_length=1, verbose_name="生产类型 0(知识导入)|1(自动生成)|2(全文生产)", help_text="生产类型",
                                    unique=False, null=True)

    task_status = models.IntegerField(max_length=1, verbose_name="任务执行状态", help_text="0|1|2|3", unique=False, null=True)

    update_time = models.DateTimeField(verbose_name="更新时间", null=True)

    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name) + " #@ " + str(self.desc) + " #@ " + str(self.task_status)

    @property
    def kg_doc_type(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_doc_ids:
            return ",".join([doc.type for doc in self.kg_doc_ids.all()])
        else:
            return None

    @property
    def kg_doc(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_doc_ids:
            return [doc.id for doc in self.kg_doc_ids.all()]
        else:
            return []

    @property
    def kg_docid_list(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_doc_ids:
            return [doc.id for doc in self.kg_doc_ids.all()]
        else:
            return []

    @property
    def kg_user(self):
        # 编写方法 直接将需要的数据格式返回
        return self.kg_user_id.username


class KgTask(models.Model):
    class Meta:
        verbose_name_plural = '细分异步执行任务记录'
        db_table = 'kg_task'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    celery_id = models.CharField(max_length=512, verbose_name="异步任务ID", help_text="异步任务ID", unique=False)
    kg_prod_task_id = models.ForeignKey(KgProductTask, verbose_name="关联任务", help_text="关联任务", blank=True,
                                        on_delete=models.CASCADE, null=True)
    task_step = models.IntegerField(max_length=1, verbose_name="任务步骤", help_text="0|1", unique=False, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.kg_prod_task_id) + " #@ " + str(self.celery_id)


class KgQA(models.Model):
    class Meta:
        verbose_name_plural = '问答对结果'
        db_table = 'kg_qa'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    task_id = models.ForeignKey(KgProductTask, verbose_name="任务来源", help_text="任务来源", blank=True,
                                on_delete=models.CASCADE, null=True)
    doc_id = models.ForeignKey(KgDoc, verbose_name="关联文件", help_text="关联文件", blank=True, on_delete=models.CASCADE,
                               null=True)
    kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE,
                                   null=True)
    question = models.CharField(max_length=200, verbose_name="问题", help_text="问题", unique=False)
    answer = models.CharField(max_length=512, verbose_name="答案", help_text="答案", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.question)

    @property
    def kg_user(self):
        # 编写方法 直接将需要的数据格式返回
        return self.kg_user_id.username

    @property
    def doc(self):
        return self.doc_id.title


class KgTmpQA(models.Model):
    class Meta:
        verbose_name_plural = '问答对临时解析结果'
        db_table = 'kg_tmp_qa'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    task_id = models.ForeignKey(KgProductTask, verbose_name="任务来源", help_text="任务来源", blank=True,
                                on_delete=models.CASCADE, null=True)
    doc_id = models.ForeignKey(KgDoc, verbose_name="关联文件", help_text="关联文件", blank=True, on_delete=models.CASCADE,
                               null=True)
    question = models.CharField(max_length=200, verbose_name="问题", help_text="问题", unique=False)
    answer = models.CharField(max_length=512, verbose_name="答案", help_text="答案", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.question)

    @property
    def simqas(self):
        return []

    @property
    def doc(self):
        return self.doc_id.title


class KgUpLoadTemplate(models.Model):
    class Meta:
        verbose_name_plural = '知识上传摸板'
        db_table = 'kg_load_template'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    title = models.CharField(max_length=200, verbose_name="模版描述", help_text="模版描述", unique=False)
    path = models.FileField(upload_to='kguploadtemplates', verbose_name='关联文件')
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    @property
    def filepath(self):
        # 编写方法 直接将需要的数据格式返回
        return self.path.url

    def __str__(self):
        return str(self.id) + " #@ " + str(self.title) + " #@ " + str(self.filepath)


class KgEntityAttrScheme(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识图谱实体属性约束'
        db_table = 'kg_entity_att_scheme'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    attname = models.CharField(max_length=200, verbose_name="实体属性名称", help_text="实体属性名称", unique=False)
    atttype = models.CharField(max_length=200, verbose_name="实体属性类型", help_text="实体属性类型", unique=False)
    attmulti = models.IntegerField(max_length=1, verbose_name="单多值", help_text="0|1", unique=False, null=True)
    attdesc = models.CharField(max_length=512, verbose_name="实体属性描述", help_text="实体属性描述", unique=False, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.attname) + " #@ " + str(self.atttype) + " #@ " + str(
            self.attmulti) + " #@ " + str(self.attdesc)


class KgEntityScheme(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识图谱实体约束'
        db_table = 'kg_entity_scheme'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="实体类型名称", help_text="实体类型名称", unique=False)
    attrs = models.ManyToManyField(KgEntityAttrScheme, verbose_name="属性列表", blank=True)
    color = models.CharField(max_length=200, verbose_name="实体展示颜色", help_text="实体展示颜色", unique=False, default='#9AA1AC')
    size = models.IntegerField(verbose_name="实体展示大小", help_text="实体展示大小", unique=False, default=60)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)

    @property
    def attlist(self):
        # 编写方法 直接将需要的数据格式返回
        ret = []
        for att in self.attrs.all():
            ret.append(model_to_dict(att))
        return ret


class KgRelationScheme(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识图谱关系约束'
        db_table = 'kg_relation_scheme'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="关系名称", help_text="关系名称", unique=False)
    desc = models.CharField(max_length=512, verbose_name="关系描述", help_text="关系描述", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class KgEntityAtt(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识图谱实体属性'
        db_table = 'kg_entity_att'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    attname = models.CharField(max_length=200, verbose_name="实体属性名称", help_text="实体属性名称", unique=False)
    atttvalue = models.CharField(max_length=512, verbose_name="实体属性值", help_text="实体属性值", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.attname) + " #@ " + str(self.atttvalue)


class KgEntity(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识图谱实体'
        db_table = 'kg_entity'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="实体名称", help_text="实体名称", unique=False)
    type = models.CharField(max_length=200, verbose_name="实体类型", help_text="实体类型", unique=False)
    tags = models.ManyToManyField(KgTag, verbose_name="实体标签", blank=True)
    atts = models.ManyToManyField(KgEntityAtt, verbose_name="属性列表", blank=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    task = models.ForeignKey(KgProductTask, verbose_name="关联任务", help_text="关联任务", blank=True, on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)

    @property
    def attlist(self):
        ret = []
        for att in self.atts.all():
            ret.append(model_to_dict(att))
        return ret

    @property
    def taglist(self):
        ret = []
        for att in self.tags.all():
            ret.append(model_to_dict(att))
        return ret

    @property
    def tagliststr(self):
        ret = []
        for att in self.tags.all():
            ret.append(att.name)
        return ",".join(ret)

    @property
    def relations(self):
        results = []
        rels = KgRelation.objects.filter(from_nodeid=self.id).all()
        if rels:
            for rent in rels:
                try:
                    toent = KgEntity.objects.get(id=rent.to_nodeid)
                    results.append({"rel": rent.name, "toNode": toent.name})
                except:
                    print(f"relations: 通过{self.name} {self.type}实体获取{rent.name} TO {rent.to_nodeid} 相关关系错误....")
                    pass
        return results

    @property
    def groupRelations(self):
        r2dstr = collections.defaultdict(str)
        rels = KgRelation.objects.filter(from_nodeid=self.id).all()
        if rels:
            r2d = collections.defaultdict(list)
            for rent in rels:
                try:
                    toent = KgEntity.objects.get(id=rent.to_nodeid)
                    r2d[rent.name].append(toent.name)
                except:
                    print(f"groupRelations: 通过{self.name} {self.type}实体获取{rent.name} TO {rent.to_nodeid} 相关关系错误....")
                    pass
            for k, v in r2d.items():
                r2dstr[k] = ",".join(v)
        return r2dstr


class KgRelation(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识图谱关系'
        db_table = 'kg_relation'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="关系名称", help_text="关系名称", unique=False)
    from_nodeid = models.IntegerField(verbose_name="from node", unique=False, null=True)
    to_nodeid = models.IntegerField(verbose_name="to node", unique=False, null=True)
    task = models.ForeignKey(KgProductTask, verbose_name="关联任务", help_text="关联任务", blank=True, on_delete=models.CASCADE,
                             null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        try:
            fromNode = KgEntity.objects.get(id=self.from_nodeid)
            toNode = KgEntity.objects.get(id=self.to_nodeid)
            return str(self.id) + " #@ " + str(fromNode.name) + " -> " + self.name + " -> " + str(toNode.name)
        except:
            return str(self.id) + " #@ " + self.name


# class KgDDAction(models.Model):
#     class Meta:
#         verbose_name_plural = '调度规则目标'
#         db_table = 'kg_dd_action'

#     id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
#     name = models.CharField(max_length=200, verbose_name="目标名称", help_text="目标名称", unique=False)
#     kg_user_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True, on_delete=models.CASCADE, null=True)
#     update_time = models.DateTimeField(verbose_name="更新时间", null=True)
#     create_time = models.DateTimeField(verbose_name="创建时间", null=True)

#     def __str__(self):
#       return str(self.id) + " #@ " + str(self.name)

#     @property
#     def kguser(self):
#         if self.kg_user_id:
#             return self.kg_user_id.username
#         return ""

class KgDDRuleAttribute(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '调度规则属性'
        db_table = 'kg_dd_attr'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    name = models.CharField(max_length=200, verbose_name="规则名称", help_text="规则名称", unique=False)

    zhName = models.CharField(max_length=200, verbose_name="规则名称", help_text="规则名称", unique=False)

    type = models.IntegerField(max_length=1, verbose_name="类型 1(条件)|2(动作)", help_text="1|2", unique=False, null=True)

    valueType = models.CharField(max_length=200, verbose_name="值类型", help_text="值类型", unique=False)

    update_time = models.DateTimeField(verbose_name="更新时间", null=True)

    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class KgDDRule(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '调度规则'
        db_table = 'kg_dd_rule'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    name = models.CharField(max_length=200, verbose_name="规则名称", help_text="规则名称", unique=False)

    desc = models.CharField(max_length=512, verbose_name="规则描述", help_text="规则描述", unique=False)

    type = models.IntegerField(max_length=1, verbose_name="类型", help_text="0|1  类型. 0:决策树", unique=False, null=True,
                               default=0)

    order = models.IntegerField(max_length=1, verbose_name="优先级", help_text="优先级 （暂未实际使用）", unique=False, null=True)

    attrs = models.ManyToManyField(KgDDRuleAttribute, verbose_name="关联指标", blank=True)

    status = models.IntegerField(max_length=1, verbose_name="1：生效，0：未生效", help_text="1：生效，0：未生效", unique=False,
                                 null=False, default=0)

    action_id = models.IntegerField(verbose_name="目标id", help_text="目标id", unique=False, null=True)

    content = models.TextField(max_length=1024, verbose_name="规则详情", help_text="规则详情", unique=False, null=False,
                               default=0)

    update_time = models.DateTimeField(verbose_name="更新时间", null=True)

    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name) + " #@ " + str(self.desc)

    @property
    def action(self):
        if self.action_id:
            try:
                tmp_obj = KgDDRuleAttribute.objects.get(id=self.action_id)
                return tmp_obj.zhName
            except:
                return ""
        return ""

    @property
    def attrlist(self):
        return ",".join([att.zhName for att in self.attrs.all()])

    @property
    def conditionInfos(self):
        return [model_to_dict(att) for att in self.attrs.all()]


class KgDataIndex(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '知识统计指数'
        db_table = 'kg_data_index'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    template_num = models.IntegerField(verbose_name="模板数量", help_text="模板数量", unique=False, null=True, default=0)

    qa_num = models.IntegerField(verbose_name="问答数量", help_text="问答数量", unique=False, null=True, default=0)

    rel_num = models.IntegerField(verbose_name="关系数量", help_text="问答数量", unique=False, null=True, default=0)

    ent_num = models.IntegerField(verbose_name="实体数量", help_text="实体数量", unique=False, null=True, default=0)

    doc_num = models.IntegerField(verbose_name="文档数量", help_text="文档数量", unique=False, null=True, default=0)

    span_type = models.IntegerField(verbose_name="统计类型 -> 0(分钟)|1(小时)|2(日级别)|3(月级别)|4|5", help_text="统计类型",
                                    unique=False, null=True, default=0)

    span_value = models.CharField(max_length=20, verbose_name="下标间歇值", help_text="下标间歇值", unique=False, null=True,
                                  default="")

    update_time = models.DateTimeField(verbose_name="更新时间", null=True)

    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " @# " + str(self.span_type) + " @# " + str(self.span_value)


class KgText2SQL(models.Model):
    class Meta:
        verbose_name_plural = 'Text2SQL'
        db_table = 'kg_txttosql'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    query = models.CharField(max_length=512, verbose_name="查询语句", help_text="查询语句", unique=False)
    sql_ctt = models.CharField(max_length=512, verbose_name="SQL内容", help_text="SQL内容", unique=False)
    activate = models.IntegerField(choices=((0, '错误'), (1, '正确')), verbose_name='转换状态', default=1)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " @# " + str(self.query) + " @# " + str(self.sql_ctt)

