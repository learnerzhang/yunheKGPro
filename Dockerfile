# 使用官方 Python 镜像
FROM python:3.10

# 安装依赖（增加 procps 包用于调试）
RUN apt-get update && apt-get install -y --no-install-recommends curl procps \
    && rm -rf /var/lib/apt/lists/*

# 复制脚本到标准路径并设置权限
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh  # 强制设置权限

# 复制项目代码
COPY . /app
WORKDIR /app

# 安装 Python 依赖
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 修复 django.utils.six 缺失问题（如果仍需）
COPY ./libs/six.py /usr/local/lib/python3.10/site-packages/django/utils/

EXPOSE 8000

# 启动命令（保持原样）
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]