from django.test import TestCase


import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
django.setup()

import os
import django
from django.utils import timezone

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # 替换为您的项目名称
django.setup()

# 导入模型
from userapp.models import User, Role, Menu

def populate_db():
    # 创建用户
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        telephone='12345678901',
        name='测试用户',
        sex=1,
        role=3  # 普通用户
    )
    print(f"用户创建成功: {user.username}")

    # 创建菜单
    menu1 = Menu.objects.create(
        menu_type=1,  # 1 表示菜单
        desc="用户管理菜单",
        name="user_management",
        title="用户管理",
        auth_ctt="user_management",
        icon="ant-design:user-outlined",
        img="/resource/image/menu/user.png",
        path="/users",
        redirect="/users",
        component="UserManagement",
        rank=1,
        father_id=0,  # 顶级菜单
        activate=1,   # 激活
        hideMenu=1,   # 显示
        create_time=timezone.now(),
        update_time=timezone.now()
    )
    print(f"菜单创建成功: {menu1.title}")

    menu2 = Menu.objects.create(
        menu_type=2,  # 2 表示按钮
        desc="添加用户",
        name="add_user",
        title="添加用户",
        auth_ctt="add_user",
        icon="ant-design:plus-outlined",
        img="/resource/image/menu/add_user.png",
        path="/users/add",
        redirect="/users/add",
        component="AddUser",
        rank=2,
        father_id=menu1.id,  # 关联到父级菜单
        activate=1,          # 激活
        hideMenu=1,          # 显示
        create_time=timezone.now(),
        update_time=timezone.now()
    )
    print(f"菜单创建成功: {menu2.title}")
    menu2 = Menu.objects.create(
        menu_type=2,  # 2 表示按钮
        desc="删除用户",
        name="add_user",
        title="删除用户",
        auth_ctt="add_user",
        icon="ant-design:plus-outlined",
        img="/resource/image/menu/add_user.png",
        path="/users/add",
        redirect="/users/add",
        component="AddUser",
        rank=2,
        father_id=menu1.id,  # 关联到父级菜单
        activate=1,          # 激活
        hideMenu=1,          # 显示
        create_time=timezone.now(),
        update_time=timezone.now()
    )
    print(f"菜单创建成功: {menu2.title}")
    # 创建角色并关联菜单
    role = Role.objects.create(
        name='管理员',
        user_id=user.id,
        remark='具有管理员权限',
        activate=1,
        create_time=timezone.now(),
        update_time=timezone.now()
    )
    role.menus.add(menu1, menu2)  # 将菜单关联到角色
    print(f"角色创建成功: {role.name}，并关联菜单。")

if __name__ == '__main__':
    populate_db()


# from userapp.models import Menu
# Create your tests here.
# 创建一个菜单示例
#删除id为 1，2的menu
#Menu.objects.filter(id__in=[1, 2]).delete()
# zhishitongji = Menu.objects.create(
#     menu_type=1,  # 1 表示菜单
#     desc="知识统计",
#     name="user_management",
#     title="知识统计",
#     auth_ctt="user_management",
#     icon="ant-design:user-outlined",
#     img="/resource/image/menu/user.png",
#     path="/users",
#     redirect="/users",
#     component="UserManagement",
#     rank=1,
#     father_id=0,  # 顶级菜单
#     activate=1,   # 激活
#     hideMenu=1    # 显示
# )
#
# # 创建子菜单示例
# shujujieru = Menu.objects.create(
#     menu_type=1,  # 2 表示按钮
#     desc="数据接入",
#     name="add_user",
#     title="数据接入",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
# father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# KNmanage = Menu.objects.create(
#     menu_type=1,  # 2 表示按钮
#     desc="图谱管理",
#     name="add_user",
#     title="图谱管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     father_id=0,  # 顶级菜单
#     rank=2,
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# EntityDefine = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="实体定义",
#     name="add_user",
#     title="实体定义",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=KNmanage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
#
# )
#
# GuanxiDefine = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="关系定义",
#     name="add_user",
#     title="关系定义",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=KNmanage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
#
# )
#
# tupuGenerate = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="图谱生产",
#     name="add_user",
#     title="图谱上产",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=KNmanage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# tpdr = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="图谱导入",
#     name="add_user",
#     title="图谱导入",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=tupuGenerate.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# zdsc = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="自动生产",
#     name="add_user",
#     title="自动生产",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=tupuGenerate.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# tupuyulan = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="图谱预览",
#     name="add_user",
#     title="图谱预览",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=KNmanage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# knowledgeGenerate = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="知识生产",
#     name="add_user",
#     title="知识生产",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# zhishidaoru = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="知识导入",
#     name="add_user",
#     title="知识导入",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=knowledgeGenerate.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# zidongshengchan = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="自动生产",
#     name="add_user",
#     title="自动生产",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=knowledgeGenerate.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# quanwenshengchan = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="全文生产",
#     name="add_user",
#     title="全文生产",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=knowledgeGenerate.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
#
# knowledgeGY = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="知识干预",
#     name="add_user",
#     title="知识干预",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# DocManage = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="文档管理",
#     name="add_user",
#     title="文档管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# TemManage = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="模板管理",
#     name="add_user",
#     title="模板管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# ModelManage = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="模型管理",
#     name="add_user",
#     title="模型管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# UseModel = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="可用模型",
#     name="add_user",
#     title="可用模型",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=ModelManage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# ModelList = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="模型清单",
#     name="add_user",
#     title="模型清单",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=ModelManage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# SystemManage = Menu.objects.create(
#     menu_type=1,  # 1 表示目录
#     desc="系统管理",
#     name="add_user",
#     title="系统管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=0,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# UserManage = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="用户管理",
#     name="add_user",
#     title="用户管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=SystemManage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# RoleManage = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="角色管理",
#     name="add_user",
#     title="角色管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=SystemManage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# LogManage = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="日志管理",
#     name="add_user",
#     title="日志管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=SystemManage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# MenuManage = Menu.objects.create(
#     menu_type=2,  # 2 表示按钮
#     desc="菜单管理",
#     name="add_user",
#     title="菜单管理",
#     auth_ctt="add_user",
#     icon="ant-design:plus-outlined",
#     img="/resource/image/menu/add_user.png",
#     path="/users/add",
#     redirect="/users/add",
#     component="AddUser",
#     rank=2,
#     father_id=SystemManage.id,  # 顶级菜单
#     activate=1,          # 激活
#     hideMenu=1           # 显示
# )
# # 打印创建的菜单
# print(zhishitongji)
# print(shujujieru)