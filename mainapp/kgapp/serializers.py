from rest_framework import serializers
from kgapp.models import KgTableContent, KgDoc, KgTag, KgBusiness, KgTemplates
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.

class KgDataIndexResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    data = serializers.DictField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTableContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KgTableContent
        fields = ['name', 'no', 'order_no', "kg_user_id", "update_time", "create_time"]


# ViewSets define the view behavior.
class KgTableContentViewSet(viewsets.ModelViewSet):
    queryset = KgTableContent.objects.all()
    serializer_class = KgTableContentSerializer


class KgDocSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    size = serializers.IntegerField()
    type = serializers.CharField()
    star = serializers.IntegerField()
    kg_user = serializers.CharField()
    kg_ctt = serializers.CharField()
    kg_ctt_id = serializers.IntegerField()
    # highlight_title = serializers.CharField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()
    desc = serializers.CharField()
    filepath = serializers.CharField()
    tag_list = serializers.ListField(read_only=True)

    def validate(self, data):
        return data


class KgDocDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgDocSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgDocResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgDocSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgText2SQLResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgDocIdListResponseSerializer(serializers.Serializer):
    data = serializers.ListField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    desc = serializers.CharField(max_length=512)
    tabctt = serializers.CharField(max_length=200)
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgTagResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgTagSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgCTTSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent_id = serializers.IntegerField()
    kg_user_id = serializers.IntegerField()

    def validate(self, data):
        return data


class KgTabCTTResponseSerializer(serializers.Serializer):
    data = KgCTTSerializer(many=False)
    tabctt = serializers.DictField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgBusSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    kg_user_id = serializers.IntegerField()


class KgBusResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgBusSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTemplateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()
    version = serializers.CharField()
    kg_user = serializers.CharField()
    kg_ctt = serializers.CharField()
    kg_ctt_id = serializers.IntegerField()
    kg_business = serializers.CharField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()
    filepath = serializers.CharField()

    def validate(self, data):
        return data


class KgTempResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgTemplateSerializer(many=True)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTempDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    data = KgTemplateSerializer(many=False)
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)


class KgTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()
    task_type = serializers.IntegerField()
    task_status = serializers.IntegerField()
    kg_user = serializers.CharField()
    kg_doc = serializers.ListField()
    kg_doc_type = serializers.CharField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgTaskDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()

    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTaskSerializer(many=False)


class KgTaskResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()

    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTaskSerializer(many=True)


class KgTaskStatusResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    status = serializers.CharField(max_length=20)


class KgTmpQASerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.CharField()
    question = serializers.CharField()
    doc = serializers.CharField()
    simqas = serializers.ListField()


class KgTmpQAResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTmpQASerializer(many=True)


class KgTmpQADetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTmpQASerializer(many=False)


class KgGraphResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = serializers.DictField()


class KgTmeplateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    path = serializers.CharField(max_length=512)
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgTaskTemplateResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgTmeplateSerializer(many=False)


class KgQASerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.CharField()
    question = serializers.CharField()
    doc = serializers.CharField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgQAResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgQASerializer(many=True)


class KgQADetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgQASerializer(many=False)


class KgEntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    attlist = serializers.ListField()
    type = serializers.CharField()
    taglist = serializers.ListField()
    relations = serializers.ListField()
    tagliststr = serializers.CharField()
    groupRelations = serializers.DictField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgEntiyResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySerializer(many=True)


class KgEntityDetailResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySerializer(many=False)


class KgEntitySchemeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    color = serializers.CharField()
    size = serializers.IntegerField()
    attlist = serializers.ListField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgEntiySchemeResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySchemeSerializer(many=True)


class KgEntitySchemeDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgEntitySchemeSerializer(many=False)


class KgRelationSchemeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    desc = serializers.CharField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgRelationSchemeResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgRelationSchemeSerializer(many=True)


class KgRelationSchemeDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgRelationSchemeSerializer(many=False)


##############################################################################

# class KgDDActionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     kguser = serializers.CharField()
#     update_time = serializers.DateTimeField()
#     create_time = serializers.DateTimeField()


# class KgDDActionResponseSerializer(serializers.Serializer):
#     total = serializers.IntegerField()
#     page = serializers.IntegerField()
#     pageSize = serializers.IntegerField()
#     code = serializers.IntegerField()
#     msg = serializers.CharField(max_length=200)
#     data = KgDDActionSerializer(many=True)


# class KgDDActionDetailResponseSerializer(serializers.Serializer):
#     total = serializers.IntegerField()
#     page = serializers.IntegerField()
#     pageSize = serializers.IntegerField()
#     code = serializers.IntegerField()
#     msg = serializers.CharField(max_length=200)
#     data = KgDDActionSerializer(many=False)


class KgDDRuleAttributeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    zhName = serializers.CharField()
    valueType = serializers.CharField()
    type = serializers.IntegerField()
    update_time = serializers.DateTimeField()
    create_time = serializers.DateTimeField()


class KgDDRuleAttributeResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleAttributeSerializer(many=True)


class KgDDRuleAttributeDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleAttributeSerializer(many=False)


class KgDDRuleSerializer(serializers.Serializer):
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

    update_time = serializers.DateTimeField()

    create_time = serializers.DateTimeField()


class KgDDRuleResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleSerializer(many=True)


class KgDDRuleDetailResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    pageSize = serializers.IntegerField()
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = KgDDRuleSerializer(many=False)


class KgDDRuleResultResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    msg = serializers.CharField(max_length=200)
    data = serializers.ListField()


class KgGraphResponseSerializer(serializers.Serializer):
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



class BaseApiResponseSerializer(serializers.Serializer):
    data = serializers.JSONField()
    code = serializers.IntegerField()
    total = serializers.IntegerField()
    pageNum = serializers.IntegerField()
    success = serializers.BooleanField()
    msg = serializers.CharField(max_length=200)
