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
    #llm = Ollama(model="qwen2.5:14b")
    llm = Ollama(model="deepseek-r1:14b")
    res = llm(text)
    return res

def query_expert(text):
    prompt = f"""用户问题为：{text}\n,
    根据用户问题，抽取语义中包含的参数，从给定的下述函数中自主匹配规则，返回给用户相关答案，答案简洁明了，不要出现冗余描述。如果匹配不到相关规则，则根据已有知识回答。
    相关函数定义如下\n：
    def yujingdengji(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    print("预警等级")
    "
    TODO 条件
    :param smx_sw: 三门峡水位
    :param lh_sw:  陆浑水位
    :param xld_sw: 小浪底水位
    :param gx_sw:  故县水位
    :param dph_sw: 大平湖水位
    :param hkc_sw: 河口村水位
    :param swz_ll: 石嘴山水位
    :return: 具体应对措施
    "
    smx_sw = shuiku_shuiwei.get("三门峡", ).get('level', 0)
    xld_sw = shuiku_shuiwei.get("小浪底", ).get('level', 0)
    lh_sw = shuiku_shuiwei.get("陆浑", ).get('level', 0)
    gx_sw = shuiku_shuiwei.get("故县", ).get('level', 0)
    hkc_sw = shuiku_shuiwei.get("河口村", ).get('level', 0)
    dph_sw = shuiku_shuiwei.get("东平湖", ).get('level', 0)

    knh_ll = shuiwenzhan_liuliang.get("唐乃亥", ).get('flow', 0)
    lz_ll = shuiwenzhan_liuliang.get("兰州", ).get('flow', 0)
    szs_ll = shuiwenzhan_liuliang.get("石嘴山", ).get('flow', 0)
    lm_ll = shuiwenzhan_liuliang.get("龙门", ).get('flow', 0)
    tg_ll = shuiwenzhan_liuliang.get("潼关", ).get('flow', 0)
    hx_ll = shuiwenzhan_liuliang.get("华县", ).get('flow', 0)
    hyk_ll = shuiwenzhan_liuliang.get("花园口", ).get('flow', 0)
    gc_ll = shuiwenzhan_liuliang.get("高村", ).get('flow', 0)
    wl_ll = shuiwenzhan_liuliang.get("武陟", ).get('flow', 0)
    act_flag, lev = None, None#huangwei_yujing_rec()
    print(act_flag, lev)
    if (act_flag and lev == 'Ⅰ') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or xld_sw >= 275 or smx_sw >= 335 or knh_ll >= 5000 or lz_ll >= 6500 or szs_ll >= 5500 or lm_ll >= 18000 or tg_ll >= 15000 or hyk_ll >= 15000 or hx_ll >= 8000 or wl_ll >= 4000:
        print("# 启动防汛一级应急响应")
        return "按照《黄河防汛抗旱应急预案》，启动一级应急响应，响应行动如下：（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛一级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导，动员社会力量支援黄河抗洪抢险救灾。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作，各职能组充实人员。黄委全体职工全力投入抗洪抢险工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 3 次，每日至少提供12 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖、北金堤滞洪区运用的分析研判；宣传组适时举行新闻发布会，向社会报道黄河抗洪抢险动态，做好新闻宣传工作。（4）黄河防总根据汛情需要，及时增派司局级领导带队的工作组、专家组赶赴现场，指导抗洪抢险救灾工作。（5）根据各地抗洪抢险需要，黄河防总按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险，必要时请求国家防总调动流域内外抢险队、物资支援黄河抗洪抢险。（6）有关省区防汛抗旱指挥机构的主要负责同志主持会商，动员部署防汛工作；按照权限组织调度水工程；根据预案转移安置危险地区群众，组织强化巡堤查险和堤防防守，及时控制险情；增派工作组、专家组赴一线指导防汛工作；受灾地区的各级防汛抗旱指挥机构负责人、成员单位负责人，应按照职责到分管的区域组织指挥防汛工作，或驻点具体帮助重灾区做好防汛工作；可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险；将工作情况上报省区人民政府及黄河防总。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期，动员一切社会力量投入黄河抗洪抢险"
    if (act_flag and lev == 'Ⅱ') or lh_sw >= 327.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 - 0.5 or gx_sw >= 547.39 or xld_sw >= 274 or smx_sw >= 335 or knh_ll >= 4000 or lz_ll >= 5000 or szs_ll >= 4000 or lm_ll >= 12000 or tg_ll >= 10000 or hyk_ll >= 8000 or hx_ll >= 6000 or wl_ll >= 3000:
        print("# 启动防汛二级应急响应")
        return "按照《黄河防汛抗旱应急预案》，启动二级应急响应，响应行动如下：（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛二级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。黄委全体职工做好随时投入抗洪抢险工作的准备。（4）黄河防总实时掌握雨情、水情、汛情（凌情）、工情、险情、灾情动态。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 2 次，每日至少提供 6 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖滞洪区运用的分析研判；宣传组定期举行新闻发布会，向社会公布黄河抗洪抢险动态。（5）黄河防总办公室根据汛情需要，及时派出司局级领导带队的工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（7）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府主要负责同志、国家防总及黄河防总。按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期。"
    if (act_flag and lev == 'Ⅲ') or lh_sw >= 319.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 3000 or lz_ll >= 4000 or szs_ll >= 3000 or lm_ll >= 8000 or tg_ll >= 8000 or hyk_ll >= 6000 or hx_ll >= 4000 or wl_ll >= 2000:
        # 启动防汛三级应急响应
        print("# 启动防汛三级应急响应")
        return "按照《黄河防汛抗旱应急预案》，启动三级应急响应，响应行动如下：（1）黄河防总秘书长主持防汛会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛三级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥、常务副总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 1 次，每日至少提供 3 次（8 时、14 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度；宣传组加强黄河抗洪抢险宣传。（4）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。黄委防汛物资、黄河机动抢险队支援抗洪抢险。（5）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府分管负责同志和黄河防总。可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。在省级主要媒体及新媒体平台发布防汛抗旱有关情况。"
    if (act_flag and lev == 'IV') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 2500 or lz_ll >= 2500 or szs_ll >= 2000 or lm_ll >= 5000 or tg_ll >= 5000 or hyk_ll >= 4000 or hx_ll >= 2500 or wl_ll >= 1000:
        # 启动防汛四级应急响应
        print("# 启动防汛四级应急响应")
        return "按照《黄河防汛抗旱应急预案》，启动四级应急响应，响应行动如下：（1）黄河防总秘书长主持会商，研究部署抗洪抢险工作，确定运行机制。响应期间，根据汛情发展变化，受黄河防总秘书长委托，可由黄河防总办公室副主任主持会商，并将情况报黄河防总秘书长。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛四级应急响应的命令及黄河汛情，对防汛工作提出要求，并向国家防办、水利部报告有关情况，必要时向黄河防总总指挥、常务副总指挥报告。（3）黄河防总办公室成员单位人员坚守工作岗位，加强防汛值班值守。按照黄委防御大洪水职责分工和机构设置，综合调度、水情测报和工情险情组等人员上岗到位。其余成员单位按照各自职责做好技术支撑、通信保障、后勤及交通保障，加强宣传报道。水情测报组及时分析天气形势并结合雨水情发展态势，做好雨情、水情、沙情的预测预报，加强与水利部信息中心、黄河流域气象中心、省区气象水文部门会商研判，每日至少制作发布气象水情预报 1 次，每日至少提供 2 次（8 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报。（4）黄委按照批准的洪水调度方案，结合当前汛情做好水库等水工程调度，监督指导地方水行政主管部门按照调度权限做好水工程调度。（5）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；按照预案做好辖区内巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，必要时请调解放军和武警部队、民兵参加重要堤段、重点工程的防守或突击抢险；派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府和黄河防总办公室。"
    print("预警等级: 按照《黄河防汛抗旱应急预案》，当前无预警")
    return "按照《黄河防汛抗旱应急预案》，当前无预警"
    """
    llm = Ollama(model="deepseek-r1:7b")
    res = llm(prompt)
    return res
