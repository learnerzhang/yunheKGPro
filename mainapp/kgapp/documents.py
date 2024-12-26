# 注意, 在app 目录下创建 documents.py 文件   名字一定要对, 不然执行命令时 会找不到索引
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from kgapp.models import KgDoc

@registry.register_document
class KgDocInfDocument(Document):  #  注意命名规范
    doc_id = fields.TextField(
        attr='id',
        fields={
            'raw': fields.KeywordField()
        }
    )
	# 设置关键属性
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.KeywordField()
        }
    )

    desc = fields.TextField(
        attr='desc',
        fields={
            'raw': fields.KeywordField()
        }
    )
    type = fields.TextField(attr='type')
    size = fields.TextField(attr='size')
    kg_user = fields.TextField(attr='kg_user')
    kg_ctt = fields.TextField(attr='kg_ctt')
    # 字典数组字段
    tags = fields.ListField(
        fields.ObjectField(
            properties={
                'name': fields.KeywordField(), 
                'desc': fields.KeywordField(),  # 假设 KgTag 模型有一个 'name' 字段
                # 可以添加其他字段，比如 'description' 等
            }
        )
    )
    kg_ctt_id = fields.TextField(attr='kg_ctt_id')
    score = fields.FloatField(attr='star')
    doc_url = fields.TextField(attr='filepath')
    
    create_time = fields.DateField(attr='create_time')
    update_time = fields.DateField(attr='update_time')

    # attr里填入Django模型的属性名称
    def prepare_tags(self, instance):
        # 将 ManyToManyField 关联的标签转换为字典列表
        return [
            {'name': tag.name, "desc": tag.desc}  # 假设 KgTag 模型有一个 'name' 字段
            for tag in instance.tags.all()
        ]
    def get_queryset(self):
        return super().get_queryset().all()
        # 用于数据库获取数据
    
    
    class Index:
        name = 'docinfo'
        settings = {
            # 设置最大索引深度(**重要)  分页查询时要用到
            'max_result_window': 10000000,
            # 切片个数
            'number_of_shards':8,
            # 保存副本数
            'number_of_replicas':2
        }

    class Django:
        model = KgDoc  # 与此文档关联的模型
        # 要在Elasticsearch中建立索引的模型的字段
         #  fields 置空 则会根据上方的对象的属性进行映射,  可直接写orm模型类字段名, 会根据orm中的字段类型进行自动选择文档字段类型
        fields = []
        # 执行迁移时的 每次从mysql中数据读取的条数. 
        queryset_pagination = 50000