# Generated by Django 3.2.18 on 2024-12-31 00:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0008_auto_20241230_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddplan',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 31, 8, 15, 2, 35039), null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='ddplan',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 31, 8, 15, 2, 35039), null=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='waterrecord',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 31, 8, 15, 2, 37038), null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='waterrecord',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 31, 8, 15, 2, 37038), null=True, verbose_name='更新时间'),
        ),
    ]