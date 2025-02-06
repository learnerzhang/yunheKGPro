import json
import requests

import re

import pandas as pd
import time
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
django.setup()
#导入其他 app中的函数 或者模块之前需要提前设置os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')

from yaapp.api_yuan import query_question
# 其他 Django 相关代码
# def process_outflow(data, timestamps):
#     # 记录每次第一个不同的数的索引
#     unique_indices = []
#     unique_values = []
#
#     # 找到每个不同出库流量的索引
#     for index in range(len(data)):
#         if index == 0 or data[index] != data[index - 1]:
#             unique_indices.append(index)
#             unique_values.append(data[index])
#
#     # 组织输出信息
#     output = []
#     for i in range(len(unique_indices)):
#         if i < len(unique_indices) - 1:  # 如果不是最后一个索引
#             duration = unique_indices[i + 1] - unique_indices[i]  # 当前值到下一个值的差
#         else:  # 如果是最后一个索引
#             duration = len(data) - unique_indices[i]  # 最后一个值到结束
#         # if i == 0:
#         #     duration = unique_indices[i + 1] - unique_indices[i]  # 第一个值到第二个值的差
#         # elif i < len(unique_indices) - 1:
#         #     duration = unique_indices[i + 1] - unique_indices[i]  # 当前值到下一个值的差
#         # else:
#         #     duration = len(data) - unique_indices[i]  # 最后一个值到结束
#
#         # 计算具体的小时数
#         hours = duration * 2
#         start_time = timestamps[unique_indices[i]]
#         output.append(f"{start_time}起按{unique_values[i]}m³/s泄放 {hours}个小时")
#     res = "，".join(output) + "。"
#     return res
#
# def generate_ddjy(file_path):
#     """
#     解析 Excel 表格数据。
#
#     参数:
#         file_path (str): Excel 文件路径。
#
#     返回:
#         list: 包含解析后的数据的字典列表。
#     """
#     # 读取 Excel 文件
#     df = pd.read_excel(file_path, header=None)
#     # 处理表头
#     # 获取前两行作为表头信息
#     first_row = df.iloc[0, :].fillna('')  # 第一行
#     second_row = df.iloc[1, :].fillna('')  # 第二行
#     # 合并表头信息
#     header = []
#     for i in range(len(first_row)):
#         prefix = str(first_row[i]).strip()
#         suffix = str(second_row[i]).strip()
#         if prefix and suffix:
#             header.append(f"{prefix} {suffix}")
#         elif prefix:
#             header.append(prefix)
#         else:
#             header.append(suffix)
#     # 设置列名
#     df.columns = header
#     df = df.drop([0, 1, 2])  # 删除前3行
#     # 动态匹配列名
#     time_column = None
#     for col in header:
#         if "月.日" in col:
#             time_column = col
#             break
#     if time_column is None:
#         raise ValueError("未找到时间列")
#     tongguan_column = None
#     for col in header:
#         if "潼关" in col and "预报流量" in col:
#             tongguan_column = col
#             break
#     if tongguan_column is None:
#         raise ValueError("未找到潼关预报流量列")
#     sanmenxia_inflow = None
#     for col in header:
#         if "三门峡" in col and "入库流量" in col:
#             sanmenxia_inflow = col
#             break
#     if sanmenxia_inflow is None:
#         raise ValueError("未找到三门峡入库流量列")
#     #print(df.iloc[:,1])
#     # 解析数据
#     time_stamps,smx_ckll, xld_ckll, lh_ckll,gx_ckll, hkc_ckll=[],[],[],[],[],[]
#     for _, row in df.iterrows():
#         time_value = row[time_column]
#         formatted_time = ""
#         if isinstance(time_value, pd.Timestamp):
#             formatted_time = time_value.strftime('%Y-%m-%d %H')  # 格式化为 "YYYY-MM-DD HH:MM:SS"
#         elif isinstance(time_value, str):
#             try:
#                 time_obj = pd.to_datetime(time_value)
#                 formatted_time = time_obj.strftime('%Y-%m-%d %H')  # 格式化为 "YYYY-MM-DD HH:MM:SS"
#             except ValueError:
#                 formatted_time = time_value  # 如果解析失败，保持原样
#         else:
#             formatted_time = str(time_value)  # 如果不是时间格式，转为字符串
#             if '.' in formatted_time:  # 检查是否包含毫秒
#                 formatted_time = formatted_time.split('.')[0]  # 去除毫秒部分
#             else:
#                 formatted_time = formatted_time  # 如果没有毫秒，保持
#         time_stamps.append(formatted_time)
#         smx_ckll.append(row.iloc[3])
#         xld_ckll.append(row.iloc[7])
#         lh_ckll.append(row.iloc[11])
#         gx_ckll.append(row.iloc[15])
#         hkc_ckll.append(row.iloc[19])
#     # print(time_stamps, "长度：",len(time_stamps))
#     # print(smx_ckll, "长度：",len(smx_ckll))
#     # print(xld_ckll, "长度：",len(xld_ckll))
#     # print(lh_ckll, "长度：",len(lh_ckll))
#     # print(gx_ckll, "长度：",len(gx_ckll))
#     # print(hkc_ckll, "长度：",len(hkc_ckll))
#     smx_ddjy = process_outflow(smx_ckll,time_stamps)
#     xld_ddjy = process_outflow(xld_ckll,time_stamps)
#     lh_ddjy = process_outflow(lh_ckll,time_stamps)
#     gx_ddjy = process_outflow(gx_ckll,time_stamps)
#     hkc_ddjy = process_outflow(hkc_ckll,time_stamps)
#     data = "三门峡水库："+smx_ddjy+"\n小浪底水库："+xld_ddjy+"\n陆浑水库："+lh_ddjy+"\n故县水库："+gx_ddjy+"\n河口村水库："+hkc_ddjy
#     return data
# # 示例调用
# file_path = "media/ddfa/2024-12-23.xlsx"  # 替换为你的 Excel 文件路径
# data = generate_ddjy(file_path)
# print(data)

