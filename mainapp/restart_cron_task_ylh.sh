#!/bin/bash

# 脚本名称: restart_cron_task.sh
# 功能: 重启 cron_task_ylh.py 进程

# 查找已有的 cron_task_ylh.py 进程
PID=$(ps -ef | grep "python3 cron_task_ylh.py" | grep -v grep | awk '{print $2}')

if [ -n "$PID" ]; then
    echo "Found existing cron_task_ylh.py process with PID $PID, killing it..."
    kill -9 $PID
    sleep 1  # 等待进程完全终止
else
    echo "No existing cron_task_ylh.py process found."
fi

# 启动新的进程
echo "Starting new cron_task_ylh.py process..."
nohup python3 cron_task_ylh.py > cron_task.log 2>&1 &

# 显示新进程信息
NEW_PID=$!
echo "New cron_task_ylh.py process started with PID $NEW_PID"