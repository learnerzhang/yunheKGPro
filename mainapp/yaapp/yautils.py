import collections
from datetime import date
import os
import pprint
import sys
import ollama
import pandas as pd
import requests
import imgkit
import json
from collections import defaultdict
from pyecharts.charts import Line
from pyecharts import options as opts
from yunheKGPro import settings
#import rule
from . import rule
#from yaapp import rule
import logging
logger = logging.getLogger('kgproj')

idx_list = ['水位', '入库', '出库', '蓄量', "流量"]
sknames = { '三门峡', '小浪底',  '陆浑', '故县', '河口村', '西霞院', '万家寨', '龙口'}
swznames = { '花园口', '小花间', "潼关", "古贤坝址","白马寺"}
othnames = { '24h水位', '古贤坝址'}


def process_complex_header(file_path):
    """
    处理复杂表头的 Excel 表格，将多行表头合并为单行表头，并按照指定格式处理
    
    参数:
        file_path (str): Excel 文件路径
        
    返回:
        DataFrame: 处理后的 DataFrame
    """
    try:
        # 读取 Excel 文件，不指定表头
        df = pd.read_excel(file_path, header=None)
        # 获取表头信息
        header_data = []
        cur = 0
        for i in range(len(df)):
            row = df.iloc[i, :]
            if not row.isnull().any():
                """如果当前行没有空值，跳出循环"""
                break
            cur += 1

            if i == 0:
                preValue = None
                for col in row:
                    if pd.isna(col):
                        header_data.append(preValue)
                    else:
                        preValue = col
                        header_data.append(col)
            else:
                for ii, col in enumerate(row):
                    if pd.isna(col):
                        continue
                    else:
                        header_data[ii] = f"{header_data[ii]}_{col}"
                pass

        # 检查表头行数是否合理
        if len(header_data) == 0:
            raise ValueError("未找到有效的表头行")
        
        
        # df.columns = header_data
        data_df = df.iloc[cur:]
        data_df.columns = header_data
        data_df.iloc[:, 0] = pd.to_datetime(data_df.iloc[:, 0]).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        # data_df.iloc[:, 0] = pd.to_datetime(data_df.iloc[:, 0], unit='s').apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        # data_df[:, 0] = pd.to_datetime(data_df['时间']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        return data_df
        
    except Exception as e:
        logger.error(f"Error processing complex header: {str(e)}")
        return pd.DataFrame()  # 返回空的 DataFrame 而不是错误信息字符串

def excel_to_json(file_path):
    """
    将 Excel 文件内容转换为 JSON 格式
    
    参数:
        file_path (str): Excel 文件路径
        
    返回:
        str: JSON 格式的字符串
    """
    try:
        # 处理复杂表头
        df = process_complex_header(file_path)
        
        # 如果 DataFrame 为空，返回空 JSON
        if df.empty:
            return json.dumps([])
        # 将 DataFrame 转换为 JSON
        json_data = df.to_json(orient='records', force_ascii=False, indent=4)
        return json_data
        
    except Exception as e:
        return f"Error converting Excel to JSON: {str(e)}"


def excel_to_dict(ddfa_file_path):
    try:
        json_data = excel_to_json(ddfa_file_path)
        skMapData = collections.defaultdict(dict)
        swMapData = collections.defaultdict(list)
        date_list = []

        for record in json.loads(json_data):
            record_keys = list(record.keys())

            # Collect date first
            if '时间' in record_keys:
                date_list.append(record['时间'])
            elif '月.日' in record_keys:
                date_list.append(record['月.日'])

            # Then collect other data
            for skname in sknames:
                for idx in idx_list:
                    for key in record_keys:
                        if skname in key and idx in key:
                            if idx not in skMapData[skname]:
                                skMapData[skname][idx] = []
                            skMapData[skname][idx].append(record[key])

            for swname in swznames:
                for key in record_keys:
                    if swname in key:
                        swMapData[swname].append(record[key])

        return skMapData, swMapData, date_list
    except Exception as e:
        print(f"Error in excel_to_dict: {str(e)}")
        return None, None, None


