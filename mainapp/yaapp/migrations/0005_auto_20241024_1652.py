# Generated by Django 3.2.15 on 2024-10-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yaapp', '0004_auto_20241023_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planbyuser',
            name='html_data',
            field=models.JSONField(blank=True, null=True, verbose_name='html数据'),
        ),
        migrations.AlterField(
            model_name='planbyuser',
            name='word_data',
            field=models.JSONField(blank=True, null=True, verbose_name='word数据'),
        ),
    ]