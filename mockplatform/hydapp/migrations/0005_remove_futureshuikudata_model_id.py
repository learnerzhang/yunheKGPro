# Generated by Django 3.2.18 on 2024-12-17 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hydapp', '0004_remove_futurehedaodata_model_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='futureshuikudata',
            name='model_id',
        ),
    ]
