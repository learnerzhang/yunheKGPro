from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('kgapp', '0001_initial'),  # 根据实际情况修改依赖的迁移文件
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE kg_task CHANGE update_time updated_at DATETIME NULL",
            reverse_sql="ALTER TABLE kg_task CHANGE updated_at update_time DATETIME NULL"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE kg_task CHANGE create_time created_at DATETIME NULL",
            reverse_sql="ALTER TABLE kg_task CHANGE created_at create_time DATETIME NULL"
        ),
    ]