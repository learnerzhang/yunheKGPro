from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from ckeditor.fields import RichTextField
from django.forms import model_to_dict  # 导入 RichTextField
# Create your models here.


class WordParagraph(models.Model):
    """
        文档段落节点内容
    """
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True)
    ctype = models.IntegerField(choices=((0, '标题'), (1, '文本'), (2, '图片'), (3, '表格'), (4, '其他')), default=1, verbose_name='文本类型')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "段落节点内容"
        verbose_name_plural = "段落节点内容"

    def __str__(self):
        return self.content

class TemplateNode(models.Model):
    """
        节点内容
    """
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    template = models.TextField(blank=True)
    result = RichTextField(blank=True)
    wordParagraphs = models.ManyToManyField(WordParagraph, verbose_name="内容节点", blank=True)
    order = models.IntegerField(default=0, help_text="用于排序的字段")  # 新增排序字段
    upload_file_flag = models.BooleanField(default=False, verbose_name="是否上传文件")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def paraglist(self):
        return [model_to_dict(wp) for wp in self.wordParagraphs.all()]
    
    def __str__(self):
        return str(model_to_dict(self, exclude=['parent', 'wordParagraphs']))
    
    class Meta:
        verbose_name = "节点列表"
        verbose_name_plural = "节点列表"


class PlanTemplate(models.Model):
    """
        落盘的预案模板
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # 预案结构
    nodes = models.ManyToManyField(TemplateNode, verbose_name="内容节点", blank=True)
    ctype = models.IntegerField(choices=((0, '黄河中下游'), (1, '小浪底秋汛'), (2, '小浪底调水调沙'), (3, '其他')), default=0, verbose_name='预案模板类型')
    published = models.BooleanField(default=False, verbose_name="发布状态",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def nodelist(self):
        tmpNodes = []
        for node in self.nodes.all():
            tmpN = model_to_dict(node, exclude=['wordParagraphs'])
            tmpN['created_at'] = node.created_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['updated_at'] = node.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['paraglist'] = [model_to_dict(wp) for wp in node.wordParagraphs.all()]
            tmpNodes.append(tmpN)
        return sorted(tmpNodes, key=lambda x: (x['order']))

    @property
    def nodeOutlineList(self):
        tmpNodes = []
        for node in self.nodes.all():
            tmpN = model_to_dict(node, exclude=['wordParagraphs', 'result'])
            tmpN['created_at'] = node.created_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['updated_at'] = node.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpNodes.append(tmpN)
        return sorted(tmpNodes, key=lambda x: (x['order']))

    class Meta:
        verbose_name = "预案模板"
        verbose_name_plural = "预案模板"


class PlanByUser(models.Model):
    """
        用户临时编辑预案模板
    """
    name = models.CharField(max_length=100, blank=True, verbose_name='预案名称')
    yadate = models.CharField(max_length=10, null=True, blank=True,default='2024-01-01', help_text="预案日期")
    nodes = models.ManyToManyField(TemplateNode, verbose_name="内容节点", blank=True)
    ctype = models.IntegerField(choices=((0, '黄河中下游'), (1, '小浪底秋汛'), (2, '小浪底调水调沙'), (3, '三花间'),(4, "其他")), default=0, verbose_name='预案模板类型', blank=True)
    word_data = models.JSONField(verbose_name='word数据', blank=True, null=True)
    html_data = models.JSONField(verbose_name='html数据', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def nodeOutlineList(self):
        tmpNodes = []
        for node in self.nodes.all():
            tmpN = model_to_dict(node, exclude=['wordParagraphs'])
            tmpN['created_at'] = node.created_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['updated_at'] = node.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpNodes.append(tmpN)
        return sorted(tmpNodes, key=lambda x: (x['order']))
    
    @property
    def nodeDetailList(self):
        tmpNodes = []
        for node in self.nodes.all():
            tmpN = model_to_dict(node, exclude=['wordParagraphs'])
            tmpN['created_at'] = node.created_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['updated_at'] = node.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpNodes.append(tmpN)
            # print(node.result)
        return sorted(tmpNodes, key=lambda x: (x['order']))
    
    @property
    def nodelist(self):
        tmpNodes = []
        for node in self.nodes.all():
            tmpN = model_to_dict(node, exclude=['wordParagraphs'])
            tmpN['created_at'] = node.created_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['updated_at'] = node.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            tmpN['paraglist'] = [model_to_dict(wp) for wp in node.wordParagraphs.all()]
            tmpNodes.append(tmpN)
        return sorted(tmpNodes, key=lambda x: (x['order']))
    class Meta:
        verbose_name = "用户临时预案"
        verbose_name_plural = "用户临时预案"


    
class PlanByUserDocument(models.Model):
    """
        用户预案文档
    """
    name = models.CharField(max_length=100)
    document = models.FileField(upload_to='plans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 预案结构来源
    plan = models.ForeignKey(PlanByUser, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "预案文档"
        verbose_name_plural = "预案文档"

