from rest_framework import serializers
from rest_framework import routers, serializers, viewsets



class BaseApiResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    result = serializers.ListField()
    code = serializers.IntegerField()
    total = serializers.IntegerField()
    pageNum = serializers.IntegerField()
    success = serializers.BooleanField()
    msg = serializers.CharField(max_length=200)