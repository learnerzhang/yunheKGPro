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
from yaapp.ylh_interface import generate_rainfall_map,download_map_images,create_flood_control_plan,call_llm_yuan_user_plan,call_llm_yuan_user_word,generate_rainfall_maps
from threading import Lock

resource_lock = Lock()
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
    with resource_lock:  # 👈 加锁
        try:
            close_old_connections()
            YLHDataFactory(dataType=4).buildJsonData()
            logger.info(f'任务运行成功！{time.strftime("%Y-%m-%d %H:%M:%S")}')
        except Exception as e:
            logger.error(f'json数据构建任务失败：{str(e)}')
        finally:
            close_old_connections() # 确保连接关闭


@register_job(scheduler, "cron", minute='*/10', id='generate_rainfall_map_job', replace_existing=True)
def generate_rainfall_map_job():
    """
    每10分钟生成降雨数据图
    """
    with resource_lock:
        try:
            close_old_connections()  # 重置数据库连接
            # 获取前一天的日期（格式YYYYMMDD）
            #download_map_images()
            stdt = "2025042808"  # 支持模糊匹配，如 "20250428"
            # 调用主函数生成降雨图
            image_files = generate_rainfall_maps(stdt=stdt)
            # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            # start_date = f"{yesterday}08"  # 前一天8点
            # end_date = f"{datetime.now().strftime('%Y%m%d')}08"  # 今天8点
            # # 生成文件名带日期
            # #output_filename = f"rainfall_map_{yesterday}.png"
            # # 调用降雨地图生成函数
            #generate_rainfall_map("2024071008", "2024071108", 24, sequence_num=1)
            logger.info(f'降雨地图生成任务成功！时间范围: ')
        except Exception as e:
            logger.error(f'降雨地图生成任务失败：{str(e)}', exc_info=True)
        finally:
            close_old_connections()
    # 监控任务


#@register_job(scheduler, "cron", minute='*/10', id='flood_control_plan_job', replace_existing=True)
@register_job(scheduler, "cron", minute='*/10', id='flood_control_plan_job', replace_existing=True)
def flood_control_plan_job():
    """
    防汛预案定时任务
    每5分钟执行一次，自动创建预案并处理相关数据
    """
    try:
        close_old_connections()  # 重置数据库连接
        # 1. 创建防汛预案
        plan_id = create_flood_control_plan()
        if plan_id:
            logger.info(f"成功创建防汛预案，ID: {plan_id}")
            # 2. 调用预案处理接口
            plan_data = call_llm_yuan_user_plan(ptid=plan_id)
            if plan_data and plan_data.get("code") == 200:
                logger.info("预案数据处理成功")

                # 3. 生成预案文档
                word_data = call_llm_yuan_user_word(id=plan_id)
                if word_data and word_data.get("code") == 200:
                    logger.info("预案文档生成成功")
                else:
                    logger.warning("预案文档生成失败")
            else:
                logger.warning("预案数据处理失败")
        else:
            logger.warning("防汛预案创建失败")

    except Exception as e:
        logger.error(f'防汛预案定时任务失败：{str(e)}', exc_info=True)
    finally:
        close_old_connections()
register_events(scheduler)
# 调度器开始运行
scheduler.start()

while True:
    pass
