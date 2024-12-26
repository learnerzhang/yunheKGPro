import datetime
import time

from django.db import models

# Create your models here.

class DDPlan(models.Model):
    class Meta:
        verbose_name_plural = '调度方案'
        db_table = 'diaodu_plan'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=512, verbose_name="调度方案名称", help_text="调度方案名称", unique=False)
    update_time = models.DateTimeField(verbose_name="更新时间", null=True, default=datetime.datetime.now())
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, default=datetime.datetime.now())

    def __str__(self):
        return str(self.id) + " @# " + str(self.name)


class WaterRecord(models.Model):
    class Meta:
        managed = True
        verbose_name_plural = '水情数据'
        db_table = 'water_record'

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=200, verbose_name="测点名称", help_text="测点名称", unique=False)
    plan = models.ForeignKey(DDPlan, verbose_name="调度方案名称", help_text="调度方案名称", blank=True, on_delete=models.CASCADE, null=True)

    inq = models.FloatField(verbose_name="入库流量", help_text="入库流量", unique=False, blank=True, default=0)
    inq_sed = models.FloatField(verbose_name="入库含沙", help_text="入库含沙", unique=False, blank=True, default=0)
    otq = models.FloatField(verbose_name="出库流量", help_text="出库流量", unique=False, blank=True, default=0)
    otq_sed = models.FloatField(verbose_name="出库含沙", help_text="出库含沙", unique=False, blank=True, default=0)

    sw = models.FloatField(verbose_name="库水位", help_text="库水位", unique=False, blank=True, default=0)
    capacity = models.FloatField(verbose_name="库容", help_text="库容", unique=False, blank=True, default=0)

    type = models.IntegerField(choices=((0, '水库'), (1, '站点')), verbose_name='测点类型', default=0)
    flow = models.FloatField(verbose_name="流量", help_text="流量", unique=False, blank=True, default=0)

    dt = models.DateField(verbose_name="监测时间", null=True, blank=True)

    update_time = models.DateTimeField(verbose_name="更新时间", null=True, default=datetime.datetime.now())
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, default=datetime.datetime.now())

