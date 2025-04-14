import pandas as pd
import datetime
from . import yautils
import os
#import yautils
import openpyxl
from datetime import datetime, timedelta
from openpyxl import load_workbook
from langchain.vectorstores import FAISS
import requests
import json

def getYuAnParamPath(ctype, mydate):
    """
        获取对应的参数路径
    """
    if ctype == 0:
        return f"data/yuan_data/0/plans/HHZXY_api_data_{mydate}.json"
    elif ctype == 1:
        return f"data/yuan_data/1/plans/XLDQX_api_data_{mydate}.json"
    elif ctype == 2:
        return f"data/yuan_data/2/plans/XLDTSTS_api_data_{mydate}.json"
    elif ctype == 3:
        return f"data/yuan_data/3/plans/HHXQ_api_data_{mydate}.json"
    elif ctype == 4:
        return f"data/yuan_data/4/plans/YLH_api_data_{mydate}.json"
    return "data/yuan_data/0/plans/HHZXY_api_data_2023-07-23.json"


def getYuAnName(ctype, mydate):
    """
    生产标准的预案名称
    """
    format_name = f"{mydate}黄河中下游防汛调度预案" 
    if ctype == 1:
        format_name = f"{mydate}小浪底秋汛防汛调度预案"
    elif ctype == 2:
        format_name = f"{mydate}小浪底调水调沙防汛调度预案"
    elif ctype == 3:
        format_name = f"{mydate}黄河汛情及水库调度方案单"
    elif ctype == 4:
        format_name = f"{mydate}伊洛河防汛预案"
    return format_name


def img2base64(imgpath):
    import base64
    with open(imgpath, 'rb') as f:
        data = f.read()
        encoded_string = base64.b64encode(data)
        return encoded_string.decode('utf-8')

def excel_to_html_with_merged_cells(file_path):
    """
    将 Excel 文件转换为 HTML 表格，保留合并单元格，并格式化数值和时间
    """
    # 加载 Excel 文件
    workbook = load_workbook(file_path)
    sheet = workbook.active

    # 创建 HTML 表格
    html_table = '<table class="dataframe">\n'

    # 遍历每一行
    for row in sheet.iter_rows():
        html_table += '<tr>\n'
        for cell in row:
            # 检查单元格是否被合并
            is_merged = False
            for merged_range in sheet.merged_cells.ranges:
                if cell.coordinate in merged_range:
                    is_merged = True
                    # 如果是合并区域的第一个单元格，设置 rowspan 和 colspan
                    if cell.coordinate == merged_range.start_cell.coordinate:
                        value = cell.value
                        if isinstance(value, (int, float)):
                            value = round(value, 2)  # 保留两位小数
                            # 添加单位并确保单位格式正确
                            cell_value = sheet.cell(row=1, column=cell.column).value
                            if cell_value is not None and "流量" in cell_value:
                                unit = "m³/s"
                            else:
                                unit = ""
                            value = f"{value} {unit}"
                        elif isinstance(value, datetime):
                            value = value.replace(microsecond=0)  # 去除微秒
                            if value.second >= 30:
                                value = (value + timedelta(minutes=1)).replace(second=0)  # 四舍五入到整点
                            else:
                                value = value.replace(second=0)  # 直接舍去秒数
                            value = value.strftime('%Y-%m-%d %H:%M')  # 格式化为年月日 时分
                        html_table += f'<th rowspan="{merged_range.size["rows"]}" colspan="{merged_range.size["columns"]}">{value}</th>\n'
                    break
            if not is_merged:
                # 普通单元格
                value = cell.value
                if isinstance(value, (int, float)):
                    value = round(value, 2)  # 保留两位小数
                    # 添加单位并确保单位格式正确
                    cell_value = sheet.cell(row=1, column=cell.column).value
                    if cell_value is not None and "流量" in cell_value:
                        unit = "m³/s"
                    else:
                        unit = ""
                    value = f"{value} {unit}"
                elif isinstance(value, datetime):
                    value = value.replace(microsecond=0)  # 去除微秒
                    if value.second >= 30:
                        value = (value + timedelta(minutes=1)).replace(second=0)  # 四舍五入到整点
                    else:
                        value = value.replace(second=0)  # 直接舍去秒数
                    value = value.strftime('%Y-%m-%d %H:%M')  # 格式化为年月日 时分
                if cell.row == 1 or cell.column == 1:
                    html_table += f'<th>{value}</th>\n'
                else:
                    html_table += f'<td>{value}</td>\n'
        html_table += '</tr>\n'
    html_table += '</table>'
    return html_table

def paraHtml(text):
    paraHtmlText = "<p>" + text +  "</p>"
    return paraHtmlText


def divHtml(text):
    paraHtmlText = "<div style='text-align: center;'>" + text +  "</div>"
    return paraHtmlText

def bold_left_align(text):
    return f"<div style='text-align: left;'><strong>{text}</strong></div>"


def pd2HtmlCSS():
    return """"""
    css = """
        <style>
            .table-container {
                width: 100%;
                margin: 20px;
                overflow-x: auto;
            }
            .dataframe {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            .dataframe thead {
                background-color: #6c7ae0 !important
                color: #000000;
            }
            .dataframe th, .dataframe td {
                padding: 12px 15px;
                text-align: left;
                border: 1px solid #ddd;
            }
            .dataframe tbody tr {
                border-bottom: 1px solid #ddd;
            }
            .dataframe tbody tr:nth-child(even) {
                background-color: #f3f3f3;
            }
            .dataframe tbody tr:hover {
                background-color: #f1f1f1;
            }
            .dataframe tbody tr:last-child {
                border-bottom: 2px solid #009879;
            }
        </style>
        """
    return css





