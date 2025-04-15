#### DOCKER
docker run --name kgnginx  -p 5000:5000 -p 8000:8000 -p 9999:9999 -p 11434:11434  -v /etc/nginx/nginx.conf:/etc/nginx/nginx.conf  -v /root/works:/root/works -d nginx



##### 清理缓存
Docker 使用 overlay2 存储驱动程序来管理容器和镜像的存储。随着时间的推移，可能会积累一些未使用的层和资源，这会导致磁盘空间不足。以下是一些步骤来清理 Docker overlay2 存储驱动程序中的未使用数据：

删除停止的容器：
    
    docker container prune

删除未使用的镜像：

    docker image prune

如果你想要删除所有未标记的镜像，可以使用 -a 选项：
    
    docker image prune -a

删除未使用的网络：

    docker network prune

删除未使用的卷：
    
    docker volume prune

删除所有未使用的资源： 如果你想要一次性删除所有未使用的容器、网络、卷和镜像（不使用 -a 选项），可以使用以下命令：

    docker system prune

如果你想要删除所有未使用的资源，包括那些未被任何容器引用的镜像，可以使用 -a 选项：
    
    docker system prune -a

清理 Docker 的构建缓存： 如果你经常构建 Docker 镜像，可能会积累大量的构建缓存。可以使用以下命令来清理：
    
    docker builder prune


### 启动服务
    
     systemctl status docker.service

### 打包镜像

    docker-compose up --build -d
    

### 最后需要进入进行执行celery队列任务


    nohup celery flower -A yunheKGPro --address=127.0.0.1 --port=5555 > flower.log  2>&1 &
    nohup celery -A yunheKGPro worker -l info --pool=solo > celery.log 2>&1&


# git 命令

git rm --cached '*.pyc'



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



# 值班报告
http://10.4.9.95/pub/html/oasource/fyj/fxdt_fyj/shzhfydt/index.html

http://10.4.9.95/pub/html/oasource/fyj/index.html

