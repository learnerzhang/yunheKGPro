# Generated by Django 3.2.18 on 2024-10-29 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kgapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kgtemptablecontent',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
        migrations.AddField(
            model_name='kgtemplates',
            name='kg_business_id',
            field=models.ForeignKey(blank=True, help_text='业务名称', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgbusiness', verbose_name='业务名称'),
        ),
        migrations.AddField(
            model_name='kgtemplates',
            name='kg_temp_content_id',
            field=models.ForeignKey(blank=True, help_text='所属目录', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgtemptablecontent', verbose_name='所属目录'),
        ),
        migrations.AddField(
            model_name='kgtemplates',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
        migrations.AddField(
            model_name='kgtask',
            name='kg_prod_task_id',
            field=models.ForeignKey(blank=True, help_text='关联任务', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgproducttask', verbose_name='关联任务'),
        ),
        migrations.AddField(
            model_name='kgtabtag',
            name='tags',
            field=models.ManyToManyField(blank=True, to='kgapp.KgTag', verbose_name='关联标签'),
        ),
        migrations.AddField(
            model_name='kgtablecontent',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
        migrations.AddField(
            model_name='kgrelation',
            name='task',
            field=models.ForeignKey(blank=True, help_text='关联任务', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgproducttask', verbose_name='关联任务'),
        ),
        migrations.AddField(
            model_name='kgqa',
            name='doc_id',
            field=models.ForeignKey(blank=True, help_text='关联文件', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgdoc', verbose_name='关联文件'),
        ),
        migrations.AddField(
            model_name='kgqa',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
        migrations.AddField(
            model_name='kgqa',
            name='task_id',
            field=models.ForeignKey(blank=True, help_text='任务来源', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgproducttask', verbose_name='任务来源'),
        ),
        migrations.AddField(
            model_name='kgproducttask',
            name='kg_doc_ids',
            field=models.ManyToManyField(blank=True, to='kgapp.KgDoc', verbose_name='文档关联'),
        ),
        migrations.AddField(
            model_name='kgproducttask',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
        migrations.AddField(
            model_name='kgentityscheme',
            name='attrs',
            field=models.ManyToManyField(blank=True, to='kgapp.KgEntityAttrScheme', verbose_name='属性列表'),
        ),
        migrations.AddField(
            model_name='kgentity',
            name='atts',
            field=models.ManyToManyField(blank=True, to='kgapp.KgEntityAtt', verbose_name='属性列表'),
        ),
        migrations.AddField(
            model_name='kgentity',
            name='tags',
            field=models.ManyToManyField(blank=True, to='kgapp.KgTag', verbose_name='实体标签'),
        ),
        migrations.AddField(
            model_name='kgentity',
            name='task',
            field=models.ForeignKey(blank=True, help_text='关联任务', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgproducttask', verbose_name='关联任务'),
        ),
        migrations.AddField(
            model_name='kgdoc',
            name='kg_table_content_id',
            field=models.ForeignKey(blank=True, help_text='所属目录', null=True, on_delete=django.db.models.deletion.CASCADE, to='kgapp.kgtablecontent', verbose_name='所属目录'),
        ),
        migrations.AddField(
            model_name='kgdoc',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
        migrations.AddField(
            model_name='kgdoc',
            name='tags',
            field=models.ManyToManyField(blank=True, to='kgapp.KgTag', verbose_name='文档关联标签'),
        ),
        migrations.AddField(
            model_name='kgddrule',
            name='attrs',
            field=models.ManyToManyField(blank=True, to='kgapp.KgDDRuleAttribute', verbose_name='关联指标'),
        ),
        migrations.AddField(
            model_name='kgbusiness',
            name='kg_user_id',
            field=models.ForeignKey(blank=True, help_text='创建作者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建作者'),
        ),
    ]