from rest_framework import serializers
from .models import DataModel,DataModelParam

from rest_framework import routers, serializers, viewsets

class DataModelSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    no = serializers.IntegerField()
    function = serializers.CharField(max_length=500)
    desc = serializers.CharField(max_length=500)
    url = serializers.CharField(max_length=500)
    version = serializers.CharField(max_length=500)
    user_id = serializers.IntegerField()
    activate = serializers.IntegerField()
    req_type = serializers.IntegerField()
    user_name = serializers.CharField(max_length=50)
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()
    kgTag_id = serializers.IntegerField(source='business_tag.id', required=False) # 添加 kgTag_id 字段

class DataModelDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = DataModelSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)

class DataModelTypeResponseSerializer(serializers.Serializer):
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)

class DataModelResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = DataModelSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)



class DataModelParamSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50)
    desc = serializers.CharField(max_length=200)
    default = serializers.CharField(max_length=200)
    model_id = serializers.IntegerField()
    necessary = serializers.IntegerField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()

class DataModelParamResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = DataModelParamSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class DataModelParamDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = DataModelParamSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)