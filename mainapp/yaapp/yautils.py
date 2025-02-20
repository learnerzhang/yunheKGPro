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


idx_list = ['水位', '入库', '出库', '蓄量', "流量"]
sknames = { '三门峡', '小浪底',  '陆浑', '故县', '河口村', '西霞院', '万家寨', '龙口'}
swznames = { '花园口', '小花间'}
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
        print(f"Error processing complex header: {str(e)}")
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
        # print(file, "JSON 数据：\n", json_data)
        print("JSON 数据：\n", ddfa_file_path)
        skMapData = collections.defaultdict(dict)
        swMapData = collections.defaultdict(list)
        date_list = []
        for record in json.loads(json_data):
            record_keys = list(record.keys())
            new_record_keys = [ "".join(k.split("_")[:2]) for k in record_keys]
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
        
        return skMapData, swMapData, date_list
    except Exception as e:
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
        # print(file, "JSON 数据：\n", json_data)
        # print("JSON 数据：\n", ddfa_file_path)
        # print("="*100)
        # print(json_data)
        skMapData = collections.defaultdict(dict)
        swMapData = collections.defaultdict(list)
        date_list = []
        for record in json.loads(json_data):
            record_keys = list(record.keys())
            new_record_keys = [ "".join(k.split("_")[:2]) for k in record_keys]
            # print(record_keys)
            # print(new_record_keys)
            print(len(record_keys), len(new_record_keys))
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
        
        print(date_list)
        pprint.pprint(swMapData)       
        print("开始绘图")
        if myDate is None:
            myDate = str(date.today())

        htmls_dir = os.path.join("data", "ddfaouts", str(business_type), myDate, "html")
        imgs_dir = os.path.join("data", "ddfaouts", str(business_type), myDate, "imgs")
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
        if sys.platform.startswith('win'):
            path_wkimg = r'D:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe'  # 工具路径
        else:
            path_wkimg = r'/usr/bin/wkhtmltoimage'

        cfg = imgkit.config(wkhtmltoimage=path_wkimg)
        options = {
            'load-error-handling': 'ignore',
            'javascript-delay': 1100,  # 延迟 1000 毫秒，根据需要调整
        }
        
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
        print("开始绘制小浪底调度过程曲线", list(skMapData.keys()))
        for sk in sknames:
            if sk not in skMapData:
                continue
            record_data = skMapData[sk]
            html_filepath = os.path.join(htmls_dir, f"{sk}.html")
            image_filepath = os.path.join(imgs_dir, f"{sk}.png")
            
            # 创建折线图
            line = Line(init_opts=opts.InitOpts(theme='white'))
            line.add_xaxis(xaxis_data=date_list)

            print("data key:", list(record_data.keys()))
            if '水位' in record_data:
                # 添加 Y 轴数据（温度）
                swdatas = record_data['水位']
                print("水位:", len(swdatas))
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
                print("出库:", len(outflowdatas))
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
                    min_=min(swdatas)-10,
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

        print("绘图完成")
        # 创建临时文件夹
    except Exception as e:
        print(e)
        print(f"Error plotting and saving HTML: {str(e)}")
        return f"Error plotting and saving HTML: {str(e)}"

if __name__ == "__main__":

    # for file in os.listdir("data/ddfa"):
    #     file_path = f"data/ddfa/{file}"
    #     # df = pd.read_excel(file_path, sheet_name='Sheet1')
    #     # print(df.head(10))
    #     plot_save_html(file_path,)
    #     break
    
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

    # for file in files:
    #     file_path = f"data/shj_ddfad/{file}"
    #     plot_save_html(file_path, 3)
    #     break



    # r = excel_to_dict("data/shj_ddfad/调度方案单13.xlsx")
    # print(r)
    pass