def excel_to_dict_v2(ddfa_file_path):
    """
    改进版Excel数据转换函数，确保每个数据点绑定对应时间戳

    参数:
        ddfa_file_path (str): Excel文件路径

    返回:
        tuple: (skMapData, swMapData, date_list)
        - skMapData: 水库数据字典，结构为 {水库名: {指标: [带时间戳的数据]}}
        - swMapData: 水文站数据字典，结构为 {站点名: [带时间戳的数据]}
        - date_list: 时间序列列表
    """
    try:
        json_data = excel_to_json(ddfa_file_path)
        skMapData = collections.defaultdict(dict)
        swMapData = collections.defaultdict(list)
        date_list = []

        records = json.loads(json_data)
        for i, record in enumerate(records):
            record_keys = list(record.keys())

            # 处理时间字段
            current_time = None
            if '时间' in record_keys:
                current_time = record['时间']
            elif '月.日' in record_keys:
                current_time = record['月.日']

            if current_time:
                date_list.append(current_time)

                # 处理水库数据（带时间戳）
                for skname in sknames:
                    for idx in idx_list:
                        for key in record_keys:
                            if skname in key and idx in key:
                                if idx not in skMapData[skname]:
                                    skMapData[skname][idx] = []
                                # 存储为 (值, 时间戳) 元组
                                skMapData[skname][idx].append((record[key], current_time))

            # 处理水文站数据（带时间戳）
            for swname in swznames:
                for key in record_keys:
                    if swname in key and current_time:
                        swMapData[swname].append((record[key], current_time))

        return skMapData, swMapData, date_list

    except Exception as e:
        logger.error(f"Error in excel_to_dict_v2: {str(e)}")
        return None