from langchain.llms import Ollama
def query_question(text):
    llm = Ollama(model="qwen2.5:14b")
    res = llm(text)
    return res

def parse_excel(file_path):
    """
    解析 Excel 表格数据。

    参数:
        file_path (str): Excel 文件路径。

    返回:
        list: 包含解析后的数据的字典列表。
    """
    # 读取 Excel 文件
    df = pd.read_excel(file_path, header=None)

    # 处理表头
    # 获取前两行作为表头信息
    first_row = df.iloc[0, :].fillna('')  # 第一行
    second_row = df.iloc[1, :].fillna('')  # 第二行

    # 合并表头信息
    header = []
    for i in range(len(first_row)):
        prefix = str(first_row[i]).strip()
        suffix = str(second_row[i]).strip()
        if prefix and suffix:
            header.append(f"{prefix} {suffix}")
        elif prefix:
            header.append(prefix)
        else:
            header.append(suffix)

    # 设置列名
    df.columns = header
    df = df.drop([0, 1, 2])  # 删除前3行

    # 动态匹配列名
    time_column = None
    for col in header:
        if "月.日" in col:
            time_column = col
            break
    if time_column is None:
        raise ValueError("未找到时间列")

    tongguan_column = None
    for col in header:
        if "潼关" in col and "预报流量" in col:
            tongguan_column = col
            break
    if tongguan_column is None:
        raise ValueError("未找到潼关预报流量列")

    sanmenxia_inflow = None
    for col in header:
        if "三门峡" in col and "入库流量" in col:
            sanmenxia_inflow = col
            break
    if sanmenxia_inflow is None:
        raise ValueError("未找到三门峡入库流量列")
    #print(df.iloc[:,1])
    # 解析数据
    data = []
    for _, row in df.iterrows():
        time_value = row[time_column]
        formatted_time = ""

        if isinstance(time_value, pd.Timestamp):
            formatted_time = time_value.strftime('%Y-%m-%d %H')  # 格式化为 "YYYY-MM-DD HH:MM:SS"
        elif isinstance(time_value, str):
            try:
                time_obj = pd.to_datetime(time_value)
                formatted_time = time_obj.strftime('%Y-%m-%d %H')  # 格式化为 "YYYY-MM-DD HH:MM:SS"
            except ValueError:
                formatted_time = time_value  # 如果解析失败，保持原样
        else:
            formatted_time = str(time_value)  # 如果不是时间格式，转为字符串
            if '.' in formatted_time:  # 检查是否包含毫秒
                formatted_time = formatted_time.split('.')[0]  # 去除毫秒部分
            else:
                formatted_time = formatted_time  # 如果没有毫秒，保持
        print(formatted_time)  # 打印格式化后的时间
        row_data = {
            "时间": formatted_time,#row[time_column].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[time_column], pd.Timestamp) else str(row[time_column]),
            "潼关": {
                "预报流量（m³/s）": row.iloc[1]
            },
            "三门峡": {
                "入库流量（m³/s）": row.iloc[2],
                "出库流量（m³/s）": row.iloc[3],
                "水位（m）": row.iloc[4],
                "蓄水量（亿m³）": row.iloc[5],
            },
            "小浪底": {
                "入库流量（m³/s）": row.iloc[6],
                "出库流量（m³/s）": row.iloc[7],
                "水位（m）": row.iloc[8],
                "蓄水量（亿m³）": row.iloc[9],
            },
            "陆浑": {
                "入库流量（m³/s）": row.iloc[10],
                "出库流量（m³/s）": row.iloc[11],
                "水位（m）": row.iloc[12],
                "蓄水量（亿m³）": row.iloc[13],
            },
            "故县": {
                "入库流量（m³/s）": row.iloc[14],
                "出库流量（m³/s）": row.iloc[15],
                "水位（m）": row.iloc[16],
                "蓄水量（亿m³）": row.iloc[17],
            },
            "河口村": {
                "入库流量（m³/s）": row.iloc[18],
                "出库流量（m³/s）": row.iloc[19],
                "水位（m）": row.iloc[20],
                "蓄水量（亿m³）": row.iloc[21],
            },
            "花园口": {
                "流量（m³/s）": row.iloc[22],
            },
        }
        data.append(row_data)

    return data