def smx_sk(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    sw = shuiku_shuiwei.get("三门峡", {}).get('level', 0)
    hyk_liuliang = shuiwenzhan_liuliang.get("花园口",{}).get('flow', 0)
    print("三门峡SK", hyk_liuliang, sw)
    """
    三门峡
    :return:
    """
    if hyk_liuliang <= 4500:
        return "视潼关站来水来沙情况，原则上按敞泄运用"
    elif hyk_liuliang <= 8000:
        return "视潼关站来水来沙情况，原则上按敞泄运用"
    elif hyk_liuliang <= 10000:
        return "视潼关站来水来沙情况，原则上按敞泄运用"
    elif hyk_liuliang <= 22000:
        return "原则上敞泄运用，视水库蓄水及来水情况适时控泄"
    else:
        return "适时控制运用"


# def xld_sk(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
#     sw = shuiku_shuiwei.get("小浪底", {}).get('level', 0)
#     hyk_liuliang = shuiwenzhan_liuliang.get("花园口", {}).get('flow', 0)
#     tongguan_liuliang = shuiwenzhan_liuliang.get("潼关", {}).get('flow', 0)
#     rate_p = float(tongguan_liuliang) / (float(hyk_liuliang) + 0.001)
#     print("小浪底SK", hyk_liuliang,tongguan_liuliang, sw)
#     """
#     小浪底库
#     :return:
#     """
#     if hyk_liuliang <= 4500:
#         return "适时调节水沙，按控制花园口站流量不大于4500m³/s的原则泄洪。西霞院水库配合小浪底水库泄洪排沙"
#     elif hyk_liuliang <= 8000:
#         return "原则上按控制花园口站4500m³/s方式运用。若洪水主要来源于三门峡以上，视来水来沙及水库淤积情况，适时按进出库平衡方式运用。控制水库最高运用水位不超过254m。西霞院水库配合小浪底水库泄洪排沙"
#     elif hyk_liuliang <= 10000:
#         if rate_p > 0.6:
#             return "小浪底：原则上按进出库平衡方式运用。西霞院水库配合小浪底水库泄洪排沙"
#         else:
#             return "小浪底：视下游汛情，适时按控制花园口站不大于8000m³/s的方式运用。西霞院水库配合小浪底水库泄洪排沙"
#     elif hyk_liuliang <= 22000:
#         if rate_p > 0.6:
#             return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
#         else:
#             if hyk_liuliang - tongguan_liuliang < 9000:
#                 return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
#             else:
#                 return "小浪底：按不大于1000m³/s（发电流量）下泄。西霞院水库配合小浪底水库泄洪排沙"
#     else:
#         # 潼关 花园口 流量大于60%
#         if rate_p > 0.6:
#             if sw < 273.5:
#                 return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
#             else:
#                 return "小浪底：按进出库平衡或敞泄运用。西霞院水库配合小浪底水库泄洪排沙"
#         else:
#             return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"


def lh_sk(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    """
    陆浑水库
    :return:
    """
    sw = shuiku_shuiwei.get("陆浑", {}).get('level', 0)
    hyk_liuliang = shuiwenzhan_liuliang.get("花园口", {}).get('flow', 0)
    print("小浪底SK", hyk_liuliang, sw)

    if hyk_liuliang <= 4500:
        if sw < 321.5:
            return "按控制下泄流量不大于1000m³/s方式运用"
        else:
            return "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 8000:
        if sw < 321.5:
            return "按控制下泄流量不大于1000m³/s方式运用"
        else:
            return "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 10000:
        if sw < 321.5:
            return "按控制下泄流量不大于1000m³/s方式运用"
        else:
            return "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 22000:
        if hyk_liuliang <= 12000:
            if sw < 321.5:
                return "按控制下泄流量不大于1000m³/s方式运用"
            else:
                return "按进出库平衡或敞泄运用"
        else:
            if sw < 323:
                return "按不超过发电流量控泄"
            else:
                return "按进出库平衡或敞泄运用"
    else:
        if sw < 323:
            return "按不超过发电流量控泄"
        else:
            return "按进出库平衡或敞泄运用"


def gx_sk(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    """
    故县水库
    :return:
    """
    sw = shuiku_shuiwei.get("故县", {}).get('level', 0)
    hyk_liuliang = shuiwenzhan_liuliang.get("花园口", {}).get('flow', 0)
    print("故县SK", hyk_liuliang, sw)

    if hyk_liuliang <= 4500:
        if sw < 542.04:
            return "按控制下泄流量不大于1000m³/s方式运用"
        else:
            return "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 8000:
        if sw < 542.04:
            return "按控制下泄流量不大于1000m³/s方式运用"
        else:
            return "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 10000:
        if sw < 542.04:
            return "按控制下泄流量不大于1000m³/s方式运用"
        else:
            return "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 22000:
        if hyk_liuliang <= 12000:
            if sw < 542.04:
                return "按控制下泄流量不大于1000m³/s方式运用"
            else:
                return "按进出库平衡或敞泄运用"
        else:
            if sw < 546.84:
                return "按不超过发电流量控泄"
            else:
                return "按进出库平衡或敞泄运用"
    else:
        if sw < 546.84:
            return "按不超过发电流量控泄"
        else:
            return "按进出库平衡或敞泄运用"


def hkc_sk(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    """
    河口村水库
    :return:
    """
    sw = shuiku_shuiwei.get("河口村", {}).get('level', 0)
    hyk_liuliang = shuiwenzhan_liuliang.get("花园口", {}).get('flow', 0)
    print("河口村SK", hyk_liuliang, sw)
    if hyk_liuliang <= 4500:
        if sw < 254.5:
            return "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        elif sw < 285.43:
            return "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            return "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    elif hyk_liuliang <= 8000:
        if sw < 254.5:
            return "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        elif sw < 285.43:
            return "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            return "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    elif hyk_liuliang <= 10000:
        if sw < 254.5:
            return "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        elif sw < 285.43:
            return "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            return "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    elif hyk_liuliang <= 22000:
        if hyk_liuliang <= 12000:
            if sw < 254.5:
                return "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
            elif sw < 285.43:
                return "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
            else:
                return "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            if sw < 254.5:
                return "关闭所有泄流设施。张峰水库适时配合河口村水库拦洪运用"
            elif sw < 285.43:
                return "尽可能按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
            else:
                return "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    else:
        if sw < 254.5:
            return "关闭所有泄流设施。张峰水库适时配合河口村水库拦洪运用"
        elif sw < 285.43:
            return "尽可能按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            return "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
        


def get_xunqi():
    day = datetime.date.today()
    m = day.month
    if m in [7, 8]:  # 前汛期
        return 1
    if m in [9, 10]:  # 后汛期
        return 2
    return 0  # 其他其


def xld_sk(sw=300, a=0.5):
    """小浪底水库"""
    xq = get_xunqi()
    if xq == 1:
        if sw >= 281:
            return "超坝顶高程{}m".format(round(sw - 281, 2))
        elif 281 - a <= sw < 281:
            return "低于坝顶高程{}m".format(round(281 - sw, 2))
        elif 275 <= sw < 281 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 275, 2))
        elif 275 - a <= sw < 275:
            return "低于校核洪水位（防洪高水位）{}m".format(round(275 - sw, 2))
        elif 274 <= sw < 275 - a:
            return "超设计洪水位{}m".format(round(sw - 274, 2))
        elif 273.5 <= sw < 274:
            return "超历史最高水位{}m".format(round(sw - 273.5, 2))
        elif 273 - a <= sw < 273.5:
            return "低于历史最高水位{}m".format(round(273.5 - sw, 2))
        elif 235 <= sw < 273 - a:
            return "超汛限水位{}m".format(round(sw - 235, 2))
        elif 235 - a <= sw < 235:
            return "低于汛限水位{}m".format(round(235 - sw, 2))
        elif 230 <= sw < 235 - a:
            return "超死水位{}m".format(round(sw - 230, 2))
        else:
            return "低于死水位{}m".format(round(230 - sw, 2))
    elif xq == 2:
        if sw >= 281:
            return "超坝顶高程{}m".format(round(sw - 281, 2))
        elif 281 - a <= sw < 281:
            return "低于坝顶高程{}m".format(round(281 - sw, 2))
        elif 275 <= sw < 281 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 275, 2))
        elif 275 - a <= sw < 275:
            return "低于校核洪水位（防洪高水位）{}m".format(round(275 - sw, 2))
        elif 274 <= sw < 275 - a:
            return "超设计洪水位{}m".format(round(sw - 274, 2))
        elif 273.5 <= sw < 274:
            return "超历史最高水位{}m".format(round(sw - 273.5, 2))
        elif 273 - a <= sw < 273.5:
            return "低于历史最高水位{}m".format(round(273.5 - sw, 2))
        elif 248 <= sw < 273 - a:
            return "超汛限水位{}m".format(round(sw - 235, 2))
        elif 248 - a <= sw < 248:
            return "低于汛限水位{}m".format(round(235 - sw, 2))
        elif 230 <= sw < 248 - a:
            return "超死水位{}m".format(round(sw - 230, 2))
        else:
            return "低于死水位{}m".format(round(230 - sw, 2))
    return ""


