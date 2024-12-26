# 使用官方 Python 镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 暴露端口
EXPOSE 8000

# 运行 Django 开发服务器
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
