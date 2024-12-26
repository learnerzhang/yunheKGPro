# 数据表初始化
# python manage.py makemigrations
# python manage.py migrate

# 创建管理员
# python manage.py createsuperuser

# 启动服务
# python manage.py runserver 0.0.0.0:8000

# 文件服务
# python -m SimpleHTTPServer
# python -m http.server

## 异步任务
启动 redis

## 异步任务
celery flower -A yunheKGPro --address=127.0.0.1 --port=5555

## 异步任务
celery -A yunheKGPro worker -l info --pool=solo