def plot_save_html(ddfa_file_path, business_type=0, myDate=None):
    """
    将数据绘制成 HTML 文件并保存
    
    参数:
        data_df (DataFrame): 包含数据的 DataFrame
        
    返回:
        str: HTML 文件路径
    """
    
    try:
        json_data = excel_to_json(ddfa_file_path)
        print("JSON 数据：\n", ddfa_file_path)
        # print(file, "JSON 数据：\n", json_data)
        # print("JSON 数据：\n", ddfa_file_path)
        # print("="*100)
        # print(json_data)
        skMapData = collections.defaultdict(dict)
        swMapData = collections.defaultdict(list)
        date_list = []
        for record in json.loads(json_data):
            record_keys = list(record.keys())
            # print("record_keys:", record_keys)
            new_record_keys = ["".join(k.split("_")[:2]) for k in record_keys]
            # print(new_record_keys)
            # print(len(record_keys), len(new_record_keys))

            # idx_list = ['水位', '入库', '出库', '蓄量', "流量"]
            # sknames = { '三门峡', '小浪底',  '陆浑', '故县', '河口村', '西霞院', '万家寨', '龙口'}
            # swznames = { '花园口', '小花间', "潼关"}
            # othnames = { '24h水位', '古贤坝址'}
            for skname in sknames:
                for idx in idx_list:
                    for key in record_keys:
                        if skname in key and idx in key:
                            # print(skname, idx)
                            if idx not in skMapData[skname]:
                                skMapData[skname][idx] = [record[key]]
                            skMapData[skname][idx].append(record[key])
            for swname in swznames:
                for key in record_keys:
                    if swname in key:
                        swMapData[swname].append(record[key])
            
            if '时间' in record_keys:
                date_list.append(record['时间'])
            elif '月.日' in record_keys:
                date_list.append(record['月.日'])
        
        # pprint.pprint(swMapData)       
        logger.debug("开始绘图")
        if myDate is None:
            myDate = str(date.today())

        htmls_dir = os.path.join("data", "yuan_data" ,str(business_type), "ddfadouts",  myDate, "html")
        imgs_dir = os.path.join("data", "yuan_data", str(business_type), "ddfadouts", myDate, "imgs")
        if not os.path.exists(htmls_dir):
            os.makedirs(htmls_dir)
        if not os.path.exists(imgs_dir):
            os.makedirs(imgs_dir)
        # 准备数据
        mark_point = opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        )

        cfg = imgkit.config(wkhtmltoimage=settings.WKING_PATH)
        options = {
            'load-error-handling': 'ignore',
            'javascript-delay': 1100,  # 延迟 1000 毫秒，根据需要调整
        }
        logger.warning(f"开始绘制水文站调度过程曲线{list(swMapData.keys())}")
        for sw in swznames:
            if sw not in swMapData:
                continue
            lldata = swMapData[sw]
            # print(sw, lldata)
            html_filepath = os.path.join(htmls_dir, f"{sw}.html")
            image_filepath = os.path.join(imgs_dir, f"{sw}.png")

            # 创建折线图
            line = Line(init_opts=opts.InitOpts(theme='white'))
            # 添加 X 轴数据
            line.add_xaxis(xaxis_data=date_list)
            
            # 添加 Y 轴数据（温度）
            line.add_yaxis(
                series_name="流量(m3/s)",
                y_axis=lldata,
                label_opts=opts.LabelOpts(is_show=False),
                is_smooth=True,  # 是否平滑曲线
                markpoint_opts=mark_point
            )

            # 设置全局配置项
            title = f"{sw}调度过程曲线"
            line.set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                legend_opts=opts.LegendOpts(),
                yaxis_opts=opts.AxisOpts(
                    min_=min(lldata)-100,
                    type_="value",
                    name="流量(m3/s)",
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
            line.render(html_filepath)
            imgkit.from_file(html_filepath, image_filepath, config=cfg, options=options)
        # print("开始绘制小浪底调度过程曲线", list(skMapData.keys()))
        logger.warning(f"开始绘制水库调度过程曲线{list(skMapData.keys())}")
        for sk in sknames:
            if sk not in skMapData:
                continue
            record_data = skMapData[sk]
            html_filepath = os.path.join(htmls_dir, f"{sk}.html")
            image_filepath = os.path.join(imgs_dir, f"{sk}.png")
            
            # 创建折线图
            line = Line(init_opts=opts.InitOpts(theme='white'))
            line.add_xaxis(xaxis_data=date_list)
            logger.debug(f"data key: {list(record_data.keys())}")
            if '水位' in record_data:
                # 添加 Y 轴数据（温度）
                swdatas = record_data['水位']
                line.add_yaxis(
                    series_name="水位(m)",
                    y_axis=swdatas,
                    label_opts=opts.LabelOpts(is_show=False),
                    is_smooth=True,  # 是否平滑曲线
                    markpoint_opts=mark_point
                )

            if '入库' in record_data and '出库' in record_data:
                # 添加额外的 Y 轴（湿度）
                inflowdatas = record_data['入库']
                outflowdatas = record_data['出库']
                line.extend_axis(
                    yaxis=opts.AxisOpts(
                    min_=min([min(inflowdatas), min(outflowdatas)])-100,
                    type_="value",
                    name="流量(m3/s)",
                    position="right",
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    )
                )
            elif '入库' in record_data:
                # 添加额外的 Y 轴（湿度）
                inflowdatas = record_data['入库']
                line.extend_axis(
                    yaxis=opts.AxisOpts(
                    min_=min(inflowdatas)-100,
                    type_="value",
                    name="流量(m3/s)",
                    position="right",
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    )
                )
            elif '出库' in record_data:
                outflowdatas = record_data['出库']
                line.extend_axis(
                    yaxis=opts.AxisOpts(
                    min_=min(outflowdatas)-100,
                    type_="value",
                    name="流量(m3/s)",
                    position="right",
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    )
                )

            if '入库' in record_data:
                # 添加 Y 轴数据（入库流量）
                inflowdatas = record_data['入库']
                line.add_yaxis(
                    series_name="入库流量(m3/s)",
                y_axis=inflowdatas,
                label_opts=opts.LabelOpts(is_show=False),
                yaxis_index=1,  # 指定该系列数据对应的是第二个 Y 轴
                is_smooth=True,  # 是否平滑曲线
                markpoint_opts=mark_point
                )

            if '出库' in record_data:
                outflowdatas = record_data['出库']
                line.add_yaxis(
                    series_name="出库流量(m3/s)",
                    y_axis=outflowdatas,
                    label_opts=opts.LabelOpts(is_show=False),
                    yaxis_index=1,
                    is_smooth=True,
                    markpoint_opts=mark_point
                )

            # 设置全局配置项
            title = f"{sk}调度过程曲线"
            swdatas = record_data['水位']
            line.set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                legend_opts=opts.LegendOpts(),
                yaxis_opts=opts.AxisOpts(
                    min_= min(swdatas)-10,
                    max_= max(swdatas)+10,
                    type_="value",
                    name="水位(m)",
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
            # 设置全局配置项
            # 渲染图表到 HTML 文件
            line.render(html_filepath)
            imgkit.from_file(html_filepath, image_filepath, config=cfg, options=options)
            # imgkit.from_url('https://httpbin.org/ip', 'ip.jpg', config=cfg) # 从url获取html，再转为图片
            # imgkit.from_string('Hello!','hello.jpg', config=cfg)  #将字符串转为图片

        logger.debug("绘图完成")
        # 创建临时文件夹
    except Exception as e:
        print(e)
        logger.error(f"Error plotting and saving HTML: {str(e)}")
        return f"Error plotting and saving HTML: {str(e)}"

def skddjy(filepath):
    r = excel_to_dict(filepath)
    skMapData, swMapData, date_list = r
    smx_ddjy =[]
    for i in range(0, len(swMapData["花园口"])):
        ddjy = rule.smx_sk(swMapData["花园口"][i])
        smx_ddjy.append(ddjy["result"])
    xld_ddjy = []
    for i in range(0, len(swMapData["花园口"])):
        # print(skMapData["小浪底"]["水位"][i])
        # print(swMapData["花园口"][i])
        # print(swMapData)
        ddjy = rule.xld_sk(skMapData["小浪底"]["水位"][i],swMapData["花园口"][i],swMapData["潼关"][i])
        xld_ddjy.append(ddjy["result"])
    lh_ddjy = []
    for i in range(0, len(swMapData["花园口"])):
        # print(skMapData["小浪底"]["水位"][i])
        # print(swMapData["花园口"][i])
        # print(swMapData)
        ddjy = rule.lh_sk(skMapData["陆浑"]["水位"][i],swMapData["花园口"][i])
        lh_ddjy.append(ddjy["result"])
    gx_ddjy = []
    for i in range(0, len(swMapData["花园口"])):
        print("len(skMapData[故县]):",len(skMapData["故县"]["水位"]))
        print(len(swMapData["花园口"]))
        # print(swMapData)
        ddjy = rule.gx_sk(skMapData["故县"]["水位"][i],swMapData["花园口"][i])
        gx_ddjy.append(ddjy["result"])
    hkc_ddjy = []
    for i in range(0, len(swMapData["花园口"])):
        # print(skMapData["小浪底"]["水位"][i])
        # print(swMapData["花园口"][i])
        # print(swMapData)
        ddjy = rule.hkc_sk(skMapData["河口村"]["水位"][i],swMapData["花园口"][i])
        hkc_ddjy.append(ddjy["result"])
    return smx_ddjy,xld_ddjy,lh_ddjy,gx_ddjy,hkc_ddjy

def skddjy_new(filepath):
    r = excel_to_dict(filepath)
    skMapData, swMapData, date_list = r

    # 定义结果字典
    results = {}

    # 获取比较短的长度
    def valid_length(data):
        return len([x for x in data if x is not None])

        # 初始化 min_length 为很大的数

        # 获取有效数据的最小长度

    def valid_length(data):
        # 仅计算存在真值的长度
        return len([x for x in data if x])

        # 初始化 min_length 为很大的数

    min_length = float('inf')

    # 检查有效数据的长度
    lengths_to_check = [
        date_list,
        swMapData.get("花园口", []),
        swMapData.get("潼关", [])
    ]

    # 遍历 skMapData 的水位字段
    for key in skMapData.keys():
        water_level_data = skMapData[key].get("水位", [])
        if water_level_data:  # 仅在水位数据存在时添加
            lengths_to_check.append(water_level_data)

    # 计算最小有效长度
    for data in lengths_to_check:
        current_length = valid_length(data)
        if current_length > 0:
            min_length = min(min_length, current_length)
    keys = skMapData.keys()
    logger.debug("keys:",keys)
    # 遍历 skMapData 的键
    for key in skMapData.keys():
        if key not in results:
            results[key] = []

        # 根据水库名称调用相应的调度规则
        if key == "故县" and len(skMapData[key]["水位"]) > 0:
            for i in range(min_length):
                flower_yard_data = swMapData.get("花园口", [None] * min_length)[i]
                ddjy = rule.gx_sk(skMapData["故县"]["水位"][i], flower_yard_data)
                results[key].append(ddjy["result"])

        elif key == "三门峡" and len(skMapData[key]["水位"]) > 0:
            for i in range(min_length):
                flower_yard_data = swMapData.get("花园口", [None] * min_length)[i]
                ddjy = rule.smx_sk(flower_yard_data)
                results[key].append(ddjy["result"])

        elif key == "小浪底" and len(skMapData[key]["水位"]) > 0:
            for i in range(min_length):
                flower_yard_data = swMapData.get("花园口", [None] * min_length)[i]
                if len(swMapData.get("潼关", [])) > i:
                    ddjy = rule.xld_sk(skMapData["小浪底"]["水位"][i], flower_yard_data, swMapData["潼关"][i])
                else:
                    ddjy = rule.xld_sk(skMapData["小浪底"]["水位"][i], flower_yard_data, None)
                results[key].append(ddjy["result"])

        elif key == "河口村" and len(skMapData[key]["水位"]) > 0:
            for i in range(min_length):
                flower_yard_data = swMapData.get("花园口", [None] * min_length)[i]
                ddjy = rule.hkc_sk(skMapData["河口村"]["水位"][i], flower_yard_data)
                results[key].append(ddjy["result"])

        elif key == "陆浑" and len(skMapData[key]["水位"]) > 0:
            for i in range(min_length):
                flower_yard_data = swMapData.get("花园口", [None] * min_length)[i]
                ddjy = rule.lh_sk(skMapData["陆浑"]["水位"][i], flower_yard_data)
                results[key].append(ddjy["result"])
    results = {k: v for k, v in results.items() if v}
    return results
smx_ddgz = (
    "三门峡水库调度规则：根据花园口水文站的流量（hyk_liuliang），三门峡水库的调度方案如下：\n"
            "如果花园口流量 ≤ 4500 m³/s，三门峡水库视潼关站来水来沙情况，原则上按敞泄运用。\n"
            "如果花园口流量 ≤ 8000 m³/s，三门峡水库视潼关站来水来沙情况，原则上按敞泄运用。\n"
            "如果花园口流量 ≤ 10000 m³/s，三门峡水库视潼关站来水来沙情况，原则上按敞泄运用。\n"
            "如果花园口流量 ≤ 22000 m³/s，三门峡水库原则上敞泄运用，视水库蓄水及来水情况适时控泄。"
)
xld_ddgz =(
    "小浪底水库调度规则：根据花园口水文站的流量（hyk_liuliang）和潼关站的流量（tongguan_liuliang），小浪底水库的调度方案如下：\n"
           "如果花园口流量 ≤ 4500 m³/s，小浪底水库按控制花园口流量不大于4500 m³/s的原则泄洪，西霞院水库配合泄洪排沙。\n"
           "如果花园口流量 ≤ 8000 m³/s，小浪底水库原则上按控制花园口流量4500 m³/s方式运用，若洪水主要来源于三门峡以上，视来水来沙及水库淤积情况，适时按进出库平衡方式运用，控制水库最高运用水位不超过254m。\n"
           "如果花园口流量 ≤ 10000 m³/s，且潼关流量占比大于60%，小浪底水库按进出库平衡方式运用；否则，视下游汛情，适时按控制花园口流量不大于8000 m³/s的方式运用。\n"
           "如果花园口流量 ≤ 22000 m³/s，且潼关流量占比大于60%，小浪底水库按控制花园口流量10000 m³/s方式运用；否则，若花园口流量减去潼关流量小于9000 m³/s，按控制花园口流量10000 m³/s方式运用；否则，按不大于1000 m³/s（发电流量）下泄。\n"
           "如果花园口流量 > 22000 m³/s，且潼关流量占比大于60%，若小浪底水位 < 273.5m，按控制花园口流量10000 m³/s方式运用；否则，按进出库平衡或敞泄运用。"
)
lh_ddgz = (
    "陆浑水库调度规则：根据花园口水文站的流量（hyk_liuliang）和陆浑水库的水位（lh_sw），陆浑水库的调度方案如下：\n"
    "如果花园口流量 ≤ 4500 m³/s，且陆浑水位 < 321.5m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 ≤ 8000 m³/s，且陆浑水位 < 321.5m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 ≤ 10000 m³/s，且陆浑水位 < 321.5m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 ≤ 22000 m³/s，且花园口流量 ≤ 12000 m³/s，若陆浑水位 < 321.5m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用；若花园口流量 > 12000 m³/s，且陆浑水位 < 323m，按不超过发电流量控泄；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 > 22000 m³/s，且陆浑水位 < 323m，按不超过发电流量控泄；否则，按进出库平衡或敞泄运用。"
)

gx_ddgz = (
    "故县水库调度规则：根据花园口水文站的流量（hyk_liuliang）和故县水库的水位（gx_sw），故县水库的调度方案如下：\n"
    "如果花园口流量 ≤ 4500 m³/s，且故县水位 < 542.04m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 ≤ 8000 m³/s，且故县水位 < 542.04m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 ≤ 10000 m³/s，且故县水位 < 542.04m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 ≤ 22000 m³/s，且花园口流量 ≤ 12000 m³/s，若故县水位 < 542.04m，按控制下泄流量不大于1000 m³/s方式运用；否则，按进出库平衡或敞泄运用；若花园口流量 > 12000 m³/s，且故县水位 < 546.84m，按不超过发电流量控泄；否则，按进出库平衡或敞泄运用。\n"
    "如果花园口流量 > 22000 m³/s，且故县水位 < 546.84m，按不超过发电流量控泄；否则，按进出库平衡或敞泄运用。"
)

hkc_ddgz = (
    "河口村水库调度规则：根据花园口水文站的流量（hyk_liuliang）和河口村水库的水位（hkc_sw），河口村水库的调度方案如下：\n"
    "如果花园口流量 ≤ 4500 m³/s，且河口村水位 < 254.5m，按控制武陟不大于2000 m³/s方式运用；若水位 < 285.43m，按控制武陟不大于4000 m³/s方式运用；否则，按进出库平衡方式运用。\n"
    "如果花园口流量 ≤ 8000 m³/s，且河口村水位 < 254.5m，按控制武陟不大于2000 m³/s方式运用；若水位 < 285.43m，按控制武陟不大于4000 m³/s方式运用；否则，按进出库平衡方式运用。\n"
    "如果花园口流量 ≤ 10000 m³/s，且河口村水位 < 254.5m，按控制武陟不大于2000 m³/s方式运用；若水位 < 285.43m，按控制武陟不大于4000 m³/s方式运用；否则，按进出库平衡方式运用。\n"
    "如果花园口流量 ≤ 22000 m³/s，且花园口流量 ≤ 12000 m³/s，若河口村水位 < 254.5m，按控制武陟不大于2000 m³/s方式运用；若水位 < 285.43m，按控制武陟不大于4000 m³/s方式运用；否则，按进出库平衡方式运用；\n"
    "若花园口流量 > 12000 m³/s，且河口村水位 < 254.5m，关闭所有泄流设施；若水位 < 285.43m，尽可能按控制武陟不大于4000 m³/s方式运用；否则，按进出库平衡方式运用。\n"
    "如果花园口流量 > 22000 m³/s，且河口村水位 < 254.5m，关闭所有泄流设施；若水位 < 285.43m，尽可能按控制武陟不大于4000 m³/s方式运用；否则，按进出库平衡方式运用。"
)
reference = "小浪底和西霞院水库联合调度，6月23日开始按控制花园口水文站2600m3/s泄放4个小时、3000m3/s泄放8个小时、4000m3/s泄放12个小时，24日8时下泄流量加大至4200m3/s，25日8时起按4400m3/s泄放，26日8时起按4200m3/s泄放，29日8时起按3500m3/s泄放，29日20时起按3000m3/s泄放，之后视情实时调整下泄流量，7月1日20时前库水位降至汛限水位235m，结束应急抗旱调度过程。三门峡水库6月23日8时起按1500m3/s下泄，之后视情实时调整下泄流量，7月1日前库水位降至汛限水位305m以下，而后进出库平衡运用。"
reference_sk="三门峡水库XX月XX日X时起按XXXXm3/s下泄，之后视情实时调整下泄流量，X月X日前库水位降至汛限水位XXXXm以下，而后进出库平衡运用。"
from langchain.llms import Ollama
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
    #文 心千帆模型调用
    API_KEY = "cP3fnwcnK9MzGsWGfGEPeUkP"
    SECRET_KEY = "AfeuE0n4ZY5eCYG21QqSXG6WkBGltcxM"
    # url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=[应用API Key]&client_secret=[应用Secret Key]"
    #水利法规问答模型，（微淘之后）
    # API_KEY = "7uad3xLbT4tB4vy6i74EILqL"
    # SECRET_KEY = "BxJ9oUQha5drTM5SJISnib0lDfKpATPF"
    #  水利法规知识库
    # API_KEY = "5UMcxwqv1XLBAlq2pSSdyvjq"
    # SECRET_KEY = "PwLDquDp5CcbPW9uMHD4qJPnHGUOPs6D"
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

#注意：翻墙的时候无法调用百度  api  接口
def query_question(text):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    #s = input()
    # 注意message必须是奇数条
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json'
    }

    res = requests.request("POST", url, headers=headers, data=payload).json()
    return res['result']

def query_question(text):
    llm = Ollama(model="deepseek-r1:14b")
    res = llm(text)
    return res
import pprint

if __name__ == "__main__":
    #pass
    #skddjy("../../mainapp/media/ddfa/2025-02-08.xlsx")
    # for file in os.listdir("data/ddfa"):
    #     file_path = f"data/ddfa/{file}"
    #     # df = pd.read_excel(file_path, sheet_name='Sheet1')
    #     # print(df.head(10))
    #     plot_save_html(file_path,)
    #     break
    #
    # print("="*100)
    # # # 文件列表
    # files = [
    #     "调度方案单13.xlsx",
    #     "调度方案单12.xlsx",
    #     "调度方案单11.xlsx",
    #     "调度方案单07.xlsx",
    #     "调度方案单04.xlsx",
    #     "调度方案单02.xlsx"
    # ]
    #
    # for file in files:
    #     file_path = f"data/shj_ddfad/{file}"
    #     plot_save_html(file_path, 3)
    #     break



    # r = excel_to_dict("../../mainapp/media/ddfa/3/2025-02-08.xlsx")
    # #pprint.pprint(r)
    # if r:
    #     skMapData, swMapData, date_list = r
    #     prompt = (
    #         "根据以下水库调度规则和水文数据，分析并生成三门峡水库的调度方案：\n\n"
    #         "### 水库调度规则：\n"
    #         f"{smx_ddgz}\n\n"
    #         "### 水库数据：\n"
    #         f"三门峡水库水位: {skMapData['三门峡']['水位']}\n"
    #         f"三门峡水库入库流量: {skMapData['三门峡'].get('入库流量', '数据缺失')}\n"
    #         f"三门峡水库出库流量: {skMapData['三门峡'].get('出库流量', '数据缺失')}\n\n"
    #         "### 水文站数据：\n"
    #         f"花园口流量: {swMapData['花园口']}\n"
    #         f"潼关流量: {swMapData.get('潼关', ['数据缺失'])}\n\n"
    #         "### 时间信息：\n"
    #         f"{date_list}\n\n"
    #         "### 任务要求：\n"
    #         "根据水库调度规则和数据，生成三门峡水库的调度方案，包括下泄流量和水位控制要求。\n"
    #         "### 参考格式：\n"
    #         f"{reference_sk}\n\n"
    #         "请直接生成调度方案文本，不要包含其他描述性语句。"
    #     )
    #     print("prompt:",prompt)
    #     res = query_question(prompt)
    #     print(res)
    # 记录开始时间
    r = excel_to_dict("../../mainapp/media/ddfa/3/2025-03-13.xlsx")
    # pprint.pprint(r)
    start_time = time.time()
    # 调用函数并获取结果
    res = yautils.skddjy_new("../../mainapp/media/ddfa/3/2025-03-13.xlsx")
    ddjy_list = []
    # 遍历返回的结果字典
    for key, value in res.items():
        # 处理每个水库的出流量
        ckll = process_outflow(value, date_list)
        ddjy_list.append(f"{key}水库：{ckll}")
    # 将所有水库的调度建议合并为一个字符串
    ddjy = "\n".join(ddjy_list)
    # 记录结束时间
    end_time = time.time()
    # 计算并打印执行时间
    execution_time = end_time - start_time
    print(f"执行结果：{res}")
    print(f"代码执行时间：{execution_time:.4f} 秒")