from rest_framework import serializers

class BaseApiResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageNum = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    success = serializers.BooleanField()
    records = serializers.ListField()
    status = serializers.CharField(max_length=20)