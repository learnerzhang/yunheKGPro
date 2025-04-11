from rest_framework import serializers

from common.serializers import BaseSerializer


class ApiAppResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageNum = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    records = serializers.ListField()
    status = serializers.CharField(max_length=20)