def dph_sk(sw=60, a=0.5):
    """
    东平湖
    :param sw:
    :param a:
    :return:
    """
    xq = get_xunqi()
    if xq == 1:
        if sw >= 43.22:
            return "超防洪运用水位{}m".format(sw - 43.22)
        elif 43.22 - a <= sw < 43.22:
            return "低于防洪运用水位{}m".format(43.22 - sw)
        elif 40.72 <= sw < 43.22 - a:
            return "超汛限水位{}m".format(sw - 40.72)
        else:
            return "低于汛限水位{}m".format(40.72 - sw)
    elif xq == 2:
        if sw >= 43.22:
            return "超防洪运用水位{}m".format(sw - 43.22)
        elif 43.22 - a <= sw < 43.22:
            return "低于防洪运用水位{}m".format(43.22 - sw)
        elif 41.72 <= sw < 43.22 - a:
            return "超汛限水位{}m".format(sw - 41.72)
        else:
            return "低于汛限水位{}m".format(41.72 - sw)


def smx_sjt_sk(sw=410.0, a=0.5):
    """
    三门峡（史家摊）
    :param sw:
    :param a:
    :return:
    """
    if sw >= 351.65:
        return "超坝顶高程{}m".format(round(sw - 351.65, 2))
    elif 351.65 - a <= sw < 351.65:
        return "低于坝顶高程{}m".format(round(351.65 - sw, 2))
    elif 335 <= sw < 351.65 - a:
        return "超校核洪水位{}m".format(round(sw - 335, 2))
    elif 335 - a <= sw < 335:
        return "超校核洪水位{}m".format(round(335 - sw, 2))
    elif 333.65 <= sw < 335 - a:
        return "超防洪运用水位{}m".format(round(sw - 333.65, 2))
    elif 333.65 - a <= sw < 333.65:
        return "低于防洪运用水位{}m".format(round(333.65 - sw, 2))
    elif 331.23 <= sw < 333.65 - a:
        return "超历史最高水位{}m".format(round(sw - 331.23, 2))
    elif 331.23 - a <= sw < 331.23:
        return "低于历史最高水位{}m".format(round(331.23 - sw, 2))
    elif 318 <= sw < 332.58 - a:
        return "超人员紧急转移水位{}m".format(round(sw - 318, 2))
    elif 318 - a <= sw < 318:
        return "低于人员紧急转移水位{}m".format(round(318 - sw, 2))
    elif 305 <= sw < 318 - a:
        return "超汛限水位{}m".format(round(sw - 305, 2))
    else:
        return "低于汛限水位{}m".format(round(305 - sw, 2))


def hkc_sk(sw=300, a=0.5):
    """
    河口村水库
    :param sw:
    :param a:
    :return:
    """
    xq = get_xunqi()
    if xq == 1:
        if sw >= 288.5:
            return "超坝顶高程{}m".format(round(sw - 288.5, 2))
        elif 288.5 - a <= sw < 288.5:
            return "低于坝顶高程{}m".format(round(288.5 - sw, 2))
        elif 285.43 <= sw < 288.5 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 285.43, 2))
        elif 285.43 - a <= sw < 285.43:
            return "低于校核洪水位（防洪高水位）{}m".format(round(285.43 - sw, 2))
        elif 283 <= sw < 285.43 - a:
            return "超人员紧急转移水位{}m".format(round(sw - 283, 2))
        elif 283 - a <= sw < 283:
            return "低于人员紧急转移水位{}m".format(round(283 - sw, 2))
        elif 279.89 <= sw < 283 - a:
            return "超历史最高水位{}m".format(round(sw - 279.89, 2))
        elif 279.89 - a <= sw < 279.89:
            return "低于历史最高水位{}m".format(round(279.89 - sw, 2))
        elif 238 <= sw < 279.89 - a:
            return "超汛限水位{}m".format(round(sw - 238, 2))
        elif 238 - a <= sw < 238:
            return "低于汛限水位{}m".format(round(238 - sw, 2))
        elif 225 <= sw < 238 - a:
            return "超死水位{}m".format(round(sw - 225, 2))
        else:
            return "低于死水位{}m".format(round(225 - sw, 2))
    elif xq == 2:
        if sw >= 288.5:
            return "超坝顶高程{}m".format(round(sw - 288.5, 2))
        elif 288.5 - a <= sw < 288.5:
            return "低于坝顶高程{}m".format(round(288.5 - sw, 2))
        elif 285.43 <= sw < 288.5 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 285.43, 2))
        elif 285.43 - a <= sw < 285.43:
            return "低于校核洪水位（防洪高水位）{}m".format(round(285.43 - sw, 2))
        elif 283 <= sw < 285.43 - a:
            return "超人员紧急转移水位{}m".format(round(sw - 283, 2))
        elif 283 - a <= sw < 283:
            return "低于人员紧急转移水位{}m".format(round(283 - sw, 2))
        elif 279.89 <= sw < 283 - a:
            return "超历史最高水位{}m".format(round(sw - 279.89, 2))
        elif 279.89 - a <= sw < 279.89:
            return "低于历史最高水位{}m".format(round(279.89 - sw, 2))
        elif 275 <= sw < 279.89 - a:
            return "超汛限水位{}m".format(round(sw - 275, 2))
        elif 275 - a <= sw < 275:
            return "低于汛限水位{}m".format(round(275 - sw, 2))
        elif 225 <= sw < 275 - a:
            return "超死水位{}m".format(round(sw - 225, 2))
        else:
            return "低于死水位{}m".format(round(225 - sw, 2))
    return ""


