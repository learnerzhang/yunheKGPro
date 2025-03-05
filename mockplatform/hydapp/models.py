from django.db import models


class ShuiKu(models.Model):
    class Meta:
        verbose_name_plural = '水库数据表'
        db_table = 'shuiku'
    
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="站名", help_text="站名", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="站号", help_text="站号", unique=False)


class ShuiWen(models.Model):
    class Meta:
        verbose_name_plural = '水文数据表'
        db_table = 'shuiwen'
    
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="站名", help_text="站名", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="站号", help_text="站号", unique=False)


# Create your models here.
class HeDaoData(models.Model):
    class Meta:
        verbose_name_plural = '河道数据表'
        db_table = 'hedao_data'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    sw_pk = models.ForeignKey(ShuiWen, on_delete=models.CASCADE, verbose_name="水文站", null=True)
    name = models.CharField(max_length=200, verbose_name="站名", help_text="站名", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="站号", help_text="站号", unique=False)
    flow_h8 = models.FloatField(verbose_name="流量", null=True)
    date = models.DateTimeField(verbose_name="日期", null=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class ShuiKuData(models.Model):
    class Meta:
        verbose_name_plural = '水库数据表'
        db_table = 'shuiku_data'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    sk_pk = models.ForeignKey(ShuiKu, on_delete=models.CASCADE, verbose_name="水库", null=True)
    name = models.CharField(max_length=200, verbose_name="站名", help_text="站名", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="站号", help_text="站号", unique=False)
    inflow = models.FloatField(verbose_name="入库流量", null=True)
    outflow = models.FloatField(verbose_name="出库流量", null=True)
    sw = models.FloatField(verbose_name="水位", null=True)
    xx_sw = models.FloatField(verbose_name="汛限水位", null=True, )
    xl = models.FloatField(verbose_name="蓄水量（亿m³）", null=True)
    diff_xl = models.FloatField(verbose_name="超蓄水量（亿m³）", null=True)
    sy_kr = models.FloatField(verbose_name="剩余防洪库容（亿m³）", null=True)
    sediment = models.FloatField(verbose_name="淤积量（亿m³）", null=True)
    sediment_rate = models.FloatField(verbose_name="泥沙含量（%）", null=True)
    date = models.DateTimeField(verbose_name="日期", null=True)

    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)

class HoleData(models.Model):
    class Meta:
        verbose_name_plural = '孔洞数据表'
        db_table = 'hole'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    sk_pk = models.ForeignKey(ShuiKu, on_delete=models.CASCADE, verbose_name="水库", null=True)
    name = models.CharField(max_length=200, verbose_name="孔洞名称", help_text="孔洞名称", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="孔洞编号", help_text="孔洞编号", unique=False)
    waterflow = models.FloatField(verbose_name="排水流量", null=True, blank=True)
    date = models.DateTimeField(verbose_name="日期", null=True, blank=True)
    status = models.BooleanField(verbose_name="运行状态", null=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class GenerateSetData(models.Model):
    class Meta:
        verbose_name_plural = '机组数据表'
        db_table = 'generate_set'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    sk_pk = models.ForeignKey(ShuiKu, on_delete=models.CASCADE, verbose_name="水库", null=True)
    name = models.CharField(max_length=200, verbose_name="机组名称", help_text="机组名称", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="机组编号", help_text="机组编号", unique=False)
    capacity = models.FloatField(verbose_name="发电容量", null=True, blank=True)
    power = models.FloatField(verbose_name="发电功率", null=True, blank=True)
    waterflow = models.FloatField(verbose_name="排水流量", null=True, blank=True)
    date = models.DateTimeField(verbose_name="日期", null=True, blank=True)
    status = models.BooleanField(verbose_name="运行状态", null=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class FutureHeDaoData(models.Model):
    class Meta:
        verbose_name_plural = '未来预报河道数据表'
        db_table = 'future_hedao'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    sw_pk = models.ForeignKey(ShuiWen, on_delete=models.CASCADE, verbose_name="水文", null=True)
    model_name = models.CharField(max_length=200, verbose_name="模型名称", help_text="模型名称", unique=False)
    name = models.CharField(max_length=200, verbose_name="站名", help_text="站名", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="站号", help_text="站号", unique=False)
    flow_h8 = models.FloatField(verbose_name="8时流量", null=True)
    date = models.DateTimeField(verbose_name="日期", null=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)


class FutureShuiKuData(models.Model):
    class Meta:
        verbose_name_plural = '未来水库数据表'
        db_table = 'future_shuiku'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    sk_pk = models.ForeignKey(ShuiKu, on_delete=models.CASCADE, verbose_name="水库", null=True)
    model_name = models.CharField(max_length=200, verbose_name="模型名称", help_text="模型名称", unique=False)
    name = models.CharField(max_length=200, verbose_name="站名", help_text="站名", unique=False)
    stcd = models.CharField(max_length=200, verbose_name="站号", help_text="站号", unique=False)
    inflow = models.FloatField(verbose_name="入库流量", null=True)
    outflow = models.FloatField(verbose_name="出库流量", null=True)
    sw = models.FloatField(verbose_name="水位", null=True)
    xx_sw = models.FloatField(verbose_name="汛限水位", null=True, )
    xl = models.FloatField(verbose_name="蓄水量（亿m³）", null=True)
    diff_xl = models.FloatField(verbose_name="超蓄水量（亿m³）", null=True)
    sy_kr = models.FloatField(verbose_name="剩余防洪库容（亿m³）", null=True)
    sediment = models.FloatField(verbose_name="淤积量（亿m³）", null=True)
    sediment_rate = models.FloatField(verbose_name="泥沙含量（%）", null=True)
    date = models.DateTimeField(verbose_name="日期", null=True)

    updated_at = models.DateTimeField(verbose_name="更新时间", null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", null=True)

    def __str__(self):
        return str(self.id) + " #@ " + str(self.name)
