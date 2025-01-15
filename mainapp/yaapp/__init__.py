import pandas as pd
import datetime


def getYuAnParamPath(ctype, mydate):
    """
        获取对应的参数路径
    """
    if ctype == 0:
        return f"data/plans/HHZXY_api_data_{mydate}.json"
    elif ctype == 1:
        return f"data/plans/XLDQX_api_data_{mydate}.json"
    elif ctype == 2:
        return f"data/plans/XLDTSTS_api_data_{mydate}.json"
    return "data/plans/default.json"


def getYuAnName(ctype, mydate):
    """
    生产标准的预案名称
    """
    format_name = f"{mydate}黄河中下游防汛调度预案" 
    if ctype == 1:
        format_name = f"{mydate}小浪底秋汛防汛调度预案"
    elif ctype == 2:
        format_name = f"{mydate}小浪底调水调沙防汛调度预案"

    return format_name


def img2base64(imgpath):
    import base64
    with open(imgpath, 'rb') as f:
        data = f.read()
        encoded_string = base64.b64encode(data)
        return encoded_string.decode('utf-8')



def paraHtml(text):
    paraHtmlText = "<p>" + text +  "</p>"
    return paraHtmlText


def divHtml(text):
    paraHtmlText = "<div style='text-align: center;'>" + text +  "</div>"
    return paraHtmlText



def pd2HtmlCSS():
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


def xld_sk(shuiku_shuiwei: dict, shuiwenzhan_liuliang: dict):
    sw = shuiku_shuiwei.get("小浪底", {}).get('level', 0)
    hyk_liuliang = shuiwenzhan_liuliang.get("花园口", {}).get('flow', 0)
    tongguan_liuliang = shuiwenzhan_liuliang.get("潼关", {}).get('flow', 0)
    rate_p = float(tongguan_liuliang) / (float(hyk_liuliang) + 0.001)
    print("小浪底SK", hyk_liuliang,tongguan_liuliang, sw)
    """
    小浪底库
    :return:
    """
    if hyk_liuliang <= 4500:
        return "适时调节水沙，按控制花园口站流量不大于4500m³/s的原则泄洪。西霞院水库配合小浪底水库泄洪排沙"
    elif hyk_liuliang <= 8000:
        return "原则上按控制花园口站4500m³/s方式运用。若洪水主要来源于三门峡以上，视来水来沙及水库淤积情况，适时按进出库平衡方式运用。控制水库最高运用水位不超过254m。西霞院水库配合小浪底水库泄洪排沙"
    elif hyk_liuliang <= 10000:
        if rate_p > 0.6:
            return "小浪底：原则上按进出库平衡方式运用。西霞院水库配合小浪底水库泄洪排沙"
        else:
            return "小浪底：视下游汛情，适时按控制花园口站不大于8000m³/s的方式运用。西霞院水库配合小浪底水库泄洪排沙"
    elif hyk_liuliang <= 22000:
        if rate_p > 0.6:
            return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
        else:
            if hyk_liuliang - tongguan_liuliang < 9000:
                return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
            else:
                return "小浪底：按不大于1000m³/s（发电流量）下泄。西霞院水库配合小浪底水库泄洪排沙"
    else:
        # 潼关 花园口 流量大于60%
        if rate_p > 0.6:
            if sw < 273.5:
                return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
            else:
                return "小浪底：按进出库平衡或敞泄运用。西霞院水库配合小浪底水库泄洪排沙"
        else:
            return "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"


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
        output.append(f"{start_time}起按{unique_values[i]}m³/s泄放 {hours}个小时")
    res = "，".join(output) + "。"
    return res

def generate_ddjy(file_path):
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