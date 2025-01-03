# Generated by Django 3.2.18 on 2024-10-23 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='模型名称', max_length=200, verbose_name='接口名称')),
                ('no', models.IntegerField(help_text='模型编号', null=True, verbose_name='模型编号')),
                ('function', models.TextField(help_text='接口功能', null=True, verbose_name='接口功能')),
                ('desc', models.TextField(help_text='接口描述', null=True, verbose_name='接口描述')),
                ('url', models.CharField(help_text='接口地址', max_length=200, null=True, verbose_name='接口地址')),
                ('version', models.CharField(help_text='版本号', max_length=200, null=True, verbose_name='版本号')),
                ('req_type', models.IntegerField(help_text='请求方式', max_length=1, null=True, verbose_name='请求方式')),
                ('activate', models.IntegerField(help_text='激活状态', max_length=1, null=True, verbose_name='激活状态')),
                ('update_time', models.DateTimeField(null=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('kg_user_id', models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者')),
            ],
            options={
                'verbose_name_plural': '知识库数据接口',
                'db_table': 'kg_datamodel',
            },
        ),
        migrations.CreateModel(
            name='DataModelParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='参数名称', max_length=20, verbose_name='参数名称')),
                ('type', models.CharField(help_text='参数类型', max_length=20, null=True, verbose_name='参数类型')),
                ('default', models.CharField(help_text='默认值', max_length=20, null=True, verbose_name='默认值')),
                ('desc', models.CharField(help_text='参数说明', max_length=20, null=True, verbose_name='参数说明')),
                ('necessary', models.IntegerField(help_text='必须参数', max_length=1, null=True, verbose_name='必须参数')),
                ('activate', models.IntegerField(help_text='激活状态', max_length=1, null=True, verbose_name='激活状态')),
                ('update_time', models.DateTimeField(null=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('kg_model_id', models.ForeignKey(blank=True, help_text='关联模型', null=True, on_delete=django.db.models.deletion.CASCADE, to='dataapp.datamodel', verbose_name='关联模型')),
            ],
            options={
                'verbose_name_plural': '数据接入接口参数',
                'db_table': 'kg_datamodel_param',
            },
        ),
    ]
