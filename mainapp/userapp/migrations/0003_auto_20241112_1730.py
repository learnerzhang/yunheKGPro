# Generated by Django 3.2.15 on 2024-11-12 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_auto_20241030_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 12, 17, 30, 44, 203208), null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 12, 17, 30, 44, 203208), null=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 12, 17, 30, 44, 203208), null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 12, 17, 30, 44, 203208), null=True, verbose_name='更新时间'),
        ),
    ]
