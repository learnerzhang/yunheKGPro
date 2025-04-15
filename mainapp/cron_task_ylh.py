import os
import time
import django
from datetime import datetime, timedelta
from dateutil import relativedelta
import logging
logger = logging.getLogger('kgproj')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
django.setup()
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

from django.db import close_old_connections
@register_job(scheduler, "cron", minute='*/10', id='buildJsonDataJob', replace_existing=True)
def buildJsonDataJob():
    try:
        close_old_connections()  # 重置数据库连接
        YLHDataFactory(dataType=4).buildJsonData()
        logger.info(f'任务运行成功！{time.strftime("%Y-%m-%d %H:%M:%S")}')
    except Exception as e:
        logger.error(f'任务失败：{str(e)}')
    finally:
        close_old_connections()  # 确保连接关闭

# 监控任务
register_events(scheduler)
# 调度器开始运行
scheduler.start()

while True:
    pass