# res = query_expert("陆浑水位为335m,应当如何处置？")
# print(res)
import requests


import requests

def run_workflow(api_key, user, query, url='http://192.168.8.2:80/v1/workflows/run'):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        "inputs": {"query": query},
        "response_mode": "blocking",
        "user": user
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 如果请求失败，抛出异常
        return response.json()  # 返回 JSON 格式的响应
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
def smx_sk(smx_sw: int = None, hyk_liuliang: int = None):
    smx_sw = smx_sw if smx_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    print("三门峡SK", hyk_liuliang, smx_sw)
    """
    三门峡
    :return:
    """
    result = "适时控制运用"
    if hyk_liuliang <= 4500:
        result = "视潼关站来水来沙情况，原则上按敞泄运用"
    elif hyk_liuliang <= 8000:
        result = "视潼关站来水来沙情况，原则上按敞泄运用"
    elif hyk_liuliang <= 10000:
        result = "视潼关站来水来沙情况，原则上按敞泄运用"
    elif hyk_liuliang <= 22000:
        result = "原则上敞泄运用，视水库蓄水及来水情况适时控泄"

    return {"result": result}

# import pandas as pd
# df = pd.read_excel('media/ddfa/1-20.xlsx')
# df2markdown = df.to_markdown()
# def smx_skyyfs(df2markdown):
#     skyyfs = (
#         "1. 花园口流量 < 4500m³/s：三门峡水库调用方式为：视潼关站来水来沙情况，原则上按敞泄运用。\n"
#         "2. 4500m³/s ≤ 花园口流量 < 8000m³/s：三门峡水库调用方式为：视潼关站来水来沙情况，原则上按敞泄运用。\n"
#         "3. 8000m³/s ≤ 花园口流量 < 10000m³/s：三门峡水库调用方式为：视潼关站来水来沙情况，原则上按敞泄运用。\n"
#         "4. 10000m³/s ≤ 花园口流量 < 22000m³/s：三门峡水库调用方式为：三门峡水库原则上敞泄运用，视水库蓄水及来水情况适时控泄。"
#     )
#     smx_shuiku = (
#         "三门峡水库7月4日8时按1000m³/s泄放，之后视情况实时调整下泄流量，7月10日前降至汛限水位305m以下后进出库平衡运用。"
#     )
#     prompt = (
#         f"根据以下三门峡水库运用规则：\n{skyyfs}\n\n"
#         f"以及当前调度方案数据（包含三门峡、小浪底、河口村、陆浑、故县水库的水位及进出库流量，以及潼关和花园口水文站的预报流量）：\n{df2markdown}\n\n"
#         f"参考描述：{smx_shuiku}\n\n"
#         f"请根据调度方案数据，结合三门峡水库的运用规则，直接生成三门峡水库的调度方案。要求：\n"
#         f"1. 方案简洁明了，避免冗余描述。\n"
#         f"2. 结合花园口流量，明确水库的运用方式（敞泄或控泄）。\n"
#         f"3. 根据实时数据，明确下泄流量调整建议。"
#     )
#     res = query_question(prompt)
#     return res
# res = smx_skyyfs(df2markdown)
# print(res)
#print(df2markdown)


