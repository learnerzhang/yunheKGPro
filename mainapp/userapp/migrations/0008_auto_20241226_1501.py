# Generated by Django 3.2.18 on 2024-12-26 07:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_auto_20241226_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 26, 15, 0, 59, 484829), null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 26, 15, 0, 59, 484829), null=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 26, 15, 0, 59, 484829), null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 26, 15, 0, 59, 484829), null=True, verbose_name='更新时间'),
        ),
    ]
