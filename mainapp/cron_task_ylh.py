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
from yaapp.ylh_interface import generate_rainfall_map,download_map_images
print('django-apscheduler starting')
# 或者清空所有任务（谨慎使用）
# DjangoJob.objects.all().delete()
# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

from django.db import close_old_connections
@register_job(scheduler, "cron", minute='*', id='buildJsonDataJob', replace_existing=True)
def buildJsonDataJob():
    try:
        close_old_connections()  # 重置数据库连接
        YLHDataFactory(dataType=4).buildJsonData()
        logger.info(f'任务运行成功！{time.strftime("%Y-%m-%d %H:%M:%S")}')
    except Exception as e:
        logger.error(f'json数据构建任务失败：{str(e)}')
    finally:
        close_old_connections()  # 确保连接关闭


@register_job(scheduler, "cron", minute='*', id='generate_rainfall_map_job', replace_existing=True)
def generate_rainfall_map_job():
    """
    每10分钟生成降雨数据图
    """
    try:
        close_old_connections()  # 重置数据库连接
        # 获取前一天的日期（格式YYYYMMDD）
        download_map_images()
        # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        # start_date = f"{yesterday}08"  # 前一天8点
        # end_date = f"{datetime.now().strftime('%Y%m%d')}08"  # 今天8点
        # # 生成文件名带日期
        # #output_filename = f"rainfall_map_{yesterday}.png"
        # # 调用降雨地图生成函数
        # generate_rainfall_map("2024071008", "2024071108", 24, sequence_num=1)
        logger.info(f'降雨地图生成任务成功！时间范围: ')
    except Exception as e:
        logger.error(f'降雨地图生成任务失败：{str(e)}', exc_info=True)
    finally:
        close_old_connections()
    # 监控任务
register_events(scheduler)
# 调度器开始运行
scheduler.start()

while True:
    pass
