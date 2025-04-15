import os
from datetime import datetime, timedelta
import shutil
# 原文件名
original_filename = "HHXQ_api_data_2025-03-11.json"

# 提取日期部分
date_str = original_filename.split("_")[-1].replace(".json", "")
date = datetime.strptime(date_str, "%Y-%m-%d")

# 生成近一个月的文件名
for i in range(1,30):
    new_date = date - timedelta(days=i)
    new_date_str = new_date.strftime("%Y-%m-%d")
    new_filename = f"HHXQ_api_data_{new_date_str}.json"
    shutil.copy2(original_filename, new_filename)
    # 这里只是打印新文件名，如果你想复制文件并重命名，可以使用shutil.copy2
    # 检查新文件名是否和原文件名相同
    if new_filename != original_filename:
        try:
            # 复制原文件并重命名
            shutil.copy2(original_filename, new_filename)
            print(f"成功复制文件到 {new_filename}")
        except Exception as e:
            print(f"复制文件到 {new_filename} 时出错: {e}")
    else:
        print(f"跳过复制，新文件名 {new_filename} 与原文件名相同。")