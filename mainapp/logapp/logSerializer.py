from rest_framework import serializers
from .models import LoginLog, OperationLog

class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'  # 默认输出所有字段

class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'  # 默认输出所有字段
