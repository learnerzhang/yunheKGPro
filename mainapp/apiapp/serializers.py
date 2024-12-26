from rest_framework import serializers
from modelapp.models import KgModel, KgModelParam

from rest_framework import routers, serializers, viewsets


class KgAPIResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
