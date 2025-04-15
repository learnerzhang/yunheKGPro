from rest_framework import serializers
from kgapp.models import KgTableContent, KgDoc, KgTag, KgBusiness, KgTemplates
from rest_framework import routers, serializers, viewsets

from common.serializers import BaseSerializer


class KgAppResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    pageNum = serializers.IntegerField()
    success = serializers.BooleanField()
    records = serializers.ListField()
    msg = serializers.CharField(max_length=200)

# Serializers define the API representation.

class KgDataIndexResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    data = serializers.DictField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTableContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KgTableContent
        fields = ['name', 'no', 'order_no', "kg_user_id", "updated_at", "created_at"]


# ViewSets define the view behavior.
class KgTableContentViewSet(viewsets.ModelViewSet):
    queryset = KgTableContent.objects.all()
    serializer_class = KgTableContentSerializer


class KgDocSerializer(BaseSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    size = serializers.IntegerField()
    type = serializers.CharField()
    star = serializers.IntegerField()
    kg_user = serializers.CharField()
    kg_ctt = serializers.CharField()
    kg_ctt_id = serializers.IntegerField()
    # highlight_title = serializers.CharField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    desc = serializers.CharField()
    filepath = serializers.CharField()
    tag_list = serializers.ListField(read_only=True)

    def validate(self, data):
        return data


class KgDocDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgDocSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgDocResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgDocSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgText2SQLResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgDocIdListResponseSerializer(BaseSerializer):
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTagSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    desc = serializers.CharField(max_length=512)
    tabctt = serializers.CharField(max_length=200)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgTagResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgTagSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgCTTSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent_id = serializers.IntegerField()
    kg_user_id = serializers.IntegerField()

    def validate(self, data):
        return data


class KgTabCTTResponseSerializer(BaseSerializer):
    data = KgCTTSerializer(many=False)
    tabctt = serializers.DictField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgBusSerializer(BaseSerializer):
    name = serializers.CharField(max_length=200)
    kg_user_id = serializers.IntegerField()


class KgBusResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgBusSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTemplateSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()
    version = serializers.CharField()
    kg_user = serializers.CharField()
    kg_ctt = serializers.CharField()
    kg_ctt_id = serializers.IntegerField()
    kg_business = serializers.CharField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    filepath = serializers.CharField()

    def validate(self, data):
        return data


class KgTempResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgTemplateSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTempDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgTemplateSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTaskSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()
    task_type = serializers.IntegerField()
    task_status = serializers.IntegerField()
    kg_user = serializers.CharField()
    kg_doc = serializers.ListField()
    kg_doc_type = serializers.CharField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgTaskDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()

    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTaskSerializer(many=False)


class KgTaskResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()

    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTaskSerializer(many=True)


class KgTaskStatusResponseSerializer(BaseSerializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=20)


class KgTmpQASerializer(BaseSerializer):
    id = serializers.IntegerField()
    answer = serializers.CharField()
    question = serializers.CharField()
    doc = serializers.CharField()
    simqas = serializers.ListField()


class KgTmpQAResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTmpQASerializer(many=True)


class KgTmpQADetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTmpQASerializer(many=False)


class KgGraphResponseSerializer(BaseSerializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = serializers.DictField()


class KgTmeplateSerializer(BaseSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    path = serializers.CharField(max_length=512)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgTaskTemplateResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTmeplateSerializer(many=False)


class KgQASerializer(BaseSerializer):
    id = serializers.IntegerField()
    answer = serializers.CharField()
    question = serializers.CharField()
    doc = serializers.CharField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgQAResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgQASerializer(many=True)


class KgQADetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgQASerializer(many=False)


class KgEntitySerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    attlist = serializers.ListField()
    type = serializers.CharField()
    taglist = serializers.ListField()
    relations = serializers.ListField()
    tagliststr = serializers.CharField()
    groupRelations = serializers.DictField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgEntiyResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySerializer(many=True)


class KgEntityDetailResponseSerializer(BaseSerializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySerializer(many=False)


class KgEntitySchemeSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    color = serializers.CharField()
    size = serializers.IntegerField()
    attlist = serializers.ListField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgEntiySchemeResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySchemeSerializer(many=True)


class KgEntitySchemeDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySchemeSerializer(many=False)


class KgRelationSchemeSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgRelationSchemeResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgRelationSchemeSerializer(many=True)


class KgRelationSchemeDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgRelationSchemeSerializer(many=False)


##############################################################################

# class KgDDActionSerializer(BaseSerializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     kguser = serializers.CharField()
#     updated_at = serializers.DateTimeField()
#     created_at = serializers.DateTimeField()


# class KgDDActionResponseSerializer(BaseSerializer):
#     total = serializers.IntegerField()
#     page = serializers.IntegerField()
#     pageSize = serializers.IntegerField()
#     code = serializers.IntegerField()
#     msg = serializers.CharField(max_length=200)
#     data = KgDDActionSerializer(many=True)


# class KgDDActionDetailResponseSerializer(BaseSerializer):
#     total = serializers.IntegerField()
#     page = serializers.IntegerField()
#     pageSize = serializers.IntegerField()
#     code = serializers.IntegerField()
#     msg = serializers.CharField(max_length=200)
#     data = KgDDActionSerializer(many=False)


class KgDDRuleAttributeSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    zhName = serializers.CharField()
    valueType = serializers.CharField()
    type = serializers.IntegerField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class KgDDRuleAttributeResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleAttributeSerializer(many=True)


class KgDDRuleAttributeDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleAttributeSerializer(many=False)


class KgDDRuleSerializer(BaseSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()

    type = serializers.IntegerField()

    order = serializers.IntegerField()

    action_id = serializers.IntegerField()

    action = serializers.CharField()

    attrlist = serializers.CharField()

    conditionInfos = serializers.ListField()

    content = serializers.CharField()

    status = serializers.IntegerField()

    updated_at = serializers.DateTimeField()

    created_at = serializers.DateTimeField()


class KgDDRuleResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleSerializer(many=True)


class KgDDRuleDetailResponseSerializer(BaseSerializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleSerializer(many=False)


class KgDDRuleResultResponseSerializer(BaseSerializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = serializers.ListField()


class KgGraphResponseSerializer(BaseSerializer):
    nodes = serializers.ListField()
    links = serializers.ListField()
    categories = serializers.ListField()
    nodeNum = serializers.IntegerField()
    linkNum = serializers.IntegerField()
    totalNodeNum = serializers.IntegerField()
    totalLinkNum = serializers.IntegerField()
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