def gx_sk(sw=600, a=0.5):
    """
    故县水库
    :param sw:
    :param a:
    :return:
    """
    xq = get_xunqi()
    if xq == 1:
        if sw >= 551.84:
            return "超坝顶高程{}m".format(round(sw - 551.84, 2))
        elif 551.84 - a <= sw < 551.84:
            return "低于坝顶高程{}m".format(round(551.84 - sw, 2))
        elif 549.86 <= sw < 551.48 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 549.86, 2))
        elif 549.86 - a <= sw < 549.86:
            return "低于校核洪水位（防洪高水位）{}m".format(round(549.86 - sw, 2))
        elif 547.39 <= sw < 549.86 - a:
            return "超设计洪水位{}m".format(round(sw - 547.39, 2))
        elif 547.39 - a <= sw < 547.39:
            return "低于设计洪水位{}m".format(round(547.39 - sw, 2))
        elif 546.84 <= sw < 547.39 - a:
            return "超防洪高水位（蓄洪限制水位）{}m".format(round(sw - 546.84, 2))
        elif 546.84 - a <= sw < 546.84:
            return "低于防洪高水位（蓄洪限制水位）{}m".format(round(546.84 - sw, 2))
        elif 543.04 <= sw < 546.84 - a:
            return "超移民水位{}m".format(round(sw - 543.04, 2))
        elif 543.04 - a <= sw < 543.04:
            return "低于移民水位{}m".format(round(543.04 - sw, 2))
        elif 537.75 <= sw < 543.04 - a:
            return "超历史最高水位{}m".format(round(sw - 537.75, 2))
        elif 537.75 - a <= sw < 537.75:
            return "低于历史最高水位{}m".format(round(537.75 - sw, 2))
        elif 533.64 <= sw < 537.75 - a:
            return "超征地水位{}m".format(round(sw - 533.64, 2))
        elif 533.64 - a <= sw < 533.64:
            return "低于征地水位{}m".format(round(533.64 - sw, 2))
        elif 527.3 <= sw < 533.64 - a:
            return "超汛限水位{}m".format(round(sw - 527.3, 2))
        elif 527.3 - a <= sw < 527.3:
            return "超汛限水位{}m".format(round(527.3 - sw, 2))
        elif 498.84 <= sw < 527.3 - a:
            return "超死水位{}m".format(round(sw - 498.84, 2))
        else:
            return "低于死水位{}m".format(round(498.84 - sw, 2))
    elif xq == 2:
        if sw >= 551.84:
            return "超坝顶高程{}m".format(round(sw - 551.84, 2))
        elif 551.84 - a <= sw < 551.84:
            return "低于坝顶高程{}m".format(round(551.84 - sw, 2))
        elif 549.86 <= sw < 551.48 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 549.86, 2))
        elif 549.86 - a <= sw < 549.86:
            return "低于校核洪水位（防洪高水位）{}m".format(round(549.86 - sw, 2))
        elif 547.39 <= sw < 549.86 - a:
            return "超设计洪水位{}m".format(round(sw - 547.39, 2))
        elif 547.39 - a <= sw < 547.39:
            return "低于设计洪水位{}m".format(round(547.39 - sw, 2))
        elif 546.84 <= sw < 547.39 - a:
            return "超防洪高水位（蓄洪限制水位）{}m".format(round(sw - 546.84, 2))
        elif 546.84 - a <= sw < 546.84:
            return "低于防洪高水位（蓄洪限制水位）{}m".format(round(546.84 - sw, 2))
        elif 543.04 <= sw < 546.84 - a:
            return "超移民水位{}m".format(round(sw - 543.04, 2))
        elif 543.04 - a <= sw < 543.04:
            return "低于移民水位{}m".format(round(543.04 - sw, 2))
        elif 537.75 <= sw < 543.04 - a:
            return "超历史最高水位{}m".format(round(sw - 537.75, 2))
        elif 537.75 - a <= sw < 537.75:
            return "低于历史最高水位{}m".format(round(537.75 - sw, 2))
        elif 534.3 <= sw < 537.75 - a:
            return "超汛限水位{}m".format(round(sw - 534.3, 2))
        elif 534.3 - a <= sw < 534.3:
            return "低于汛限水位{}m".format(round(534.3 - sw, 2))
        elif 533.64 <= sw < 534.3 - a:
            return "超征地水位{}m".format(round(sw - 533.64, 2))
        elif 533.64 - a <= sw < 533.64:
            return "低于征地水位{}m".format(round(533.64 - sw, 2))
        elif 498.84 <= sw < 533.64 - a:
            return "超死水位{}m".format(round(sw - 498.84, 2))
        else:
            return "低于死水位{}m".format(round(498.84 - sw, 2))
    return ""


def lhbs_sk(sw=380, a=0.5):
    """
    陆浑坝上
    :param sw:
    :param a:
    :return:
    """
    sw = round(sw, 2)
    xq = get_xunqi()
    if xq == 1:
        if sw >= 333:
            return "超坝顶高程{}m".format(round(sw - 333, 2))
        elif 333 - a <= sw < 333:
            return "低于坝顶高程{}m".format(round(333 - sw, 2))
        elif 331.8 <= sw < 333 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 331.8, 2))
        elif 331.8 - a <= sw < 331.8:
            return "低于校核洪水位（防洪高水位）{}m".format(round(331.8 - sw, 2))
        elif 327.5 <= sw < 331.8 - a:
            return "超设计洪水位{}m".format(round(sw - 327.5, 2))
        elif 327.5 - a <= sw < 327.5:
            return "低于设计洪水位{}m".format(round(327.5 - sw, 2))
        elif 325 <= sw < 327.5 - a:
            return "超移民水位{}m".format(round(sw - 325, 2))
        elif 325 - a <= sw < 325:
            return "低于移民水位{}m".format(round(325 - sw, 2))
        elif 323 <= sw < 325 - a:
            return "超蓄洪限制水位{}m".format(round(sw - 323, 2))
        elif 323 - a <= sw < 323:
            return "低于蓄洪限制水位{}m".format(round(323 - sw, 2))
        elif 320.91 <= sw < 323 - a:
            return "超历史最高水位{}m".format(round(sw - 320.91, 2))
        elif 320.91 - a <= sw < 320.91:
            return "低于历史最高水位{}m".format(round(320.91 - sw, 2))
        elif 319.5 <= sw < 320.91 - a:
            return "超征地水位{}m".format(round(sw - 319.5, 2))
        elif 319.5 - a <= sw < 319.5:
            return "低于征地水位{}m".format(round(319.5 - sw, 2))
        elif 317 <= sw < 319.5 - a:
            return "超汛限水位{}m".format(round(sw - 317, 2))
        elif 317 - a <= sw < 317:
            return "低于汛限水位{}m".format(round(317 - sw, 2))
        elif 298 <= sw < 317 - a:
            return "超死水位{}m".format(round(sw - 298, 2))
        else:
            return "低于死水位{}m".format(round(498.84 - sw, 2))
        
    elif xq == 2:
        if sw >= 333:
            return "超坝顶高程{}m".format(round(sw - 333, 2))
        elif 333 - a <= sw < 333:
            return "低于坝顶高程{}m".format(round(333 - sw, 2))
        elif 331.8 <= sw < 333 - a:
            return "超校核洪水位（防洪高水位）{}m".format(round(sw - 331.8, 2))
        elif 331.8 - a <= sw < 331.8:
            return "低于校核洪水位（防洪高水位）{}m".format(round(331.8 - sw, 2))
        elif 327.5 <= sw < 331.8 - a:
            return "超设计洪水位{}m".format(round(sw - 327.5, 2))
        elif 327.5 - a <= sw < 327.5:
            return "低于设计洪水位{}m".format(round(327.5 - sw, 2))
        elif 325 <= sw < 327.5 - a:
            return "超移民水位{}m".format(round(sw - 325, 2))
        elif 325 - a <= sw < 325:
            return "低于移民水位{}m".format(round(325 - sw, 2))
        elif 323 <= sw < 325 - a:
            return "超蓄洪限制水位{}m".format(round(sw - 323, 2))
        elif 323 - a <= sw < 323:
            return "低于蓄洪限制水位{}m".format(round(323 - sw, 2))
        elif 320.91 <= sw < 323 - a:
            return "超历史最高水位{}m".format(round(sw - 320.91, 2))
        elif 320.91 - a <= sw < 320.91:
            return "低于历史最高水位{}m".format(round(320.91 - sw, 2))
        elif 319.5 <= sw < 320.91 - a:
            return "超征地水位{}m".format(round(sw - 319.5, 2))
        elif 319.5 - a <= sw < 319.5:
            return "低于征地水位{}m".format(round(319.5 - sw, 2))
        elif 317.5 <= sw < 319.5 - a:
            return "超汛限水位{}m".format(round(sw - 317.5, 2))
        elif 317.5 - a <= sw < 317.5:
            return "低于汛限水位{}m".format(round(317.5 - sw, 2))
        elif 298 <= sw < 317.5 - a:
            return "超死水位{}m".format(round(sw - 298, 2))
        else:
            return "低于死水位{}m".format(round(498.84 - sw, 2))
    return ""