# 示例调用
file_path = "media/ddfa/2024-12-23.xlsx"  # 替换为你的 Excel 文件路径
data = parse_excel(file_path)
print("type(data):",type(data))
default_context =("小浪底和西霞院水库联合调度，6月25日8时起按控制花园口水文站4400m3/s泄放，26日8时起按4000m3/s泄放，之后视情况实时调整下泄流量，7月8日前库水位降至汛限水位235m以下，结束应急抗旱调度过程。\n"
                  "三门峡水库6月25日20时起继续按600m3/s下泄，之后视情况实时调整下泄流量，7月10日前库水位降至汛限水位305m以下，而后进出库平衡运用。")
prompt = (f"参考描述：{default_context}"
          "依据参考描述，请根据以下数据,撰写三门峡、小浪底、陆浑、故县、河口村数据的运用方式。"
          f"数据为：{data}")      #百度API不支持数据接入，超出其最长输序列
res = query_question(prompt)
print(res)
import webbrowser

def open_baidu():
    url = 'https://www.baidu.com'
    webbrowser.open(url)

open_baidu()
#
#
# # 给定的出库流量数据
# outflow_data = [
#     1460, 1460, 1460, 1460, 1460, 1460, 1460, 1460, 1460,
#     1865, 1865, 1865, 1865, 1865, 1865,
#     1985, 1985, 1985, 1985, 1985, 1985, 1985, 1985
# ]
#
# # 给定的时间列表
# time_stamps = [
#     "2021/10/27 8:00", "2021/10/27 10:00", "2021/10/27 12:00",
#     "2021/10/27 14:00", "2021/10/27 16:00", "2021/10/27 18:00",
#     "2021/10/27 20:00", "2021/10/27 22:00", "2021/10/28 0:00",
#     "2021/10/28 2:00", "2021/10/28 4:00", "2021/10/28 6:00",
#     "2021/10/28 8:00", "2021/10/28 10:00", "2021/10/28 12:00",
#     "2021/10/28 14:00", "2021/10/28 16:00", "2021/10/28 18:00",
#     "2021/10/28 20:00", "2021/10/28 22:00", "2021/10/29 0:00",
#     "2021/10/29 2:00", "2021/10/29 4:00"
# ]
#
# # 处理数据
# results = process_outflow(outflow_data, time_stamps)
#
# # 打印结果
# final_output = "，".join(results) + "。"
# print(final_output)

