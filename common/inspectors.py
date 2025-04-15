from drf_yasg.inspectors import FieldInspector
from drf_yasg import openapi
from rest_framework import serializers

class CustomFieldInspector(FieldInspector):
    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        print("inspector field_to_swagger_object", field)
        return super().field_to_swagger_object(field, swagger_object_type, use_references, **kwargs)