# 使用示例
# api_key = 'app-lfd1N6uy7KhJAmrXKyYn1wwn'
# user = 'Jack Li'
# query = '潼关最大流量是多少'
# response = run_workflow(api_key, user, query)
#
# print(response)
# def parse_excel(file_path):
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
#
#     # 处理表头
#     # 获取前两行作为表头信息
#     first_row = df.iloc[0, :].fillna('')  # 第一行
#     second_row = df.iloc[1, :].fillna('')  # 第二行
#
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
#
#     # 设置列名
#     df.columns = header
#     df = df.drop([0, 1, 2])  # 删除前3行
#
#     # 动态匹配列名
#     time_column = None
#     for col in header:
#         if "月.日" in col:
#             time_column = col
#             break
#     if time_column is None:
#         raise ValueError("未找到时间列")
#
#     tongguan_column = None
#     for col in header:
#         if "潼关" in col and "预报流量" in col:
#             tongguan_column = col
#             break
#     if tongguan_column is None:
#         raise ValueError("未找到潼关预报流量列")
#
#     sanmenxia_inflow = None
#     for col in header:
#         if "三门峡" in col and "入库流量" in col:
#             sanmenxia_inflow = col
#             break
#     if sanmenxia_inflow is None:
#         raise ValueError("未找到三门峡入库流量列")
#     #print(df.iloc[:,1])
#     # 解析数据
#     data = []
#     for _, row in df.iterrows():
#         time_value = row[time_column]
#         formatted_time = ""
#
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
#         print(formatted_time)  # 打印格式化后的时间
#         row_data = {
#             "时间": formatted_time,#row[time_column].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[time_column], pd.Timestamp) else str(row[time_column]),
#             "潼关": {
#                 "预报流量（m³/s）": row.iloc[1]
#             },
#             "三门峡": {
#                 "入库流量（m³/s）": row.iloc[2],
#                 "出库流量（m³/s）": row.iloc[3],
#                 "水位（m）": row.iloc[4],
#                 "蓄水量（亿m³）": row.iloc[5],
#             },
#             "小浪底": {
#                 "入库流量（m³/s）": row.iloc[6],
#                 "出库流量（m³/s）": row.iloc[7],
#                 "水位（m）": row.iloc[8],
#                 "蓄水量（亿m³）": row.iloc[9],
#             },
#             "陆浑": {
#                 "入库流量（m³/s）": row.iloc[10],
#                 "出库流量（m³/s）": row.iloc[11],
#                 "水位（m）": row.iloc[12],
#                 "蓄水量（亿m³）": row.iloc[13],
#             },
#             "故县": {
#                 "入库流量（m³/s）": row.iloc[14],
#                 "出库流量（m³/s）": row.iloc[15],
#                 "水位（m）": row.iloc[16],
#                 "蓄水量（亿m³）": row.iloc[17],
#             },
#             "河口村": {
#                 "入库流量（m³/s）": row.iloc[18],
#                 "出库流量（m³/s）": row.iloc[19],
#                 "水位（m）": row.iloc[20],
#                 "蓄水量（亿m³）": row.iloc[21],
#             },
#             "花园口": {
#                 "流量（m³/s）": row.iloc[22],
#             },
#         }
#         data.append(row_data)
#
#     return data
# # 示例调用
# file_path = "media/ddfa/2024-12-23.xlsx"  # 替换为你的 Excel 文件路径
# data = parse_excel(file_path)
# print("type(data):",type(data))
# default_context =("小浪底和西霞院水库联合调度，6月25日8时起按控制花园口水文站4400m3/s泄放，26日8时起按4000m3/s泄放，之后视情况实时调整下泄流量，7月8日前库水位降至汛限水位235m以下，结束应急抗旱调度过程。\n"
#                   "三门峡水库6月25日20时起继续按600m3/s下泄，之后视情况实时调整下泄流量，7月10日前库水位降至汛限水位305m以下，而后进出库平衡运用。")
# prompt = (f"参考描述：{default_context}"
#           "依据参考描述，请根据以下数据,撰写三门峡、小浪底、陆浑、故县、河口村数据的运用方式。"
#           f"数据为：{data}")      #百度API不支持数据接入，超出其最长输序列
# res = query_question(prompt)
# print(res)

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
#
# import webbrowser
#
# def open_baidu():
#     url = 'https://www.baidu.com'
#     webbrowser.open(url)
#
# open_baidu()
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os


