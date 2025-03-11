from rest_framework import serializers
from modelapp.models import KgModel, KgModelParam

from rest_framework import routers, serializers, viewsets


class KgAPIResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    total = serializers.IntegerField()
    pageNum = serializers.IntegerField()
    success = serializers.BooleanField()
    records = serializers.ListField()
    msg = serializers.CharField(max_length=200)


class BaseApiResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    success = serializers.BooleanField()
    records = serializers.ListField()
    status = serializers.CharField(max_length=20)