from rest_framework import serializers
from rest_framework import routers, serializers, viewsets



class BaseApiResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    success = serializers.BooleanField()
    status = serializers.CharField(max_length=20)
    