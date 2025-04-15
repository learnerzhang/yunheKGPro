# Create your models here.
import datetime

from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
# 用户表
from django.forms import model_to_dict


class User(AbstractUser):
    # 继承原来的auth表，拓展字段，不要与原来有的字段名重复
    telephone = models.CharField(max_length=11, verbose_name='手机号码')
    icon = models.ImageField(upload_to='icon', default='/icon/default.jpg', verbose_name='用户头像')
    name = models.CharField(max_length=12, verbose_name='用户姓名')
    sex = models.IntegerField(choices=((1, '男'), (0, '女')), default=1, verbose_name='性别')
    role = models.IntegerField(choices=((1, '超级管理员'), (2, '管理员'), (3, '普通用户'), (4, '临时用户')), default=4, verbose_name='用户角色')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="new_user_set",  # 更改 related_name
        related_query_name="user",
    )  

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="new_user_set",  # 更改 related_name
        related_query_name="user",
    )


class Menu(models.Model):
    class Meta:
        verbose_name_plural = '菜单表'
        db_table = 'kg_menu'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    menu_type = models.IntegerField(choices=((0, '目录'), (1, '菜单'), (2, '按钮')), default=0, verbose_name='菜单类型')
    desc = models.CharField(max_length=512, verbose_name="菜单描述", help_text="菜单描述", unique=False, blank=True)
    name = models.CharField(max_length=200, verbose_name="路由名称", help_text="路由名称", unique=False, blank=True)
    title = models.CharField(max_length=200, verbose_name="菜单名称", help_text="菜单名称", unique=False, blank=True)
    auth_ctt = models.CharField(max_length=200, verbose_name="权限标识(菜单)", help_text="权限标识(菜单)", unique=False, blank=True)
    icon = models.CharField(max_length=200, verbose_name="菜单图标", help_text="菜单图标", unique=False,
                            default="ant-design:fund-projection-screen-outlined", blank=True)
    img = models.CharField(max_length=200, verbose_name="菜单图片", help_text="菜单图片", unique=False,
                           default="/resource/image/menu/default.png", blank=True)
    path = models.CharField(max_length=512, verbose_name="路由地址", help_text="路由地址", unique=False, blank=True)
    redirect = models.CharField(max_length=512, verbose_name="重定向", help_text="重定向", unique=False, blank=True)
    component = models.CharField(max_length=512, verbose_name="组件地址", help_text="组件地址", unique=False, blank=True)
    rank = models.IntegerField(verbose_name="排序", help_text="排序", unique=False, null=True, default=0, blank=True)
    father_id = models.IntegerField(verbose_name="父级菜单", help_text="父级菜单", unique=False, null=True, default=0,
                                    blank=True)
    activate = models.IntegerField(choices=((0, '非激活'), (1, '激活')), verbose_name="激活状态", help_text="激活状态", unique=False,
                                   null=True, default=1, blank=True)
    hideMenu = models.IntegerField(choices=((0, '隐藏'), (1, '显示')), verbose_name="是否显示", help_text="是否显示", unique=False,
                                   null=True, default=1, blank=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True, default=datetime.datetime.now())
    created_at = models.DateTimeField(verbose_name="创建时间", null=True, default=datetime.datetime.now())

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name) + " #@ " + str(self.menu_type) + " #@ " + str(self.desc)


class Role(models.Model):
    class Meta:
        verbose_name_plural = '角色表'
        db_table = 'kg_role'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="角色名称", help_text="角色名称", unique=False)
    user_id = models.IntegerField(verbose_name="用户ID", help_text="用户ID", unique=False, null=True, default=0)
    menus = models.ManyToManyField(Menu, verbose_name="关联菜单", blank=True)

    remark = models.CharField(max_length=512, verbose_name="备注", help_text="备注", unique=False)
    activate = models.IntegerField(max_length=1, verbose_name="激活状态", help_text="激活状态", unique=False, null=True,
                                   default=1)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True, default=datetime.datetime.now())
    created_at = models.DateTimeField(verbose_name="创建时间", null=True, default=datetime.datetime.now())

    @property
    def menus_list(self):
        menus_arr = []
        for men in self.menus.all():
            menus_arr.append(model_to_dict(men))
        return menus_arr

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name) + " #@ " + str(self.user_id) + " #@ " + str(self.remark)
