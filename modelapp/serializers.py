from rest_framework import serializers
from modelapp.models import KgModel, KgModelParam

from rest_framework import routers, serializers, viewsets
# Serializers define the API representation.
# class KgModelSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = KgModel
#         fields = ['name', 'no', 'function', 'desc', 'url', 'version', "activate", "kg_user_id", "updated_at", "created_at"]

# # ViewSets define the view behavior.
# class KgModelViewSet(viewsets.ModelViewSet):
#     queryset = KgModel.objects.all()
#     serializer_class = KgModelSerializer 



# class KgModelParamSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = KgModelParam
#         fields = ['name', 'type', 'necessary', 'activate', 'kg_model_id', "updated_at", "created_at"]

# # ViewSets define the view behavior.
# class KgModelParamViewSet(viewsets.ModelViewSet):
#     queryset = KgModelParam.objects.all()
#     serializer_class = KgModelParamSerializer 
class KgModelSerializer(serializers.Serializer):

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
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgModelDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgModelSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)

class KgModelTypeResponseSerializer(serializers.Serializer):
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)

class KgModelResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgModelSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)



class KgModelParamSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50)
    desc = serializers.CharField(max_length=200)
    default = serializers.CharField(max_length=200)
    model_id = serializers.IntegerField()
    necessary = serializers.IntegerField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()

class KgModelParamResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgModelParamSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgModelParamDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgModelParamSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)