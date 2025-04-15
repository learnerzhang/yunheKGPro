#! /bin/shell
# 杀死进程
# set -x

cmd="$1"
appName='celery'
source /root/anaconda3/bin/activate env

if [ "$cmd" = "stop" ]; then
    ps -ef|grep ${appName} |grep -v grep|cut -c 9-16| xargs kill -9
    sleep 2
    if [ $? == 0 ];then
        echo "kill ${appName} success..."
    else
        echo "kill ${appName} fail"
    fi
fi 

if [ "$cmd" = "start" ]; then

    var=$(ps -ef | grep celery | grep -v grep | wc -l)
    if [ 0 != $var ]; then
        echo "${appName} service has exist"
    else
        nohup celery flower -A yunheKGPro --address=127.0.0.1 --port=5555 > flower.log  2>&1 &
        nohup celery -A yunheKGPro worker -l info --pool=solo > celery.log 2>&1&

        if [ $? == 0 ];then
            echo "${appName} service start success"
        else
            echo "${appName} service start fail"
        fi
    fi 
fi 

if [ "$cmd" = "restart" ]; then
    appName='celery'
    ps -ef|grep ${appName} |grep -v grep|cut -c 9-16| xargs kill -9
    sleep 2
    if [ $? == 0 ];then
        echo "kill ${appName} success..."
    else
        echo "kill ${appName} fail"
    fi
    
    echo "start ${appName}..."
    nohup celery flower -A yunheKGPro --address=127.0.0.1 --port=5555 > flower.log  2>&1 &
    nohup celery -A yunheKGPro worker -l info --pool=solo > celery.log 2>&1&

    if [ $? == 0 ];then
        echo "${appName} service start success"
    else
        echo "${appName} service start fail"
    fi
fi 

if [ "$cmd" = "status" ]; then
    var=$(ps -ef | grep celery | grep -v grep | wc -l)
    echo "the ${var} celery running"
fi 

if [ "$cmd" = "kgstart" ]; then
    appName='8080'

    var=$(ps -ef | grep ${appName} | grep -v grep | wc -l)
    if [ 0 != $var ]; then
        ps -ef|grep ${appName} |grep -v grep|cut -c 9-16| xargs kill -9
        sleep 2
        if [ $? == 0 ];then
            echo "kill ${appName} success..."
        else
            echo "kill ${appName} fail"
        fi
    fi 
    echo "start ${appName}..."
    nohup python manage.py runserver 0.0.0.0:8080 > run.log  2>&1 &
    if [ $? == 0 ];then
        echo "${appName} service start success"
    else
        echo "${appName} service start fail"
    fi
fi 