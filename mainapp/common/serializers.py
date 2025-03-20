from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    success = serializers.BooleanField()
    msg = serializers.CharField(max_length=200)
    