import re
def text_table(text):
    """
    从输入文本中提取黄河下游工程数据，并转换为结构化数据。

    参数:
        text (str): 输入文本。

    返回:
        list: 包含各河段及总计数据的字典列表。
    """
    # 定义正则表达式提取数据
    pattern = re.compile(
        r"(\w+段)累计有(\d+)处工程(\d+)道坝出险(\d+)次，抢险用石([\d.]+)万方，耗资([\d.]+)万元"
    )
    # 提取数据
    matches = pattern.findall(text)

    # 转换为目标格式
    data = []
    total = {
        "河段": "总计",
        "工程数量": 0,
        "出险坝数": 0,
        "出险次数": 0,
        "抢险用石（万方）": 0.0,
        "耗资（万元）": 0.0
    }

    for match in matches:
        segment_data = {
            "河段": match[0],
            "工程数量": int(match[1]),
            "出险坝数": int(match[2]),
            "出险次数": int(match[3]),
            "抢险用石（万方）": float(match[4]),
            "耗资（万元）": float(match[5])
        }
        data.append(segment_data)

        # 计算总计
        total["工程数量"] += segment_data["工程数量"]
        total["出险坝数"] += segment_data["出险坝数"]
        total["出险次数"] += segment_data["出险次数"]
        total["抢险用石（万方）"] += segment_data["抢险用石（万方）"]
        total["耗资（万元）"] += segment_data["耗资（万元）"]

    # 添加总计行
    data.append(total)

    return data

def extract_shuiku_data(text):
    """
    从输入文本中提取水库名称和运用方式，并转换为结构化数据。

    参数:
        text (str): 输入文本。

    返回:
        list: 包含水库名称和运用方式的字典列表。
    """
    # 定义正则表达式提取数据
    # pattern = re.compile(
    #     r"([\u4e00-\u9fa5]+水库)：(.+?)\n"
    # )
    pattern = re.compile(
        r"([\u4e00-\u9fa5]+水库)：(.+?)(\n|$)"
    )
    # 提取数据
    matches = pattern.findall(text)

    # 转换为目标格式
    data = []
    for match in matches:
        reservoir_data = {
            "水库": match[0],
            "调度原则": match[1].strip()
        }
        data.append(reservoir_data)

    return data


def extract_shuiku_data_jianyi(text):
    """
    从输入文本中提取水库名称和运用方式，并转换为结构化数据。

    参数:
        text (str): 输入文本。

    返回:
        list: 包含水库名称和运用方式的字典列表。
    """
    # 定义正则表达式提取数据
    # pattern = re.compile(
    #     r"([\u4e00-\u9fa5]+水库)：(.+?)\n"
    # )
    pattern = re.compile(
        r"([\u4e00-\u9fa5]+水库)：(.+?)(\n|$)"
    )
    # 提取数据
    matches = pattern.findall(text)

    # 转换为目标格式
    data = []
    for match in matches:
        reservoir_data = {
            "水库": match[0],
            "调度建议": match[1].strip()
        }
        data.append(reservoir_data)

    return data

def process_outflow(data, timestamps):
    # 记录每次第一个不同的数的索引
    unique_indices = []
    unique_values = []

    # 找到每个不同出库流量的索引
    for index in range(len(data)):
        if index == 0 or data[index] != data[index - 1]:
            unique_indices.append(index)
            unique_values.append(data[index])

    # 组织输出信息
    output = []
    for i in range(len(unique_indices)):
        if i < len(unique_indices) - 1:  # 如果不是最后一个索引
            duration = unique_indices[i + 1] - unique_indices[i]  # 当前值到下一个值的差
        else:  # 如果是最后一个索引
            duration = len(data) - unique_indices[i]  # 最后一个值到结束
        # if i == 0:
        #     duration = unique_indices[i + 1] - unique_indices[i]  # 第一个值到第二个值的差
        # elif i < len(unique_indices) - 1:
        #     duration = unique_indices[i + 1] - unique_indices[i]  # 当前值到下一个值的差
        # else:
        #     duration = len(data) - unique_indices[i]  # 最后一个值到结束

        # 计算具体的小时数
        hours = duration * 2
        start_time = timestamps[unique_indices[i]]
        if i < len(unique_indices) - 1:
            end_time = timestamps[unique_indices[i + 1]]
        else:
            end_time = timestamps[-1]  # 最后一个值的结束时间为 timestamps 的最后一个元素
        output.append(f"{start_time}起按{unique_values[i]}m³/s泄放 {hours}个小时,至{end_time}结束")
    res = "，".join(output) + "。"
    return res

def generate_ddjy_v1(file_path):
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
    time_stamps,smx_ckll, xld_ckll, lh_ckll,gx_ckll, hkc_ckll=[],[],[],[],[],[]
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
        time_stamps.append(formatted_time)
        smx_ckll.append(row.iloc[3])
        xld_ckll.append(row.iloc[7])
        lh_ckll.append(row.iloc[11])
        gx_ckll.append(row.iloc[15])
        hkc_ckll.append(row.iloc[19])
    # print(time_stamps, "长度：",len(time_stamps))
    # print(smx_ckll, "长度：",len(smx_ckll))
    # print(xld_ckll, "长度：",len(xld_ckll))
    # print(lh_ckll, "长度：",len(lh_ckll))
    # print(gx_ckll, "长度：",len(gx_ckll))
    # print(hkc_ckll, "长度：",len(hkc_ckll))
    smx_ddjy = process_outflow(smx_ckll,time_stamps)
    xld_ddjy = process_outflow(xld_ckll,time_stamps)
    lh_ddjy = process_outflow(lh_ckll,time_stamps)
    gx_ddjy = process_outflow(gx_ckll,time_stamps)
    hkc_ddjy = process_outflow(hkc_ckll,time_stamps)
    data = "三门峡水库："+smx_ddjy+"\n小浪底水库："+xld_ddjy+"\n陆浑水库："+lh_ddjy+"\n故县水库："+gx_ddjy+"\n河口村水库："+hkc_ddjy
    return data

def generate_ddjy(file_path):
    """
    解析 Excel 表格数据。

    参数:
        file_path (str): Excel 文件路径。

    返回:
        list: 包含解析后的数据的字典列表。
    """
    # 读取 Excel 文件
    skMapData, swMapData, date_list = yautils.excel_to_dict(file_path)
    smx_ckll,xld_ckll,lh_ckll,gx_ckll,hkc_ckll = yautils.skddjy(file_path)
    smx_ddjy = process_outflow(smx_ckll,date_list)
    xld_ddjy = process_outflow(xld_ckll,date_list)
    lh_ddjy = process_outflow(lh_ckll,date_list)
    gx_ddjy = process_outflow(gx_ckll,date_list)
    hkc_ddjy = process_outflow(hkc_ckll,date_list)
    data = "三门峡水库："+smx_ddjy+"\n小浪底水库："+xld_ddjy+"\n陆浑水库："+lh_ddjy+"\n故县水库："+gx_ddjy+"\n河口村水库："+hkc_ddjy
    return data

