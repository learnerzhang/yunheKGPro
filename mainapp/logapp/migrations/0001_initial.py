# Generated by Django 3.2.18 on 2024-10-29 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True, verbose_name='用户姓名')),
                ('username', models.CharField(blank=True, max_length=32, null=True, verbose_name='登录用户名')),
                ('ip', models.CharField(blank=True, max_length=32, null=True, verbose_name='登录ip')),
                ('agent', models.TextField(blank=True, null=True, verbose_name='agent信息')),
                ('browser', models.CharField(blank=True, max_length=200, null=True, verbose_name='浏览器名')),
                ('os', models.CharField(blank=True, max_length=200, null=True, verbose_name='操作系统')),
                ('login_type', models.IntegerField(choices=[(1, '普通登录'), (2, '手机号登录')], default=1, verbose_name='登录类型')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
                'db_table': 'system_login_log',
                'ordering': ('-create_datetime',),
            },
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_modular', models.CharField(blank=True, max_length=64, null=True, verbose_name='请求模块')),
                ('request_path', models.CharField(blank=True, max_length=400, null=True, verbose_name='请求地址')),
                ('request_body', models.TextField(blank=True, null=True, verbose_name='请求参数')),
                ('request_method', models.CharField(blank=True, max_length=8, null=True, verbose_name='请求方式')),
                ('request_msg', models.TextField(blank=True, null=True, verbose_name='操作说明')),
                ('request_ip', models.CharField(blank=True, max_length=32, null=True, verbose_name='请求ip地址')),
                ('request_browser', models.CharField(blank=True, max_length=64, null=True, verbose_name='请求浏览器')),
                ('response_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='响应状态码')),
                ('request_os', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统')),
                ('json_result', models.TextField(blank=True, null=True, verbose_name='返回信息')),
                ('status', models.TextField(verbose_name='响应状态')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'db_table': 'system_operation_log',
                'ordering': ('-create_datetime',),
            },
        ),
    ]