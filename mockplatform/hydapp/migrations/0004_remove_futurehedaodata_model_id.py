# Generated by Django 3.2.18 on 2024-12-17 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hydapp', '0003_auto_20241215_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='futurehedaodata',
            name='model_id',
        ),
    ]