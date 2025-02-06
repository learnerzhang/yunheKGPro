
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
