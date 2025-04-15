from django.apps import AppConfig


class DataAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dataapp'
    verbose_name = '数据接入管理'
    