def create_watermark(text):
    # 注册中文字体
    try:
        # 先尝试注册宋体
        font_paths = [
            "C:/Windows/Fonts/simsun.ttc",  # Windows 常见路径
            "C:/Windows/Fonts/simsun.ttf",
            "C:/Windows/Fonts/SimSun.ttc",
            "/System/Library/Fonts/STSong.ttc",  # macOS 常见路径
            "/usr/share/fonts/chinese/simsun.ttc",  # Linux 常见路径
            "./SimSun.ttc",  # 当前目录
        ]

        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('SimSun', font_path))
                    font_loaded = True
                    break
                except:
                    continue

        if not font_loaded:
            # 如果上述字体都无法加载，尝试使用内置的字体
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            font_name = 'STSong-Light'
        else:
            font_name = 'SimSun'

    except Exception as e:
        print(f"字体注册错误: {str(e)}")
        # 使用默认字体
        font_name = 'Helvetica'

    # 创建水印
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    # 设置字体和大小
    c.setFont(font_name, 30)

    # 设置透明度
    c.setFillColorRGB(1, 0, 0, alpha=0.6)

    # 获取页面尺寸
    width, height = A4

    # 在多个位置重复绘制水印以覆盖整个页面
    for y in range(0, int(height), 120):
        for x in range(0, int(width), 320):
            c.saveState()
            c.translate(x, y)
            c.rotate(45)
            # 使用中文编码确保正确显示
            c.drawString(0, 0, text.encode('utf-8').decode('utf-8'))
            c.restoreState()

    c.save()
    packet.seek(0)
    return PdfReader(packet)


def add_watermark(input_pdf, output_pdf, watermark_reader):
    try:
        with open(input_pdf, "rb") as file:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()

            # 处理每一页
            for page in pdf_reader.pages:
                # 合并水印
                page.merge_page(watermark_reader.pages[0])
                pdf_writer.add_page(page)

            # 写入新文件
            with open(output_pdf, "wb") as output_file:
                pdf_writer.write(output_file)

            return True
    except Exception as e:
        print(f"添加水印时发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    # 输入参数
    input_pdf = "media/plans/黄河汛情及水库调度方案单.pdf"  # 输入PDF文件路径
    output_pdf = "media/plans/黄河汛情及水库调度方案单_new.pdf"  # 输出PDF文件路径
    watermark_text = "小浪底水利枢纽"  # 水印文本

    try:
        # 创建水印
        watermark_reader = create_watermark(watermark_text)

        # 添加水印
        if add_watermark(input_pdf, output_pdf, watermark_reader):
            print("水印添加成功！")
        else:
            print("水印添加失败！")

    except Exception as e:
        print(f"程序执行出错: {str(e)}")