from django.db import models  
from userapp.models import User 
  
class OperationLog(models.Model):  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True)  
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True)  
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True)  
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True)  
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True)  
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True)  
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True)  
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True)  
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True)  
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True)  
    status = models.TextField(verbose_name="响应状态")  
    create_datetime = models.DateTimeField(auto_now_add=True)  
  
    class Meta:  
        db_table = "system_operation_log"  
        verbose_name = "操作日志"  
        verbose_name_plural = verbose_name  
        ordering = ("-create_datetime",)  
  
class LoginLog(models.Model):  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    LOGIN_TYPE_CHOICES = ((1, "普通登录"), (2, "手机号登录"),)
    name = models.TextField(verbose_name="用户姓名", null=True, blank=True) 
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True)  
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True)  
    agent = models.TextField(verbose_name="agent信息", null=True, blank=True)  
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True)  
    os = models.CharField(max_length=200, verbose_name="操作系统", null=True, blank=True)  
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型")  
    create_datetime = models.DateTimeField(auto_now_add=True)  
  
    class Meta:  
        db_table = "system_login_log"  
        verbose_name = "登录日志"  
        verbose_name_plural = verbose_name  
        ordering = ("-create_datetime",)