def yujingdengji(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    print("预警等级")
    """
    TODO 条件
    :param smx_sw:
    :param lh_sw:
    :param xld_sw:
    :param gx_sw:
    :param dph_sw:
    :param hkc_sw:
    :param swz_ll:
    :return:
    """
    smx_sw = shuiku_shuiwei.get("三门峡", {}).get('level', 0)
    xld_sw = shuiku_shuiwei.get("小浪底", {}).get('level', 0)
    lh_sw = shuiku_shuiwei.get("陆浑", {}).get('level', 0)
    gx_sw = shuiku_shuiwei.get("故县", {}).get('level', 0)
    hkc_sw = shuiku_shuiwei.get("河口村", {}).get('level', 0)
    dph_sw = shuiku_shuiwei.get("东平湖", {}).get('level', 0)

    knh_ll = shuiwenzhan_liuliang.get("唐乃亥", {}).get('flow', 0)
    lz_ll = shuiwenzhan_liuliang.get("兰州", {}).get('flow', 0)
    szs_ll = shuiwenzhan_liuliang.get("石嘴山", {}).get('flow', 0)
    lm_ll = shuiwenzhan_liuliang.get("龙门", {}).get('flow', 0)
    tg_ll = shuiwenzhan_liuliang.get("潼关", {}).get('flow', 0)
    hx_ll = shuiwenzhan_liuliang.get("华县", {}).get('flow', 0)
    hyk_ll = shuiwenzhan_liuliang.get("花园口", {}).get('flow', 0)
    gc_ll = shuiwenzhan_liuliang.get("高村", {}).get('flow', 0)
    wl_ll = shuiwenzhan_liuliang.get("武陟", {}).get('flow', 0)
    act_flag, lev = None, None#huangwei_yujing_rec()
    print(act_flag, lev)
    if (act_flag and lev == 'Ⅰ') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or xld_sw >= 275 or smx_sw >= 335 or knh_ll >= 5000 or lz_ll >= 6500 or szs_ll >= 5500 or lm_ll >= 18000 or tg_ll >= 15000 or hyk_ll >= 15000 or hx_ll >= 8000 or wl_ll >= 4000:
        print("# 启动防汛一级应急响应")
        return """按照《黄河防汛抗旱应急预案》，启动一级应急响应，响应行动如下：（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛一级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导，动员社会力量支援黄河抗洪抢险救灾。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作，各职能组充实人员。黄委全体职工全力投入抗洪抢险工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 3 次，每日至少提供12 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖、北金堤滞洪区运用的分析研判；宣传组适时举行新闻发布会，向社会报道黄河抗洪抢险动态，做好新闻宣传工作。（4）黄河防总根据汛情需要，及时增派司局级领导带队的工作组、专家组赶赴现场，指导抗洪抢险救灾工作。（5）根据各地抗洪抢险需要，黄河防总按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险，必要时请求国家防总调动流域内外抢险队、物资支援黄河抗洪抢险。（6）有关省区防汛抗旱指挥机构的主要负责同志主持会商，动员部署防汛工作；按照权限组织调度水工程；根据预案转移安置危险地区群众，组织强化巡堤查险和堤防防守，及时控制险情；增派工作组、专家组赴一线指导防汛工作；受灾地区的各级防汛抗旱指挥机构负责人、成员单位负责人，应按照职责到分管的区域组织指挥防汛工作，或驻点具体帮助重灾区做好防汛工作；可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险；将工作情况上报省区人民政府及黄河防总。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期，动员一切社会力量投入黄河抗洪抢险"""
    if (act_flag and lev == 'Ⅱ') or lh_sw >= 327.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 - 0.5 or gx_sw >= 547.39 or xld_sw >= 274 or smx_sw >= 335 or knh_ll >= 4000 or lz_ll >= 5000 or szs_ll >= 4000 or lm_ll >= 12000 or tg_ll >= 10000 or hyk_ll >= 8000 or hx_ll >= 6000 or wl_ll >= 3000:
        print("# 启动防汛二级应急响应")
        return """按照《黄河防汛抗旱应急预案》，启动二级应急响应，响应行动如下：（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛二级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。黄委全体职工做好随时投入抗洪抢险工作的准备。（4）黄河防总实时掌握雨情、水情、汛情（凌情）、工情、险情、灾情动态。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 2 次，每日至少提供 6 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖滞洪区运用的分析研判；宣传组定期举行新闻发布会，向社会公布黄河抗洪抢险动态。（5）黄河防总办公室根据汛情需要，及时派出司局级领导带队的工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（7）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府主要负责同志、国家防总及黄河防总。按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期。"""
    if (act_flag and lev == 'Ⅲ') or lh_sw >= 319.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 3000 or lz_ll >= 4000 or szs_ll >= 3000 or lm_ll >= 8000 or tg_ll >= 8000 or hyk_ll >= 6000 or hx_ll >= 4000 or wl_ll >= 2000:
        # 启动防汛三级应急响应
        print("# 启动防汛三级应急响应")
        return """按照《黄河防汛抗旱应急预案》，启动三级应急响应，响应行动如下：（1）黄河防总秘书长主持防汛会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛三级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥、常务副总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 1 次，每日至少提供 3 次（8 时、14 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度；宣传组加强黄河抗洪抢险宣传。（4）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。黄委防汛物资、黄河机动抢险队支援抗洪抢险。（5）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府分管负责同志和黄河防总。可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。在省级主要媒体及新媒体平台发布防汛抗旱有关情况。"""
    if (act_flag and lev == 'IV') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 2500 or lz_ll >= 2500 or szs_ll >= 2000 or lm_ll >= 5000 or tg_ll >= 5000 or hyk_ll >= 4000 or hx_ll >= 2500 or wl_ll >= 1000:
        # 启动防汛四级应急响应
        print("# 启动防汛四级应急响应")
        return """按照《黄河防汛抗旱应急预案》，启动四级应急响应，响应行动如下：（1）黄河防总秘书长主持会商，研究部署抗洪抢险工作，确定运行机制。响应期间，根据汛情发展变化，受黄河防总秘书长委托，可由黄河防总办公室副主任主持会商，并将情况报黄河防总秘书长。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛四级应急响应的命令及黄河汛情，对防汛工作提出要求，并向国家防办、水利部报告有关情况，必要时向黄河防总总指挥、常务副总指挥报告。（3）黄河防总办公室成员单位人员坚守工作岗位，加强防汛值班值守。按照黄委防御大洪水职责分工和机构设置，综合调度、水情测报和工情险情组等人员上岗到位。其余成员单位按照各自职责做好技术支撑、通信保障、后勤及交通保障，加强宣传报道。水情测报组及时分析天气形势并结合雨水情发展态势，做好雨情、水情、沙情的预测预报，加强与水利部信息中心、黄河流域气象中心、省区气象水文部门会商研判，每日至少制作发布气象水情预报 1 次，每日至少提供 2 次（8 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报。（4）黄委按照批准的洪水调度方案，结合当前汛情做好水库等水工程调度，监督指导地方水行政主管部门按照调度权限做好水工程调度。（5）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；按照预案做好辖区内巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，必要时请调解放军和武警部队、民兵参加重要堤段、重点工程的防守或突击抢险；派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府和黄河防总办公室。"""
    print("""预警等级: 按照《黄河防汛抗旱应急预案》，当前无预警""")
    return """按照《黄河防汛抗旱应急预案》，当前无预警"""



def search_fragpacks(query, top_k=5):
    from yunheKGPro.settings import embedding
    """
    根据 query 检索知识片段，并返回分数最高的文本片段。

    参数:
        query (str): 查询字符串。
        top_k (int): 返回的相似片段数量，默认为 1。

    返回:
        分数最高的文本片段（str）。
        如果向量库不存在或未检索到结果，返回 None。
    """
    # 构建知识库目录路径
    kgdir = f"../data/knowledges/264c159aa9e1dd91e31ab9f38f3d4f9c"
    if not os.path.exists(kgdir):
        os.makedirs(kgdir)
    # 构建向量库文件路径
    index_path = os.path.join(kgdir, "faiss.index")
    # 如果向量库不存在，返回 None
    if not os.path.exists(index_path):
        print("❌ 向量库不存在")
        return None
    # 加载 embedding 模型和向量库
    print("✅ 加载 embedding 模型")
    db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    print("✅ 已加载现有向量库")
    # 执行向量检索
    fragpacks = db.similarity_search_with_score(query, top_k)

    # 如果没有检索到结果，返回 None
    if not fragpacks:
        print("❌ 未检索到任何结果")
        return None
    # 找到分数最高的结果
    highest_score_doc = max(fragpacks, key=lambda x: x[1])  # 按分数排序，取最高分
    return highest_score_doc[0].page_content

def oauth_login(
        access_key: str = "fxylh",
        secret_key: str = "656ed363fa5513bb9848b430712290b2",
        user_type: int = 3
) :
    """
    """
    url = "http://10.4.158.35:8070/oauth/login"
    headers = {"Content-Type": "application/json",
        "Accept": "application/json"}
    payload = {"accessKey": access_key, "secretKey": secret_key, "userType": user_type}
    try:
        response = requests.post(url=url,headers=headers,data=json.dumps(payload),timeout=10)
        response.raise_for_status()
        return response.json()['data']

    except requests.exceptions.RequestException as e:
        return {"code": 500,"data": None,"msg": f"请求失败: {str(e)}"}
    except ValueError:
        return {"code": 500,"data": None,"msg": "响应数据解析失败"}

def get_rainfall_data_day(basin=None, start_time=None, end_time=None):
    """
    获取实时雨量数据（带完整错误处理和JWT鉴权）

    参数:
        basin: 流域编码 (如"RH01")
        start_time: 开始时间 (格式: "2024-03-01")，若不传则默认为昨天
        end_time: 结束时间 (格式: "2024-03-02")，若不传则默认为今天

    返回:
        (status_code, response_data) 元组
    """
    # 构造请求参数
    params = {}
    # 设置默认时间范围（今天和昨天）
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    # 处理时间参数
    params["endDate"] = end_time if end_time else today
    params["startDate"] = start_time if start_time else yesterday
    if basin:
        params["stcd"] = basin
    try:
        # 使用提供的JWT token
        auth_token = oauth_login()

        # 添加超时和请求头
        response = requests.get(
            url="http://10.4.158.35:8070/rainfall/dayrt/getRainfall",
            params=params,
            headers={
                "Accept": "application/json",
                "Authorization": f"{auth_token}"
            },
            timeout=10  # 10秒超时
        )
        response.raise_for_status()  # 自动检查4xx/5xx错误
        return response.status_code, response.json()

    except requests.exceptions.Timeout:
        return 408, {"error": "请求超时"}
    except requests.exceptions.RequestException as e:
        return 500, {"error": f"请求失败: {str(e)}"}
    except ValueError:  # JSON解析错误
        return 500, {"error": "返回数据格式异常"}


def generate_rainfall_report(response_data):
    """
    生成降雨量报告文本

    参数:
        response_data: API返回的JSON数据

    返回:
        降雨量报告文本
    """
    if not response_data or 'data' not in response_data:
        return "无有效降雨数据"

    # 筛选伊洛河流域站点(416开头)
    yiluo_stations = [station for station in response_data['data']
                      if str(station['stcd']).startswith('416')]

    if not yiluo_stations:
        return "伊洛河流域无降雨监测数据"

    # 统计降雨等级
    rainfall_stats = {
        '小雨': 0,
        '中雨': 0,
        '大雨': 0,
        '暴雨': 0,
        '大暴雨': 0,
        '特大暴雨': 0
    }

    max_rainfall = 0
    max_station = ""

    for station in yiluo_stations:
        rf = station['rf']

        if rf == 0:
            continue

        if rf < 10:
            rainfall_stats['小雨'] += 1
        elif 10 <= rf < 25:
            rainfall_stats['中雨'] += 1
        elif 25 <= rf < 50:
            rainfall_stats['大雨'] += 1
        elif 50 <= rf < 100:
            rainfall_stats['暴雨'] += 1
        elif 100 <= rf < 250:
            rainfall_stats['大暴雨'] += 1
        else:
            rainfall_stats['特大暴雨'] += 1

        # 记录最大降雨量
        if rf > max_rainfall:
            max_rainfall = rf
            max_station = station['stnm']

    # 如果没有降雨
    if all(count == 0 for count in rainfall_stats.values()):
        return f"{datetime.now().month}月{datetime.now().day}日，伊洛河流域无降雨"

    # 生成报告文本
    today = datetime.now()
    report_parts = [f"{today.month}月{today.day}日，伊洛河流域"]

    # 添加降雨描述
    rainfall_desc = []
    if rainfall_stats['小雨'] > 0:
        rainfall_desc.append("小雨")
    if rainfall_stats['中雨'] > 0:
        rainfall_desc.append("中雨")
    if rainfall_stats['大雨'] > 0:
        rainfall_desc.append("大雨")
    if rainfall_stats['暴雨'] > 0:
        rainfall_desc.append("暴雨")
    if rainfall_stats['大暴雨'] > 0:
        rainfall_desc.append("大暴雨")
    if rainfall_stats['特大暴雨'] > 0:
        rainfall_desc.append("特大暴雨")
    if rainfall_desc:
        report_parts.append("大部地区降" + "、".join(rainfall_desc))
    # 添加最大降雨点
    if max_rainfall > 0:
        report_parts.append(f"，最大点雨量{max_station}站{max_rainfall}毫米")
    return "".join(report_parts)

def get_hydrometric_station(station_code=None, ):
    """
    获取河道水文站基本信息

    参数:
        station_code: 水文站代码 (String, 可选)
        auth_token: JWT认证令牌 (String)

    返回:
        (status_code, response_data) 元组
    """
    auth_token = oauth_login()

    try:
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"
        }

        params = {}
        if station_code:
            params["stcd"] = station_code
        HYDROMETRIC_API_URL = "http://10.4.158.35:8070/hydrometric/hourrt/listLatest"
        response = requests.get(
            HYDROMETRIC_API_URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        return response.status_code, response.json()

    except requests.exceptions.Timeout:
        return 408, {"error": "请求超时"}
    except requests.exceptions.RequestException as e:
        return 500, {"error": f"请求失败: {str(e)}"}
    except ValueError:
        return 500, {"error": "返回数据格式异常"}

def format_hydrometric_data(station_code=None):
    """
    获取并格式化水文站数据

    参数:
        station_code: 水文站代码 (可选)

    返回:
        (status_code, formatted_data) 元组
        formatted_data格式示例:
        {
            "hdsq": [
                {
                    "站名": "站名1",
                    "时间": "2023-01-01 08:00",
                    "流量(m³/s)": 100.5,
                    "水位(m)": 50.2
                },
                ...
            ]
        }
    """
    # 首先获取原始数据
    status_code, raw_data = get_hydrometric_station(station_code)

    # 如果请求不成功，直接返回原始结果
    if status_code != 200:
        return status_code, raw_data

    # 初始化格式化后的数据
    formatted_data = {"hdsq": []}

    try:
        # 处理数据
        if 'data' in raw_data and isinstance(raw_data['data'], list):
            for station in raw_data['data']:
                # 只处理416开头的站点
                if str(station.get('stcd', '')).startswith('416'):
                    # 转换时间戳
                    timestamp = station.get('date')
                    if timestamp:
                        dt = datetime.fromtimestamp(timestamp / 1000)
                        time_str = dt.strftime("%Y-%m-%d %H:%M")
                    else:
                        time_str = "时间未知"

                    # 构建格式化条目
                    formatted_entry = {
                        "站名": station.get('stnm', '未知站名'),
                        "时间": time_str,
                        "流量(m³/s)": station.get('dstrvm', 0),
                        "水位(m)": station.get('level', 0)
                    }
                    formatted_data["hdsq"].append(formatted_entry)

        return status_code, formatted_data

    except Exception as e:
        return 500, {"error": f"数据处理错误: {str(e)}"}

def get_sk_data():
    """
    获取河道水文站基本信息

    参数:
        station_code: 水文站代码 (String, 可选)
        auth_token: JWT认证令牌 (String)

    返回:
        (status_code, response_data) 元组
    """
    auth_token = oauth_login()

    try:
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"
        }

        params = {}
        HYDROMETRIC_API_URL = "http://10.4.158.35:8070/hydrometric/rhourrt/listLatest"
        response = requests.get(
            HYDROMETRIC_API_URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()
        return response.status_code, response.json()

    except requests.exceptions.Timeout:
        return 408, {"error": "请求超时"}
    except requests.exceptions.RequestException as e:
        return 500, {"error": f"请求失败: {str(e)}"}
    except ValueError:
        return 500, {"error": "返回数据格式异常"}


def format_reservoir_data():
    """
    获取并格式化水库数据
    返回:
        dict: 格式化后的水库数据，结构如下:
        {
            "sksq": [
                {
                    "水库名称": str,
                    "水位（m）": float,
                    "蓄量（亿m³）": float,
                    "入库流量": float,
                    "出库流量": float
                },
                ...
            ]
        }
    """
    # 获取原始数据
    status_code, raw_data = get_sk_data()
    #logger.debug(f"原始数据:{raw_data}")

    # 初始化结果字典
    formatted_data = {"sksq": []}

    try:
        # 检查请求是否成功且数据格式正确
        if status_code == 200 and isinstance(raw_data, dict) and "data" in raw_data and isinstance(raw_data["data"],list):
            for reservoir in raw_data["data"]:  # 注意这里应该是raw_data["data"]
                formatted_entry = {
                    "水库名称": reservoir.get("ennm", "未知水库"),
                    "水位（m）": round(float(reservoir.get("level", 0)), 2),
                    "蓄量（亿m³）": round(float(reservoir.get("wq", 0)), 3),
                    "入库流量（m³/s）": round(float(reservoir.get("inflow", 0)), 2),
                    "出库流量（m³/s）": round(float(reservoir.get("outflow", 0)), 2)
                }
                formatted_data["sksq"].append(formatted_entry)

        return formatted_data

    except Exception as e:
        print(f"数据格式化错误: {str(e)}")
        return {"sksq": []}

if __name__ == '__main__':
    import time
    import matplotlib.pyplot as plt
    res = search_fragpacks("雨水情信息")
    print(res)
#     # 记录开始时间
#     r = yautils.excel_to_dict("../../mainapp/media/ddfa/3/2025-03-03.xlsx")
#     skMapData, swMapData, date_list = r
#     # pprint.pprint(r)
#     start_time = time.time()
#     # 调用函数并获取结果
#     res = yautils.skddjy_new("../../mainapp/media/ddfa/3/2025-03-03.xlsx")
#     ddjy_list = []
#     # 遍历返回的结果字典
#     for key, value in res.items():
#         # 处理每个水库的出流量
#         ckll = process_outflow(value, date_list)
#         ddjy_list.append(f"{key}水库：{ckll}")
#     # 将所有水库的调度建议合并为一个字符串
#     ddjy = "\n".join(ddjy_list)
#     # 记录结束时间
#     end_time = time.time()
#     # 计算并打印执行时间
#     execution_time = end_time - start_time
#     print(f"水库调度建议：\n{ddjy}")
#     print(f"代码执行时间：{execution_time:.4f} 秒")
#     plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
#     plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#
#     # 示例数据
#     data = {
#         "水库名称": ["故县水库", "陆浑水库", "河口村水库", "三门峡水库", "小浪底水库"],
#         "开始时间": ["2021-10-27 08:00:00"] * 5,
#         "结束时间": ["2021-10-27 22:00:00"] * 5,
#         "流量": [1000, 900, 4000, 500, 4500],  # 流量值，三门峡为敞泄（假设为0）
#     }
#
#     # 转换为 DataFrame
#     df = pd.DataFrame(data)
#
#     # 将时间转换为 datetime 格式
#     df["开始时间"] = pd.to_datetime(df["开始时间"])
#     df["结束时间"] = pd.to_datetime(df["结束时间"])
#
#     # 创建图表
#     plt.figure(figsize=(12, 6))
#
#     # 绘制每个水库的调度时间段
#     for i, row in df.iterrows():
#         # 绘制时间段
#         plt.plot([row["开始时间"], row["结束时间"]], [row["流量"], row["流量"]],
#                  marker="o", label=row["水库名称"], linewidth=2)
#         # # 标注流量值
#         # plt.text(row["开始时间"], row["流量"], f"{row['流量']} m³/s",
#         #          va="bottom", ha="right", fontsize=10, color="blue")
#
#     # 设置图表属性
#     plt.xlabel("时间", fontsize=12)
#     plt.ylabel("出库流量 (立方米/秒)", fontsize=12)
#     plt.title("水库调度方式时间序列图", fontsize=14)
#     plt.grid(True, linestyle="--", alpha=0.6)  # 网格线
#     plt.legend(loc="upper right", fontsize=10)  # 图例
#
#     # 设置 X 轴时间格式
#     plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S'))
#     plt.gcf().autofmt_xdate()  # 自动旋转 X 轴标签
#
#     # 显示图表
#     plt.tight_layout()
#     plt.show()