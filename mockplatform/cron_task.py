import os
import time
import django
from datetime import datetime, timedelta
from dateutil import relativedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mockplatform.settings')
django.setup()
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

print('django-apscheduler starting')

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

def demo(name):
    # 具体要执行的代码
    print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))


scheduler.add_job(demo, "interval", seconds=10, args=['arg1'], id="demo", replace_existing=True)

# 监控任务
register_events(scheduler)
# 调度器开始运行
scheduler.start()

while True:
    pass
