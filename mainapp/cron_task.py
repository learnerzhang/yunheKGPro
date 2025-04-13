import os
import time
import django
from datetime import datetime, timedelta
from dateutil import relativedelta
import logging
logger = logging.getLogger('kgproj')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
django.setup()
from kgapp.models import KgDoc, KgEntity, KgProductTask, KgEntityAtt, KgRelation, KgQA, KgDataIndex, KgTemplates
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events
#from yaapp.api_hhxq_data import SHJDataFactory
from yaapp.api_ylh_data import YLHDataFactory
print('django-apscheduler starting')
# 或者清空所有任务（谨慎使用）
# DjangoJob.objects.all().delete()
# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")


# @register_job(scheduler, "interval", seconds=60, args=[], id="dataIndexByMinuteJob", replace_existing=True)
# def dataIndexByMinuteJob():
#     # 具体要执行的代码
#     # 统计类型 -> 0(分钟)|1(小时)|2(日级别)|3(月级别)|4|5
#     template_num = len(KgTemplates.objects.all())
#     qa_num = len(KgQA.objects.all())
#     rel_num = len(KgRelation.objects.all())
#     ent_num = len(KgEntity.objects.all())
#     doc_num = len(KgDoc.objects.all())
#
#     now = datetime.now() + timedelta(minutes=-1)
#     minute = now.minute
#     hour = now.hour
#
#     tmpDI = KgDataIndex.objects.create(template_num=template_num, qa_num=qa_num,
#                                        rel_num=rel_num, ent_num=ent_num, doc_num=doc_num,
#                                        span_type=0, span_value="{}时{}分".format(hour, minute),
#                                        updated_at=datetime.now(),
#                                        created_at=datetime.now())
#     tmpDI.save()
#     print('{} 任务运行成功！{}'.format(tmpDI, time.strftime("%Y-%m-%d %H:%M:%S")))

#
# @register_job(scheduler, "cron", hour="*", minute="0", id='dataIndexByHourJob', replace_existing=True)
# def dataIndexByHourJob():
#     # 具体要执行的代码
#     template_num = len(KgTemplates.objects.all())
#     qa_num = len(KgQA.objects.all())
#     rel_num = len(KgRelation.objects.all())
#     ent_num = len(KgEntity.objects.all())
#     doc_num = len(KgDoc.objects.all())
#
#     now = datetime.now() + timedelta(hours=-1)
#     hour = now.hour
#     day = now.day
#     # 统计类型 -> 0(分钟)|1(小时)|2(日级别)|3(月级别)|4|5
#     tmpDI = KgDataIndex.objects.create(template_num=template_num, qa_num=qa_num,
#                                        rel_num=rel_num, ent_num=ent_num, doc_num=doc_num,
#                                        span_type=1, span_value="{}日{}时".format(day, hour),
#                                        updated_at=datetime.now(),
#                                        created_at=datetime.now())
#
#     tmpDI.save()
#     print('{} 任务运行成功！{}'.format(tmpDI, time.strftime("%Y-%m-%d %H:%M:%S")))
#
#
# # 每天的00:00 执行这个任务
# @register_job(scheduler, "cron", day='*', hour="0", minute="0", id='dataIndexByDayJob', replace_existing=True)
# def dataIndexByDayJob():
#     # 具体要执行的代码
#     # 统计类型 -> 0(分钟)|1(小时)|2(日级别)|3(月级别)|4|5
#     template_num = len(KgTemplates.objects.all())
#     qa_num = len(KgQA.objects.all())
#     rel_num = len(KgRelation.objects.all())
#     ent_num = len(KgEntity.objects.all())
#     doc_num = len(KgDoc.objects.all())
#
#     now = datetime.now() + timedelta(days=-1)
#     day = now.day
#     month = now.month
#     tmpDI = KgDataIndex.objects.create(template_num=template_num, qa_num=qa_num,
#                                        rel_num=rel_num, ent_num=ent_num, doc_num=doc_num,
#                                        span_type=2, span_value="{}月{}日".format(month, day),
#                                        updated_at=datetime.now(),
#                                        created_at=datetime.now())
#
#     tmpDI.save()
#     print('{} 任务运行成功！{}'.format(tmpDI, time.strftime("%Y-%m-%d %H:%M:%S")))
#
#
# # 每月的1号00:00 执行这个任务
# @register_job(scheduler, "cron", month='*', day='1', hour="0", minute="0", id='dataIndexByMonthJob',
#               replace_existing=True)
# def dataIndexByMonthJob():
#     # 具体要执行的代码
#     template_num = len(KgTemplates.objects.all())
#     qa_num = len(KgQA.objects.all())
#     rel_num = len(KgRelation.objects.all())
#     ent_num = len(KgEntity.objects.all())
#     doc_num = len(KgDoc.objects.all())
#
#     now = datetime.now() + relativedelta.relativedelta(months=-1)
#     year = now.year
#     month = now.month
#     # 统计类型 -> 0(分钟)|1(小时)|2(日级别)|3(月级别)|4|5
#     tmpDI = KgDataIndex.objects.create(template_num=template_num, qa_num=qa_num,
#                                        rel_num=rel_num, ent_num=ent_num, doc_num=doc_num,
#                                        span_type=3, span_value="{}年{}月".format(year, month),
#                                        updated_at=datetime.now(),
#                                        created_at=datetime.now())
#     tmpDI.save()
#     print('{} 任务运行成功！{}'.format(tmpDI, time.strftime("%Y-%m-%d %H:%M:%S")))


@register_job(scheduler, "cron", day='*', hour="0", minute="0", id='buildJsonDataJob', replace_existing=True)
def buildJsonDataJob():
    try:
        # 调用目标函数
        YLHDataFactory(dataType=4).buildJsonData()
        #SHJDataFactory(dataType=3).buildJsonData()
        print('{} 任务运行成功！{}'.format("buildJsonDataJob", time.strftime("%Y-%m-%d %H:%M:%S")))
    except Exception as e:
        print('{} 任务运行失败：{}'.format("buildJsonDataJob", str(e)))
#每分钟执行一次
@register_job(scheduler, "cron", minute='*', id='buildJsonDataJob_test', replace_existing=True)
def buildJsonDataJob_test():
    print("测试分钟及定时任务")
    #logger.debug("测试分钟及定时任务")
    # try:
    #     # 调用目标函数
    #     YLHDataFactory(dataType=4).buildJsonData()
    #     #SHJDataFactory(dataType=3).buildJsonData()
    #     print('{} Json文件生成任务运行成功！{}'.format("buildJsonDataJob", time.strftime("%Y-%m-%d %H:%M:%S")))
    # except Exception as e:
    #     print('{} 任务运行失败：{}'.format("buildJsonDataJob", str(e)))

# def demo(name):
#     # 具体要执行的代码
#     print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))
#
#
# scheduler.add_job(demo, "interval", seconds=10, args=['arg1'], id="demo", replace_existing=True)


# 监控任务
register_events(scheduler)
# 调度器开始运行
scheduler.start()

while True:
    pass
