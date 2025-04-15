from rest_framework import routers, serializers, viewsets
from userapp.models import User
from common.serializers import BaseSerializer

# Serializers define the API representation.

class UserSerializer(BaseSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    telephone = serializers.CharField(max_length=200)
    icon = serializers.ImageField()
    name = serializers.CharField(max_length=200)
    sex = serializers.IntegerField()
    email = serializers.CharField(max_length=200)
    role = serializers.IntegerField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()

    def validate(self, attrs):
        return attrs

# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer 

class KgUserResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = UserSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)

    def validate(self, attrs):
        return attrs


class KgUserDetailResponseSerializer(BaseSerializer):
    data = UserSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    success = serializers.BooleanField()

    def validate(self, attrs):
        return attrs


class KgMenuSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class KgMenuResponseSerializer(BaseSerializer):
    menus = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgMenuDetailResponseSerializer(BaseSerializer):
    menus = KgMenuSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class RoleSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    user_id = serializers.IntegerField()
    remark = serializers.CharField(max_length=512)
    activate = serializers.IntegerField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    menus = KgMenuSerializer(many=True)

    def validate(self, attrs):
        return attrs
    

class KgRoleDetailResponseSerializer(BaseSerializer):
    data = RoleSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    

class KgRoleResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = RoleSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)

    def validate(self, attrs):
        return attrs