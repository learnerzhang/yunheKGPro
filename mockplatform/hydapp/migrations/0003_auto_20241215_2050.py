# Generated by Django 3.2.18 on 2024-12-15 12:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hydapp', '0002_auto_20241215_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='hedaodata',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, help_text='站名', max_length=200, verbose_name='站名'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hedaodata',
            name='stcd',
            field=models.CharField(default=1, help_text='站号', max_length=200, verbose_name='站号'),
            preserve_default=False,
        ),
    ]