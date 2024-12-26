from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 继承原来的auth表，拓展字段，不要与原来有的字段名重复
    telephone = models.CharField(max_length=11, verbose_name='手机号码')
    icon = models.ImageField(upload_to='icon', default='/icon/default.jpg', verbose_name='用户头像')
    name = models.CharField(max_length=12, verbose_name='用户姓名')
    sex = models.IntegerField(choices=((1, '男'), (0, '女')), default=1, verbose_name='性别')
    role = models.IntegerField(choices=((1, '超级管理员'), (2, '管理员'), (3, '普通用户'), (4, '临时用户')), default=4,
                               verbose_name='用户角色')
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="userapp_groups",  # 指定一个不同的 related_name
        related_query_name="userapp",  # 可选，用于查询时使用的名称
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="userapp_user_permissions",  # 指定一个不同的 related_name
        related_query_name="userapp",  # 可选，用于查询时使用的名称
    )