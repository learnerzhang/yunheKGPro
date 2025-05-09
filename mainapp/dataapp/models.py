from django.db import models
from django.forms import model_to_dict
from userapp.models import User
from kgapp.models import KgTag
# Create your models here.
class DataModel(models.Model):
    class Meta:
        verbose_name_plural = '知识库数据接口'
        db_table = 'kg_datamodel'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="接口名称", help_text="模型名称", unique=False)
    no = models.IntegerField(verbose_name="模型编号", help_text="模型编号", unique=False, null=True)
    function = models.TextField(verbose_name="接口功能", help_text="接口功能", unique=False, null=True)
    desc = models.TextField(verbose_name="接口描述", help_text="接口描述", unique=False, null=True)
    url = models.CharField(max_length=200, verbose_name="接口地址", help_text="接口地址", unique=False, null=True)
    # 添加 business_tag 字段，与 KgTag 模型建立映射关系
    business_tag = models.ForeignKey(KgTag, verbose_name="业务标签", help_text="关联的业务标签",on_delete=models.SET_NULL, null=True, blank=True)
    version = models.CharField(max_length=200, verbose_name="版本号", help_text="版本号", unique=False, null=True)
    req_type = models.IntegerField(max_length=1, verbose_name="请求方式", help_text="请求方式", unique=False, null=True)
    activate = models.IntegerField(max_length=1, verbose_name="激活状态", help_text="激活状态", unique=False, null=True)
    kg_user_data_id = models.ForeignKey(User, verbose_name="创建作者", help_text="创建作者", blank=True,
                                   on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)

    @property
    def user_id(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_user_id:
            return self.kg_user_id.pk
        else:
            return None

    @property
    def user_name(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_user_id:
            return self.kg_user_id.username
        else:
            return None

    @property
    def params(self):
        return self.datamodelparam_set.all()


class DataModelParam(models.Model):
    class Meta:
        verbose_name_plural = '数据接入接口参数'
        db_table = 'kg_datamodel_param'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=20, verbose_name="参数名称", help_text="参数名称", unique=False)
    type = models.CharField(max_length=20, verbose_name="参数类型", help_text="参数类型", unique=False, null=True)
    default = models.CharField(max_length=20, verbose_name="默认值", help_text="默认值", unique=False, null=True)
    desc = models.CharField(max_length=20, verbose_name="参数说明", help_text="参数说明", unique=False, null=True)
    necessary = models.IntegerField(max_length=1, verbose_name="必须参数", help_text="必须参数", unique=False,
                                    null=True)
    activate = models.IntegerField(max_length=1, verbose_name="激活状态", help_text="激活状态", unique=False, null=True)
    kg_model_id = models.ForeignKey(DataModel, verbose_name="关联模型", help_text="关联模型", blank=True,
                                    on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name) + " #@ " + str(self.type)

    @property
    def model_id(self):
        # 编写方法 直接将需要的数据格式返回
        if self.kg_model_id:
            return self.kg_model_id.pk
        else:
            return None

class AppAPIModel(models.Model):
    class Meta:
        verbose_name_plural = '应用接口模型'
        db_table = 'kg_appapimodel'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    appname = models.CharField(max_length=200, verbose_name="业务应用名称", help_text="业务应用名称", unique=False)
    appdesc = models.TextField(verbose_name="接口描述", help_text="接口描述", unique=False, null=True)
    appurl = models.CharField(max_length=200, verbose_name="接口地址", help_text="接口地址", unique=False, null=True)
    appkey = models.CharField(max_length=200, verbose_name="接口KEY", help_text="接口KEY", unique=False, null=True)

    tip_type = models.IntegerField(choices=((1, '数据分析'), (2, '其他')), default=1, verbose_name='提示词类型')
    tip_ctt = models.CharField(max_length=200, verbose_name="提示词内容", help_text="提示词内容", unique=False, null=True)

    toolapis = models.ManyToManyField(DataModel, verbose_name="工具集接口", help_text="工具集接口", blank=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.appname)

    @property
    def toollist(self):

        retTools = []
        for tool in self.toolapis.all():
            retTools.append(model_to_dict(tool))
        return retTools