# # 打印结果
# print(json.dumps(data, indent=4, ensure_ascii=False))
# def extract_shuiku_data(text):
#     """
#     从输入文本中提取水库名称和运用方式，并转换为结构化数据。
#
#     参数:
#         text (str): 输入文本。
#
#     返回:
#         list: 包含水库名称和运用方式的字典列表。
#     """
#     # 定义正则表达式提取数据
#     # pattern = re.compile(
#     #     r"([\u4e00-\u9fa5]+水库)：(.+?)\n"
#     # )
#     pattern = re.compile(
#         r"([\u4e00-\u9fa5]+水库)：(.+?)(\n|$)"
#     )
#     # 提取数据
#     matches = pattern.findall(text)
#
#     # 转换为目标格式
#     data = []
#     for match in matches:
#         reservoir_data = {
#             "水库": match[0],
#             "运用方式": match[1].strip()
#         }
#         data.append(reservoir_data)
#
#     return data
#
#
# # 示例调用
# # text = """
# # 三门峡水库：视潼关站来水来沙情况，原则上按敞泄运用
# # 小浪底水库：原则上按控制花园口站4500m³/s方式运用。若洪水主要来源于三门峡以上，视来水来沙及水库淤积情况，适时按进出库平衡方式运用。控制水库最高运用水位不超过254m。西霞院水库配合小浪底水库泄洪排沙
# # 陆浑水库：按进出库平衡或敞泄运用
# # 故县水库：按进出库平衡或敞泄运用
# # 河口村水库：按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用。
# # """
# text = "三门峡水库：按不超305m进出库平衡运用。 \n小浪底水库：继续按500m³/s控泄，库水位维持在220m附近。 \n陆浑水库：18时起按300m³/s下泄.\n故县水库：18时起按300m³/s下泄。\n河口村水库：18时起按300m³/s下泄。"
# # 调用函数
# data = extract_shuiku_data(text)
#
# # 打印结果
# print(data)



# def text_table(text):
#     """
#     从输入文本中提取黄河下游工程数据，并转换为结构化数据。
#
#     参数:
#         text (str): 输入文本。
#
#     返回:
#         list: 包含各河段及总计数据的字典列表。
#     """
#     # 定义正则表达式提取数据
#     # pattern = re.compile(
#     #     r"(\w+段)累计有(\d+)处工程(\d+)道坝出险(\d+)次，抢险用石([\d.]+)万方，耗资([\d.]+)万元"
#     # )
#     pattern = re.compile(
#         r"(\w+段)累计有(\d+)处工程(\d+)道坝出险(\d+)次，抢险用石([\d.]+)(万方|立方米)，耗资([\d.]+)万元"
#     )
#     # 提取数据
#     matches = pattern.findall(text)
#
#     # 转换为目标格式
#     data = []
#     total = {
#         "河段": "总计",
#         "工程数量": 0,
#         "出险坝数": 0,
#         "出险次数": 0,
#         "抢险用石（万方）": 0.0,
#         "耗资（万元）": 0.0
#     }
#
#     for match in matches:
#         segment_data = {
#             "河段": match[0],
#             "工程数量": int(match[1]),
#             "出险坝数": int(match[2]),
#             "出险次数": int(match[3]),
#             "抢险用石（万方）": float(match[4]),
#             "耗资（万元）": float(match[5])
#         }
#         data.append(segment_data)
#
#         # 计算总计
#         total["工程数量"] += segment_data["工程数量"]
#         total["出险坝数"] += segment_data["出险坝数"]
#         total["出险次数"] += segment_data["出险次数"]
#         total["抢险用石（万方）"] += segment_data["抢险用石（万方）"]
#         total["耗资（万元）"] += segment_data["耗资（万元）"]
#
#     # 添加总计行
#     data.append(total)
#
#     return data
#
# # 示例调用
# text = """
# 黄河下游累计有39处工程123道坝出险214次，抢险用石5.08万方，耗资1723.27万元，河南段累计有30处工程107道坝出险197次，抢险用石4.09万方，耗资1354.85万元；山东段累计有9处 工程17道坝出险18次，抢险用石0.99立方米，耗资377.81万元。
# """
#
# # 调用函数
# data = text_table(text)
#
# # 打印结果
# print(data)


# def test():
#     url = "http://192.168.2.182:8000/dataapp/datamodelsearchoradd"#"http://192.168.2.182:8000/kgapp/kgtabtaglist"#
#     response = requests.get(url,headers={'Content-Type': 'application/json'})
#     print(response.text)
#
# if __name__ == '__main__':
#     #batch_QA()
#     test()
# print("aaaaaaa")