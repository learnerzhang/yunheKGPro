from django.apps import AppConfig


class ModelappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modelapp'
    verbose_name = '模型管理'
