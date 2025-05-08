import logging
logger = logging.getLogger('kgproj')

def yujingdengji(smx_sw=None, xld_sw=None, lh_sw=None, gx_sw=None,
                 hkc_sw=None, dph_sw=None,
                 knh_ll=None, lz_ll=None, szs_ll=None,
                 lm_ll=None, tg_ll=None, hx_ll=None,
                 hyk_ll=None, gc_ll=None, wl_ll=None,
                 act_flag=False, lev=None
                 ):
    logger.debug("预警等级")

    # 如果参数为 None，则默认为 0
    smx_sw = smx_sw if smx_sw is not None else 0
    xld_sw = xld_sw if xld_sw is not None else 0
    lh_sw = lh_sw if lh_sw is not None else 0
    gx_sw = gx_sw if gx_sw is not None else 0
    hkc_sw = hkc_sw if hkc_sw is not None else 0
    dph_sw = dph_sw if dph_sw is not None else 0

    knh_ll = knh_ll if knh_ll is not None else 0
    lz_ll = lz_ll if lz_ll is not None else 0
    szs_ll = szs_ll if szs_ll is not None else 0
    lm_ll = lm_ll if lm_ll is not None else 0
    tg_ll = tg_ll if tg_ll is not None else 0
    hx_ll = hx_ll if hx_ll is not None else 0
    hyk_ll = hyk_ll if hyk_ll is not None else 0
    gc_ll = gc_ll if gc_ll is not None else 0
    wl_ll = wl_ll if wl_ll is not None else 0
    level="无预警"
    result = """按照《黄河防汛抗旱应急预案》，当前无预警"""
    if (act_flag and lev == 'Ⅰ') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or xld_sw >= 275 or smx_sw >= 335 or knh_ll >= 5000 or lz_ll >= 6500 or szs_ll >= 5500 or lm_ll >= 18000 or tg_ll >= 15000 or hyk_ll >= 15000 or hx_ll >= 8000 or wl_ll >= 4000:
        logger.debug("# 启动防汛一级应急响应")
        level = "一级预警"
        result = """按照《黄河防汛抗旱应急预案》，启动一级应急响应，响应行动如下：\n（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。\n（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛一级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导，动员社会力量支援黄河抗洪抢险救灾。\n（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作，各职能组充实人员。黄委全体职工全力投入抗洪抢险工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 3 次，每日至少提供12 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖、北金堤滞洪区运用的分析研判；宣传组适时举行新闻发布会，向社会报道黄河抗洪抢险动态，做好新闻宣传工作。\n（4）黄河防总根据汛情需要，及时增派司局级领导带队的工作组、专家组赶赴现场，指导抗洪抢险救灾工作。\n（5）根据各地抗洪抢险需要，黄河防总按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险，必要时请求国家防总调动流域内外抢险队、物资支援黄河抗洪抢险。（6）有关省区防汛抗旱指挥机构的主要负责同志主持会商，动员部署防汛工作；按照权限组织调度水工程；根据预案转移安置危险地区群众，组织强化巡堤查险和堤防防守，及时控制险情；增派工作组、专家组赴一线指导防汛工作；受灾地区的各级防汛抗旱指挥机构负责人、成员单位负责人，应按照职责到分管的区域组织指挥防汛工作，或驻点具体帮助重灾区做好防汛工作；可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险；将工作情况上报省区人民政府及黄河防总。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期，动员一切社会力量投入黄河抗洪抢险"""
        return {"level":level,"result": result}
    if (act_flag and lev == 'Ⅱ') or lh_sw >= 327.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 - 0.5 or gx_sw >= 547.39 or xld_sw >= 274 or smx_sw >= 335 or knh_ll >= 4000 or lz_ll >= 5000 or szs_ll >= 4000 or lm_ll >= 12000 or tg_ll >= 10000 or hyk_ll >= 8000 or hx_ll >= 6000 or wl_ll >= 3000:
        logger.debug("# 启动防汛二级应急响应")
        level = "二级预警"
        result = """按照《黄河防汛抗旱应急预案》，启动二级应急响应，响应行动如下：\n（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。\n（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛二级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。\n（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。黄委全体职工做好随时投入抗洪抢险工作的准备。\n（4）黄河防总实时掌握雨情、水情、汛情（凌情）、工情、险情、灾情动态。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 2 次，每日至少提供 6 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖滞洪区运用的分析研判；宣传组定期举行新闻发布会，向社会公布黄河抗洪抢险动态。\n（5）黄河防总办公室根据汛情需要，及时派出司局级领导带队的工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（7）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府主要负责同志、国家防总及黄河防总。按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期。"""
        return {"level":level,"result": result}
    if (act_flag and lev == 'Ⅲ') or lh_sw >= 319.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 3000 or lz_ll >= 4000 or szs_ll >= 3000 or lm_ll >= 8000 or tg_ll >= 8000 or hyk_ll >= 6000 or hx_ll >= 4000 or wl_ll >= 2000:
        # 启动防汛三级应急响应
        level= "三级预警"
        logger.debug("# 启动防汛三级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动三级应急响应，响应行动如下：\n（1）黄河防总秘书长主持防汛会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。\n（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛三级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥、常务副总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。\n（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 1 次，每日至少提供 3 次（8 时、14 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度；宣传组加强黄河抗洪抢险宣传。\n（4）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。黄委防汛物资、黄河机动抢险队支援抗洪抢险。\n（5）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府分管负责同志和黄河防总。可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。在省级主要媒体及新媒体平台发布防汛抗旱有关情况。"""
        return {"level":level,"result": result}
    if (act_flag and lev == 'IV') or lh_sw >= 317.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 2500 or lz_ll >= 2500 or szs_ll >= 2000 or lm_ll >= 5000 or tg_ll >= 5000 or hyk_ll >= 4000 or hx_ll >= 2500 or wl_ll >= 1000:
        # 启动防汛四级应急响应
        level = "四级预警"
        logger.debug("# 启动防汛四级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动四级应急响应，响应行动如下：\n（1）黄河防总秘书长主持会商，研究部署抗洪抢险工作，确定运行机制。响应期间，根据汛情发展变化，受黄河防总秘书长委托，可由黄河防总办公室副主任主持会商，并将情况报黄河防总秘书长。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛四级应急响应的命令及黄河汛情，对防汛工作提出要求，并向国家防办、水利部报告有关情况，必要时向黄河防总总指挥、常务副总指挥报告。\n（3）黄河防总办公室成员单位人员坚守工作岗位，加强防汛值班值守。按照黄委防御大洪水职责分工和机构设置，综合调度、水情测报和工情险情组等人员上岗到位。其余成员单位按照各自职责做好技术支撑、通信保障、后勤及交通保障，加强宣传报道。水情测报组及时分析天气形势并结合雨水情发展态势，做好雨情、水情、沙情的预测预报，加强与水利部信息中心、黄河流域气象中心、省区气象水文部门会商研判，每日至少制作发布气象水情预报 1 次，每日至少提供 2 次（8 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报。\n（4）黄委按照批准的洪水调度方案，结合当前汛情做好水库等水工程调度，监督指导地方水行政主管部门按照调度权限做好水工程调度。\n（5）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；按照预案做好辖区内巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，必要时请调解放军和武警部队、民兵参加重要堤段、重点工程的防守或突击抢险；派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府和黄河防总办公室。"""
        return {"level":level,"result": result}
    logger.debug("""预警等级: 按照《黄河防汛抗旱应急预案》，当前无预警""")
    return {"level":level,"result": result}


def smx_sk(smx_sw: int = None, hyk_liuliang: int = None):
    smx_sw = smx_sw if smx_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    """
    三门峡水库调度方案
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


def xld_sk(xld_sw: int = None, hyk_liuliang: int = None, tongguan_liuliang: int = None):
    xld_sw = xld_sw if xld_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0
    tongguan_liuliang = tongguan_liuliang if tongguan_liuliang is not None else 0

    rate_p = float(tongguan_liuliang) / (float(hyk_liuliang) + 0.001)
    #logger.debug("小浪底SK", hyk_liuliang, tongguan_liuliang, xld_sw)
    """
    小浪底库调度方案
    """
    result = {}

    if hyk_liuliang <= 4500:
        result['result'] = "适时调节水沙，按控制花园口站流量不大于4500m³/s的原则泄洪。西霞院水库配合小浪底水库泄洪排沙"
    elif hyk_liuliang <= 8000:
        result['result'] = "原则上按控制花园口站4500m³/s方式运用。若洪水主要来源于三门峡以上，视来水来沙及水库淤积情况，适时按进出库平衡方式运用。控制水库最高运用水位不超过254m。西霞院水库配合小浪底水库泄洪排沙"
    elif hyk_liuliang <= 10000:
        if rate_p > 0.6:
            result['result'] = "小浪底：原则上按进出库平衡方式运用。西霞院水库配合小浪底水库泄洪排沙"
        else:
            result['result'] = "小浪底：视下游汛情，适时按控制花园口站不大于8000m³/s的方式运用。西霞院水库配合小浪底水库泄洪排沙"
    elif hyk_liuliang <= 22000:
        if rate_p > 0.6:
            result['result'] = "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
        else:
            if hyk_liuliang - tongguan_liuliang < 9000:
                result['result'] = "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
            else:
                result['result'] = "小浪底：按不大于1000m³/s（发电流量）下泄。西霞院水库配合小浪底水库泄洪排沙"
    else:
        if rate_p > 0.6:
            if xld_sw < 273.5:
                result['result'] = "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"
            else:
                result['result'] = "小浪底：按进出库平衡或敞泄运用。西霞院水库配合小浪底水库泄洪排沙"
        else:
            result['result'] = "小浪底：按控制花园口站10000m³/s方式运用。西霞院水库配合小浪底水库泄洪排沙"

    return result


def lh_sk(lh_sw: int = None, hyk_liuliang: int = None):
    """
    陆浑水库调度方案
    """
    lh_sw = lh_sw if lh_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    #logger.debug("陆浑水库SK", hyk_liuliang, lh_sw)

    result = {}

    if hyk_liuliang <= 4500:
        if lh_sw < 321.5:
            result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
        else:
            result['result'] = "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 8000:
        if lh_sw < 321.5:
            result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
        else:
            result['result'] = "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 10000:
        if lh_sw < 321.5:
            result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
        else:
            result['result'] = "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 22000:
        if hyk_liuliang <= 12000:
            if lh_sw < 321.5:
                result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
            else:
                result['result'] = "按进出库平衡或敞泄运用"
        else:
            if lh_sw < 323:
                result['result'] = "按不超过发电流量控泄"
            else:
                result['result'] = "按进出库平衡或敞泄运用"
    else:
        if lh_sw < 323:
            result['result'] = "按不超过发电流量控泄"
        else:
            result['result'] = "按进出库平衡或敞泄运用"

    return result

def gx_sk(gx_sw: int = None, hyk_liuliang: int = None):
    """
    故县水库调度方案
    """
    gx_sw = gx_sw if gx_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    #logger.debug("故县SK", hyk_liuliang, gx_sw)

    result = {}

    if hyk_liuliang <= 4500:
        if gx_sw < 542.04:
            result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
        else:
            result['result'] = "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 8000:
        if gx_sw < 542.04:
            result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
        else:
            result['result'] = "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 10000:
        if gx_sw < 542.04:
            result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
        else:
            result['result'] = "按进出库平衡或敞泄运用"
    elif hyk_liuliang <= 22000:
        if hyk_liuliang <= 12000:
            if gx_sw < 542.04:
                result['result'] = "按控制下泄流量不大于1000m³/s方式运用"
            else:
                result['result'] = "按进出库平衡或敞泄运用"
        else:
            if gx_sw < 546.84:
                result['result'] = "按不超过发电流量控泄"
            else:
                result['result'] = "按进出库平衡或敞泄运用"
    else:
        if gx_sw < 546.84:
            result['result'] = "按不超过发电流量控泄"
        else:
            result['result'] = "按进出库平衡或敞泄运用"

    return result

def hkc_sk(hkc_sw: int = None, hyk_liuliang: int = None):
    """
    河口村水库调度方案
    """
    hkc_sw = hkc_sw if hkc_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    #logger.debug("河口村SK", hyk_liuliang, hkc_sw)

    result = {}

    if hyk_liuliang <= 4500:
        if hkc_sw < 254.5:
            result['result'] = "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        elif hkc_sw < 285.43:
            result['result'] = "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            result['result'] = "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    elif hyk_liuliang <= 8000:
        if hkc_sw < 254.5:
            result['result'] = "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        elif hkc_sw < 285.43:
            result['result'] = "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            result['result'] = "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    elif hyk_liuliang <= 10000:
        if hkc_sw < 254.5:
            result['result'] = "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        elif hkc_sw < 285.43:
            result['result'] = "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            result['result'] = "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    elif hyk_liuliang <= 22000:
        if hyk_liuliang <= 12000:
            if hkc_sw < 254.5:
                result['result'] = "按控制武陟不大于2000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
            elif hkc_sw < 285.43:
                result['result'] = "按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
            else:
                result['result'] = "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            if hkc_sw < 254.5:
                result['result'] = "关闭所有泄流设施。张峰水库适时配合河口村水库拦洪运用"
            elif hkc_sw < 285.43:
                result['result'] = "尽可能按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
            else:
                result['result'] = "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"
    else:
        if hkc_sw < 254.5:
            result['result'] = "关闭所有泄流设施。张峰水库适时配合河口村水库拦洪运用"
        elif hkc_sw < 285.43:
            result['result'] = "尽可能按控制武陟不大于4000m³/s方式运用。张峰水库适时配合河口村水库拦洪运用"
        else:
            result['result'] = "按进出库平衡方式运用。张峰水库适时配合河口村水库拦洪运用"

    return result

def wh_shzhfy(hhgl_liuliang=None,  # 黄河干流流量
              h1_jiangyu=None,    # 1小时降雨量
              bhw_yujing=None,    # 渤海湾预警
              qls_yujing=None,    # 千里山预警
              sdmg_yujing=None,   # 石大门沟预警
              nzw_shzmj=None,     # 农作物受旱灾面积
              ysknrk=None):       # 饮水困难人口比例
    # 如果参数为 None，则默认为 0
    hhgl_liuliang = hhgl_liuliang if hhgl_liuliang is not None else 0
    h1_jiangyu = h1_jiangyu if h1_jiangyu is not None else 0
    bhw_yujing = bhw_yujing if bhw_yujing is not None else 0
    qls_yujing = qls_yujing if qls_yujing is not None else 0
    sdmg_yujing = sdmg_yujing if sdmg_yujing is not None else 0
    nzw_shzmj = nzw_shzmj if nzw_shzmj is not None else 0
    ysknrk = ysknrk if ysknrk is not None else 0

    result = "当前无预警"

    # 判断响应级别
    if hhgl_liuliang > 6000 or h1_jiangyu > 40 or bhw_yujing == 2  or qls_yujing == 1 or sdmg_yujing ==1 or nzw_shzmj > 0.6 or ysknrk >0.09:
        result = ("视情况启动一级响应；\n响应行动：1）水旱灾害防御领导小组组长主持会商，做出防御工作安排，提请自治区水行政主管部门现场指挥调度。水旱灾害防御领导小组办公室和有关单位通报有关情况，并将有关情况报市委、政府、市防汛抗旱指挥部、自治区水行政主管部门。"
                  "\n2）实行局领导带班制度，局属各科室，各二级单位加强应急值守，密切关注雨情、旱情及工程险情的发展变化，跟踪防汛抗旱工作动态，做好上传下达。"
                  "\n3）市水行政主管部门第一时间派出由组长带队的防汛应急工作指导组或防汛应急技术指导组赴一线协助各区指导水旱灾害防御抢险技术工作。"
                  "\n4）相关区水行政主管部门要增加值班人员，密切监视汛情、旱情和工情的发展变化，做好汛情、旱情预测预报，按职责分工全面做好各项防御工作，并按照预案配合区政府立即转移危险地区群众和财产，做好临时安置。"
                  "\n5）遭受洪水地区的区水行政主管部门，组织强化对水库、水闸等重点水利工程调度和堤防的巡查、防守，实时掌握汛情、险情和旱情的发展变化，及时准确报送信息。"
                  "\n6）遭受旱灾地区的区水行政主管部门，要加强旱情监测和分析研判，按照职责权限做好抗旱应急水源的科学调度与管理。\n7）各专家工作组要按照职责分工和会商工作安排开展工作。")
    elif hhgl_liuliang > 4000 or h1_jiangyu > 30  or bhw_yujing == 2  or qls_yujing == 1 or sdmg_yujing ==1 or nzw_shzmj > 0.4 or ysknrk >0.07:
        result = ("视情况启动二级响应：\n响应行动：1）水旱灾害防御领导小组组长主持会商，做出防御工作安排。水旱灾害防御领导小组办公室将有关情况报市委、政府、市防汛抗旱指挥部和自治区水行政主管部门。"
                  "\n2）实行局领导带班制度，局属各科室，各二级单位加强应急值守，密切关注雨情、旱情及工程险情的发展变化，跟踪防汛抗旱工作动态，做好上传下达。"
                  "\n3）市水行政主管部门第一时间派出由组长带队的防汛应急工作指导组或防汛应急技术指导组赴一线协助各区指导水旱灾害防御抢险技术工作。"
                  "\n4）相关区水行政主管部门要增加值班值守人员，密切监视汛情、旱情和工情的发展变化，做好汛情、旱情预测预报，按职责分工全面做好各项防御工作，并按照预案配合区政府准备做好群众安全转移工作。"
                  "\n5）遭受洪水地区的区水行政主管部门，组织强化对水库、水闸等重点水利工程调度和堤防巡查、防守的技术指导，实时掌握汛情、险情的发展变化，及时准确报送信息。"
                  "\n6）遭受旱灾地区的区水行政主管部门，要加强旱情监测和分析研判，按照职责权限做好抗旱应急水源的科学调度与管理。"
                  "\n7）各专家工作组要按照职责分工和会商工作安排开展工作。")
    elif hhgl_liuliang > 3300 or h1_jiangyu > 15 or bhw_yujing == 3  or qls_yujing == 2 or sdmg_yujing ==2 or nzw_shzmj > 0.2 or ysknrk >0.05:
        result = ("视情况启动三级响应；\n响应行动：1）水旱灾害防御领导小组副组长主持会商，做出防御工作安排。水旱灾害防御领导小组办公室将有关情况报市委、政府、市防汛抗旱指挥部和自治区水行政主管部门。"
                  "\n2）实行局领导带班制度，局属各科室，各二级单位加强应急值守，密切关注雨情、旱情及工程险情的发展变化，跟踪防汛抗旱工作动态，做好上传下达。"
                  "\n3）市水行政主管部门在24小时内派出由副组长带队的防汛应急工作指导组或防汛应急技术指导组赴一线协助各区指导水旱灾害防御抢险技术工作。"
                  "\n4）相关区水行政主管部门加强水旱灾害防御工作指导，增加值班人员，密切监视汛情、旱情和工情的发展变化，按职责分工全面做好各项防御工作。"
                  "\n5）相关区水行政主管部门组织力量做好水利工程初期险情处置和防洪工程抢险的技术指导。根据汛情、险情，区水行政主管部门要及时提请当地政府做好抗洪抢险及险情处置等工作。"
                  "\n6）遭受洪水地区的区水行政主管部门，组织强化对水库、水闸等重点水利工程调度和堤防巡查、防守的技术指导，实时掌握汛情、险情的发展变化，及时准确报送信息。"
                  "\n7）遭受旱灾地区的区水行政主管部门，要加强旱情监测和分析研判，按照职责权限做好抗旱应急水源的科学调度与管理。"
                  "\n8）各专家工作组要按照职责分工和会商工作安排开展工作。")
    elif hhgl_liuliang > 3000 or h1_jiangyu > 10  or qls_yujing == 3 or sdmg_yujing ==3 or nzw_shzmj > 0.1 or ysknrk >0.03:
        result = ("视情况启动四级响应：\n响应行动：1）水旱灾害防御领导小组副组长主持会商，做出防御工作安排。水旱灾害防御领导小组办公室将有关情况报市委、政府、市防汛抗旱指挥部和自治区水行政主管部门。"
                  "\n2）实行局领导带班制度，局属各科室，各二级单位加强应急值守，密切关注雨情、旱情及工程险情的发展变化，跟踪防汛抗旱工作动态，做好上传下达。"
                  "\n3）视情况派出防汛应急工作指导组或防汛应急技术指导组赴一线协助各区指导水旱灾害防御抢险技术工作。"
                  "\n4）各区水行政主管部门组织力量做好水利工程初期险情处置和防洪工程抢险的技术指导，根据汛情、险情，及时提请当地政府做好抗洪抢险及险情处置等工作。"
                  "\n5）各区水行政主管部门按照职责权限做好水利工程的运行调度工作，加强汛情、旱情的监测预报。"
                  "\n6）遭受洪水地区的区水行政主管部门，要进一步加强对水库、水闸和堤防等重点水利工程的巡查值守，实时掌握汛情、险情的发展变化，及时准确报送信息。"
                  "\n7）遭受旱灾地区的区水行政主管部门，要加强旱情监测和分析研判，按照职责权限做好抗旱应急水源的科学调度与管理。"
                  "\n8）各专家工作组要按照职责分工和会商工作安排开展工作。")
    return {"result": result}

def tanquyanmo(hyk_liuliang, usetag=False):
    """
    滩区淹没（参数【花园口流量】）
    :return: dict
    """
    logger.debug("滩区淹没（参数【花园口流量】）")

    def k_value(start, end, value, liuliang):
        return round(1.0 * value * (liuliang - start) / (end - start), 2)

    if hyk_liuliang <= 4000:
        main_str = "属于主河道正常行洪，不会发生漫滩。此级洪水没有村庄被洪水围困，不需要迁移安置滩区群众。"
    elif hyk_liuliang <= 6000:
        main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(4000, 6000, 70, hyk_liuliang)),
            k_value(4000, 6000, 6.18, hyk_liuliang),
            int(k_value(4000, 6000, 273, hyk_liuliang)),
            k_value(4000, 6000, 24.85, hyk_liuliang),
            k_value(4000, 6000, 110.29, hyk_liuliang),
            k_value(4000, 6000, 70.81, hyk_liuliang),
            k_value(4000, 6000, 140.87, hyk_liuliang),
        ) + "山东省预计漫滩面积万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，需转移安置{}万人，就地或就近安置{}万人。".format(
            k_value(4000, 6000, 39.07, hyk_liuliang),
            int(k_value(4000, 6000, 93, hyk_liuliang)),
            int(k_value(4000, 6000, 18, hyk_liuliang)),
            int(k_value(4000, 6000, 46, hyk_liuliang)),
            k_value(4000, 6000, 4.54, hyk_liuliang),
            k_value(4000, 6000, 2.46, hyk_liuliang),
            k_value(4000, 6000, 2.09, hyk_liuliang),
        )

        if usetag:
            main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            '<span class="hn">' + str(int(k_value(4000, 6000, 70, hyk_liuliang))) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 6.18, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(int(k_value(4000, 6000, 273, hyk_liuliang))) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 24.85, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 110.29, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 70.81, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 140.87, hyk_liuliang)) + '</span>',
        ) + "山东省预计漫滩面积万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，需转移安置{}万人，就地或就近安置{}万人。".format(
            '<span class="hn">' + str(k_value(4000, 6000, 39.07, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(int(k_value(4000, 6000, 93, hyk_liuliang))) + '</span>',
            '<span class="hn">' + str(int(k_value(4000, 6000, 18, hyk_liuliang))) + '</span>',
            '<span class="hn">' + str(int(k_value(4000, 6000, 46, hyk_liuliang))) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 4.54, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 2.46, hyk_liuliang)) + '</span>',
            '<span class="hn">' + str(k_value(4000, 6000, 2.09, hyk_liuliang)) + '</span>',
        )

    elif hyk_liuliang <= 8000:
        main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(6000, 8000, 438, hyk_liuliang)),
            k_value(6000, 8000, 51.47, hyk_liuliang),
            int(k_value(6000, 8000, 280, hyk_liuliang)),
            k_value(6000, 8000, 27.07, hyk_liuliang),
            k_value(6000, 8000, 215.53, hyk_liuliang),
            k_value(6000, 8000, 152.85, hyk_liuliang),
            k_value(6000, 8000, 327.17, hyk_liuliang),
        ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，除东明县部分群众利用新建村台，东平县、平阴县、长清区部分群众利用山坡避洪外，需转移安置{}万人，就地或就近安置{}万人。".format(
            k_value(6000, 8000, 204.05, hyk_liuliang),
            k_value(6000, 8000, 134.34, hyk_liuliang),
            int(k_value(6000, 8000, 108, hyk_liuliang)),
            int(k_value(6000, 8000, 105, hyk_liuliang)),
            int(k_value(6000, 8000, 206, hyk_liuliang)),
            k_value(6000, 8000, 25.26, hyk_liuliang),
            k_value(6000, 8000, 5.70, hyk_liuliang),
            k_value(6000, 8000, 16.98, hyk_liuliang),
        )
        if usetag:
            main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
                '<span class="hn">' + str(int(k_value(6000, 8000, 438, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(int(k_value(6000, 8000, 51.47, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(int(k_value(6000, 8000, 280, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(6000, 8000, 27.07, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(6000, 8000, 215.53, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(6000, 8000, 152.85, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(6000, 8000, 327.17, hyk_liuliang)) + '</span>',
                ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，除东明县部分群众利用新建村台，东平县、平阴县、长清区部分群众利用山坡避洪外，需转移安置{}万人，就地或就近安置{}万人。".format(
                    '<span class="hn">' + str(k_value(6000, 8000, 204.05, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(6000, 8000, 134.34, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(int(k_value(6000, 8000, 108, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(6000, 8000, 105, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(6000, 8000, 206, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(k_value(6000, 8000, 25.26, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(6000, 8000, 5.70, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(6000, 8000, 16.98, hyk_liuliang)) + '</span>',
                    )

    elif hyk_liuliang <= 10000:
        main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(8000, 10000, 905, hyk_liuliang)),
            int(k_value(8000, 10000, 112.70, hyk_liuliang)),
            int(k_value(8000, 10000, 191, hyk_liuliang)),
            k_value(8000, 10000, 18.53, hyk_liuliang),
            k_value(8000, 10000, 323.22, hyk_liuliang),
            k_value(8000, 10000, 219.20, hyk_liuliang),
            k_value(8000, 10000, 467.43, hyk_liuliang),
        ) + "山东省预计黄河滩区全部漫滩，漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，除东平县、平阴县、长清区部分群众利用山坡避洪外，需转移安置{}万人，就地或就近安置{}万人。".format(
            k_value(8000, 10000, 228.35, hyk_liuliang),
            k_value(8000, 10000, 174.27, hyk_liuliang),
            int(k_value(8000, 10000, 109, hyk_liuliang)),
            int(k_value(8000, 10000, 222, hyk_liuliang)),
            int(k_value(8000, 10000, 161, hyk_liuliang)),
            k_value(8000, 10000, 31.42, hyk_liuliang),
            k_value(8000, 10000, 7.44, hyk_liuliang),
            k_value(8000, 10000, 22.63, hyk_liuliang),
        )

        if usetag:
            main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
                '<span class="hn">' + str(int(k_value(8000, 10000, 905, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(int(k_value(8000, 10000, 112.70, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(int(k_value(8000, 10000, 191, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(8000, 10000, 18.53, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(8000, 10000, 323.22, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(8000, 10000, 219.20, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(8000, 10000, 467.43, hyk_liuliang)) + '</span>',
                ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，除东平县、平阴县、长清区部分群众利用山坡避洪外，需转移安置{}万人，就地或就近安置{}万人。".format(
                    '<span class="hn">' + str(k_value(8000, 10000, 228.35, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(8000, 10000, 174.27, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(int(k_value(8000, 10000, 109, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(8000, 10000, 222, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(8000, 10000, 161, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(k_value(8000, 10000, 31.42, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(8000, 10000, 7.44, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(8000, 10000, 22.63, hyk_liuliang)) + '</span>',
                    )
    elif hyk_liuliang <= 12370:
        main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(10000, 12370, 1029, hyk_liuliang)),
            k_value(10000, 12370, 125.22, hyk_liuliang),
            int(k_value(10000, 12370, 80, hyk_liuliang)),
            k_value(10000, 12370, 6.97, hyk_liuliang),
            k_value(10000, 12370, 329.80, hyk_liuliang),
            k_value(10000, 12370, 223.09, hyk_liuliang),
            k_value(10000, 12370, 494.89, hyk_liuliang),
        ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，其中需转移安置{}万人，就地或就近安置{}万人。".format(
            k_value(10000, 12370, 234.71, hyk_liuliang),
            k_value(10000, 12370, 176.90, hyk_liuliang),
            int(k_value(10000, 12370, 109, hyk_liuliang)),
            int(k_value(10000, 12370, 243, hyk_liuliang)),
            int(k_value(10000, 12370, 157, hyk_liuliang)),
            k_value(10000, 12370, 31.68, hyk_liuliang),
            k_value(10000, 12370, 20.09, hyk_liuliang),
            k_value(10000, 12370, 11.59, hyk_liuliang),
        )

        if usetag:
            main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
                '<span class="hn">' + str(int(k_value(10000, 12370, 1029, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(10000, 12370, 125.22, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(int(k_value(10000, 12370, 80, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(10000, 12370, 6.97, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(10000, 12370, 329.80, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(10000, 12370, 223.09, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(10000, 12370, 494.89, hyk_liuliang)) + '</span>',
                ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，其中需转移安置{}万人，就地或就近安置{}万人。".format(
                    '<span class="hn">' + str(k_value(10000, 12370, 234.71, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(10000, 12370, 176.90, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(int(k_value(10000, 12370, 109, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(10000, 12370, 243, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(10000, 12370, 157, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(k_value(10000, 12370, 31.68, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(10000, 12370, 20.09, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(10000, 12370, 11.59, hyk_liuliang)) + '</span>',
                    )
            
    elif hyk_liuliang <= 15700:
        main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(12370, 15700, 1103, hyk_liuliang)),
            k_value(12370, 15700, 134.30, hyk_liuliang),
            int(k_value(12370, 15700, 48, hyk_liuliang)),
            k_value(12370, 15700, 3.99, hyk_liuliang),
            k_value(12370, 15700, 342.10, hyk_liuliang),
            k_value(12370, 15700, 234.10, hyk_liuliang),
            k_value(12370, 15700, 507.66, hyk_liuliang),
        ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，其中需转移安置{}万人，就地或就近安置{}万人。".format(
            k_value(12370, 15700, 234.71, hyk_liuliang),
            k_value(12370, 15700, 176.90, hyk_liuliang),
            int(k_value(12370, 15700, 109, hyk_liuliang)),
            int(k_value(12370, 15700, 243, hyk_liuliang)),
            int(k_value(12370, 15700, 157, hyk_liuliang)),
            k_value(12370, 15700, 31.68, hyk_liuliang),
            k_value(12370, 15700, 20.09, hyk_liuliang),
            k_value(12370, 15700, 11.59, hyk_liuliang),
        )

        if usetag:
            main_str = "河南省预计进水村庄{}个、人口{}万人，水围村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
                '<span class="hn">' + str(int(k_value(12370, 15700, 1103, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 134.30, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(int(k_value(12370, 15700, 48, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 3.99, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 342.10, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 234.10, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 507.66, hyk_liuliang)) + '</span>',
                ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，其中需转移安置{}万人，就地或就近安置{}万人。".format(
                    '<span class="hn">' + str(k_value(12370, 15700, 234.71, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(12370, 15700, 176.90, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(int(k_value(12370, 15700, 109, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(12370, 15700, 243, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(int(k_value(12370, 15700, 157, hyk_liuliang))) + '</span>',
                    '<span class="hn">' + str(k_value(12370, 15700, 31.68, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(12370, 15700, 20.09, hyk_liuliang)) + '</span>',
                    '<span class="hn">' + str(k_value(12370, 15700, 11.59, hyk_liuliang)) + '</span>',
                    )
            
    elif hyk_liuliang <= 22000:
        main_str = "河南省预计进水村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(12370, 15700, 1196, hyk_liuliang)),
            k_value(12370, 15700, 144.66, hyk_liuliang),
            k_value(12370, 15700, 365.00, hyk_liuliang),
            k_value(12370, 15700, 253.10, hyk_liuliang),
            k_value(12370, 15700, 529.20, hyk_liuliang),
        ) + "山东省预计漫滩面积234.71万亩，淹没耕地176.90万亩，109个滩区进水，243个自然村进水，157个自然村被水围困，涉及31.68万人，其中需转移安置20.09万人，就地或就近安置11.59万人。"
        if usetag:
            main_str = "河南省预计进水村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
                '<span class="hn">' + str(int(k_value(12370, 15700, 1196, hyk_liuliang))) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 144.66, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 365.00, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 253.10, hyk_liuliang)) + '</span>',
                '<span class="hn">' + str(k_value(12370, 15700, 529.20, hyk_liuliang)) + '</span>',
                ) + "山东省预计漫滩面积{}万亩，淹没耕地{}万亩，{}个滩区进水，{}个自然村进水，{}个自然村被水围困，涉及{}万人，其中需转移安置{}万人，就地或就近安置{}万人。".format(
                    '<span class="hn">' + str(234.71) + '</span>',
                    '<span class="hn">' + str(176.90) + '</span>',
                    '<span class="hn">' + str(109) + '</span>',
                    '<span class="hn">' + str(243) + '</span>',
                    '<span class="hn">' + str(157) + '</span>',
                    '<span class="hn">' + str(31.68) + '</span>',
                    '<span class="hn">' + str(20.09) + '</span>',
                    '<span class="hn">' + str(11.59) + '</span>',
                )
    else:
        main_str = "尚未制定超级特大洪水的滩区淹没计算方法。"
                    
    return {"result": main_str}

def smx_yujingdengji(lm_ll=None, tg_ll=None, hx_ll=None,):
    logger.debug("预警等级")

    lm_ll = lm_ll if lm_ll is not None else 0
    tg_ll = tg_ll if tg_ll is not None else 0
    hx_ll = hx_ll if hx_ll is not None else 0
    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑
    result = """按照《黄河防汛抗旱应急预案》，当前无预警"""
    if  lm_ll >= 18000 or tg_ll >= 15000 or hx_ll >= 8000:
        logger.debug("# 启动防汛一级应急响应")
        result = """启动防汛一级应急响应，响应行动如下：（1）局防指向水库防汛行政责任人、河南省防指及黄河防总办公室汇报雨情、水情、汛情、工情、险情等情况，请示由水库抢险指挥机构全面部署水库防汛应急相关工作。\n
        （2）水库抢险指挥机构指挥长或其委托人主持召开三门峡水库防汛抢险会商会，部署开展枢纽防汛运用措施，研究制定枢纽运用方案。\n
        （3）局防指指挥长到枢纽现场指挥。组织局防汛抢险专家等技术力量研究应急处置方案，局防指办及各单位、部门组织实施。机关部门相关岗位人员全部上岗到位。局防指办全员到岗，及时滚动以短信等方式向局防指成员发布水雨情、水库调度、险情等最新信息。\n
        （4）三门峡发电公司、水电公司、服务中心等单位所有相关岗位人员全部上岗到位。紧盯电厂厂房、供电点、防汛设备启闭机室以及防汛道路等重点区域，严防雨水正（倒）灌引发事故灾害；加强枢纽防汛设备与水工建筑物险工、险点等巡视检查，发现险情，立即组织抢险并按应急处置程序逐级上报。\n
        （5）局防指办按工作部署及时向有关各方汇报枢纽防汛运用、险情处置等情况。"""
    if  lm_ll >= 12000 or tg_ll >= 10000 or hx_ll >= 6000:
        logger.debug("# 启动防汛二级应急响应")
        result = """启动二级应急响应，响应行动如下：（1）局防指向水库防汛行政责任人、河南省防指及黄河防总办公室汇报雨情、水情、汛情、工情、险情等情况，请示由水库抢险指挥机构指导部署水库防汛应急相关工作。\n
        （2）局防指指挥长主持召开三门峡枢纽防汛会商会，落实水库抢险指挥机构工作部署。通报雨水情、工情、险情等重要预警信息，组织开展枢纽防汛运用措施，根据黄委等调度要求研究制定枢纽运用方案。\n
        （3）局防指常务副指挥长到枢纽现场指挥。组织局防汛抢险专家等技术力量研究应急处置方案，局防指办及各单位、部门组织实施。机关部门主要负责人到岗。局防指办值班实行双人双岗值班，根据情况增加值班人员，及时以短信等方式向局防指成员发布水雨情、水库调度等最新信息（每日 8 时、14 时、20 时）。防汛督察与宣传报道人员上岗。\n
        （4）三门峡发电公司、水电公司、服务中心等单位主要负责人到岗，做好协调与分级指挥工作。防汛抢险队员上岗待命。增加防汛电源、防汛物资、交通、后勤保障、电厂厂房防正（倒）灌、通信、网络、大坝安全监测等岗位人员。加强对所辖坝区工作、生活的低洼区域以及防汛道路的巡查，严防雨水正灌引发事故灾害；加强枢纽防汛设备与水工建筑物险工、险点等巡视检查，发现险情，立即组织抢险并按应急处置程序逐级上报。\n
        （5）局防指办按工作部署及时向有关各方汇报枢纽防汛运用、险情处置等情况。"""
    if  lm_ll >= 8000 or tg_ll >= 8000 or hx_ll >= 4000:
        # 启动防汛三级应急响应
        logger.debug("# 启动防汛三级应急响应")
        result = """启动三级应急响应，响应行动如下：（1）局防指常务副指挥长（或副指挥长）主持召开防汛会商会，安排部署枢纽防汛工作，并及时向指挥长汇报枢纽防汛运用情况。局防指成员参加会商。\n
        （2）根据会商意见，局防指向局属相关单位、部门发出通知，通报雨水情、工情、险情等重要预警信息，对枢纽防汛工作提出要求。\n
        （3）局防指办根据黄委等调度要求研究制定枢纽运用方案，经常务副指挥长批准后组织落实。局防指带班领导到枢纽现场指挥、带班。机关相关部门主要负责人到岗。局防指办值班实行双人双岗值班，根据情况增加值班人员，及时以短信等方式向局防指成员发布水雨情、水库调度等最新信息（每日 8 时、14 时、20 时）。\n
        （4）三门峡发电公司、水电公司、服务中心等单位主要负责人到岗，配合做好防汛会商、协调、部署与分级指挥工作。各单位防汛抢险队员待命。增加防汛电源、防汛物资、交通、后勤保障与电厂厂房防正（倒）灌、通信、网络等岗位人员，保障各系统可靠运转。\n
        （5）局防指办及时向三门峡市防指、河南省防指及黄河防总办公室报告启动响应及枢纽运用等情况。"""
    if  lm_ll >= 5000 or tg_ll >= 5000 or hx_ll >= 2500:
        # 启动防汛四级应急响应
        logger.debug("# 启动防汛四级应急响应")
        result = """启动四级应急响应，响应行动如下：（1）局防指办主任主持召开防汛会商会，安排部署枢纽防汛工作，并及时向带班领导、常务副指挥长汇报枢纽防汛运用情况。局防指成员单位派员参加会商。\n
        （2）根据会商意见，局防指向局属相关单位、部门发出通知，通报雨水情、工情、险情等重要预警信息，对枢纽防汛工作提出要求。\n
        （3）局防指办根据黄委等调度要求研究制定枢纽运用方案，经常务副指挥长批准后组织落实。局防指带班领导到枢纽现场指挥、带班。局防指办值班实行双人双岗值班，及时以短信等方式向局防指成员发布水雨情、水库调度等最新信息（每日 8 时、20 时）。\n
        （4）三门峡发电公司、水电公司、服务中心等单位分管负责人到岗，配合做好防汛会商、协调、部署与分级指挥工作。枢纽闸门启闭、防汛电源、通信、网络、交通等重要防汛岗位人员，按照防汛预案保障防汛系统可靠运转。\n
        （5）局防指办及时向三门峡市防指、河南省防指及黄河防总办公室报告启动响应及枢纽运用等情况。"""
    logger.debug("""预警等级: 按照《黄河防汛抗旱应急预案》，当前无预警""")
    return {"result": result}
def hh_yujingdengji(smx_sw=None, xld_sw=None, lh_sw=None, gx_sw=None,
                 hkc_sw=None, dph_sw=None,
                 knh_ll=None, lz_ll=None, szs_ll=None,
                 lm_ll=None, tg_ll=None, hx_ll=None,
                 hyk_ll=None, gc_ll=None, wl_ll=None,bms_ll=None,lmz_ll=None):
    """

    """
    logger.debug("预警等级")

    # 如果参数为 None，则默认为 0
    smx_sw = smx_sw if smx_sw is not None else 0
    xld_sw = xld_sw if xld_sw is not None else 0
    lh_sw = lh_sw if lh_sw is not None else 0
    gx_sw = gx_sw if gx_sw is not None else 0
    hkc_sw = hkc_sw if hkc_sw is not None else 0
    dph_sw = dph_sw if dph_sw is not None else 0

    knh_ll = knh_ll if knh_ll is not None else 0
    lz_ll = lz_ll if lz_ll is not None else 0
    szs_ll = szs_ll if szs_ll is not None else 0
    lm_ll = lm_ll if lm_ll is not None else 0
    tg_ll = tg_ll if tg_ll is not None else 0
    hx_ll = hx_ll if hx_ll is not None else 0
    hyk_ll = hyk_ll if hyk_ll is not None else 0
    gc_ll = gc_ll if gc_ll is not None else 0
    wl_ll = wl_ll if wl_ll is not None else 0
    bms_ll = bms_ll if bms_ll is not None else 0
    lmz_ll = lmz_ll if lmz_ll is not None else 0
    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑
    level = None
    result = """按照《黄河防汛抗旱应急预案》，当前无预警"""
    if (act_flag and lev == 'Ⅰ') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or xld_sw >= 275 or smx_sw >= 335 or knh_ll >= 5000 or lz_ll >= 6500 or szs_ll >= 5500 or lm_ll >= 18000 or tg_ll >= 15000 or hyk_ll >= 15000 or hx_ll >= 8000 or wl_ll >= 4000 or bms_ll>=6000 or lmz_ll>=5000:
        logger.debug("# 启动防汛一级应急响应")
        level = 1
        result = """按照《黄河防汛抗旱应急预案》，启动一级应急响应，响应行动如下：\n
        （1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。\n
        （2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛一级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导，动员社会力量支援黄河抗洪抢险救灾。\n
        （3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作，各职能组充实人员。黄委全体职工全力投入抗洪抢险工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 3 次，每日至少提供12 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖、北金堤滞洪区运用的分析研判；宣传组适时举行新闻发布会，向社会报道黄河抗洪抢险动态，做好新闻宣传工作。\n
        （4）黄河防总根据汛情需要，及时增派司局级领导带队的工作组、专家组赶赴现场，指导抗洪抢险救灾工作。\n
        （5）根据各地抗洪抢险需要，黄河防总按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险，必要时请求国家防总调动流域内外抢险队、物资支援黄河抗洪抢险。\n
        （6）有关省区防汛抗旱指挥机构的主要负责同志主持会商，动员部署防汛工作；按照权限组织调度水工程；根据预案转移安置危险地区群众，组织强化巡堤查险和堤防防守，及时控制险情；增派工作组、专家组赴一线指导防汛工作；受灾地区的各级防汛抗旱指挥机构负责人、成员单位负责人，应按照职责到分管的区域组织指挥防汛工作，或驻点具体帮助重灾区做好防汛工作；可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险；将工作情况上报省区人民政府及黄河防总。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期，动员一切社会力量投入黄河抗洪抢险"""
    elif (act_flag and lev == 'Ⅱ') or lh_sw >= 327.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 - 0.5 or gx_sw >= 547.39 or xld_sw >= 274 or smx_sw >= 335 or knh_ll >= 4000 or lz_ll >= 5000 or szs_ll >= 4000 or lm_ll >= 12000 or tg_ll >= 10000 or hyk_ll >= 8000 or hx_ll >= 6000 or wl_ll >= 3000 or bms_ll>=4000 or lmz_ll>=4000:
        logger.debug("# 启动防汛二级应急响应")
        level = 2
        result = """按照《黄河防汛抗旱应急预案》，启动二级应急响应，响应行动如下：\n
        （1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。\n
        （2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛二级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。\n
        （3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。黄委全体职工做好随时投入抗洪抢险工作的准备。\n
        （4）黄河防总实时掌握雨情、水情、汛情（凌情）、工情、险情、灾情动态。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 2 次，每日至少提供 6 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖滞洪区运用的分析研判；宣传组定期举行新闻发布会，向社会公布黄河抗洪抢险动态。\n
        （5）黄河防总办公室根据汛情需要，及时派出司局级领导带队的工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。\n
        （6）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。\n
        （7）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府主要负责同志、国家防总及黄河防总。按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期。"""
    elif (act_flag and lev == 'Ⅲ') or lh_sw >= 319.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 3000 or lz_ll >= 4000 or szs_ll >= 3000 or lm_ll >= 8000 or tg_ll >= 8000 or hyk_ll >= 6000 or hx_ll >= 4000 or wl_ll >= 2000 or bms_ll>=3000 or lmz_ll>=3000:
        # 启动防汛三级应急响应
        level= 3
        logger.debug("# 启动防汛三级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动三级应急响应，响应行动如下：\n
        （1）黄河防总秘书长主持防汛会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。\n
        （2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛三级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥、常务副总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。\n
        （3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 1 次，每日至少提供 3 次（8 时、14 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度；宣传组加强黄河抗洪抢险宣传。\n
        （4）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。黄委防汛物资、黄河机动抢险队支援抗洪抢险。\n
        （5）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。\n
        （6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府分管负责同志和黄河防总。可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。在省级主要媒体及新媒体平台发布防汛抗旱有关情况。"""
    elif (act_flag and lev == 'IV') or lh_sw >= 317.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 2500 or lz_ll >= 2500 or szs_ll >= 2000 or lm_ll >= 5000 or tg_ll >= 5000 or hyk_ll >= 4000 or hx_ll >= 2500 or wl_ll >= 1000 or bms_ll>=2000 or lmz_ll>=2000:
        # 启动防汛四级应急响应
        level = 4
        logger.debug("# 启动防汛四级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动四级应急响应，响应行动如下：\n
        （1）黄河防总秘书长主持会商，研究部署抗洪抢险工作，确定运行机制。响应期间，根据汛情发展变化，受黄河防总秘书长委托，可由黄河防总办公室副主任主持会商，并将情况报黄河防总秘书长。\n
        （2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛四级应急响应的命令及黄河汛情，对防汛工作提出要求，并向国家防办、水利部报告有关情况，必要时向黄河防总总指挥、常务副总指挥报告。\n
        （3）黄河防总办公室成员单位人员坚守工作岗位，加强防汛值班值守。按照黄委防御大洪水职责分工和机构设置，综合调度、水情测报和工情险情组等人员上岗到位。其余成员单位按照各自职责做好技术支撑、通信保障、后勤及交通保障，加强宣传报道。水情测报组及时分析天气形势并结合雨水情发展态势，做好雨情、水情、沙情的预测预报，加强与水利部信息中心、黄河流域气象中心、省区气象水文部门会商研判，每日至少制作发布气象水情预报 1 次，每日至少提供 2 次（8 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报。\n
        （4）黄委按照批准的洪水调度方案，结合当前汛情做好水库等水工程调度，监督指导地方水行政主管部门按照调度权限做好水工程调度。\n
        （5）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。\n
        （6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；按照预案做好辖区内巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，必要时请调解放军和武警部队、民兵参加重要堤段、重点工程的防守或突击抢险；派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府和黄河防总办公室。"""
    logger.debug("""预警等级: 按照《黄河防汛抗旱应急预案》，当前无预警""")
    return {"level":level,"result": result}

def ylh_yujingdengji(
                 bms_ll=None,
                 lm_ll=None,
                 hsg_ll=None):
    logger.debug("预警等级")
    """
    伊洛河防汛预警出发条件：
    bms_ll:白马寺流量
    lm_ll:龙门镇流量
    hsg_ll:黑石关流量
    """
    # 如果参数为 None，则默认为 0
    bms_ll = bms_ll if bms_ll is not None else 0
    lm_ll = lm_ll if lm_ll is not None else 0
    hsg_ll = hsg_ll if hsg_ll is not None else 0

    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑
    level = None
    result = """按照《河南省黄河流域伊洛河防洪预案》，当前无需采取防御措施"""
    if (act_flag and lev == 'Ⅰ') or bms_ll >= 4600 or lm_ll >= 4600 or hsg_ll >= 2050:
        logger.debug("# 启动防汛一级应急响应")
        level = 1
        result = """按照《河南省黄河流域伊洛河防洪预案》，响应行动如下：\n洛阳市、郑州市各级防汛指挥机构领导要坐阵指挥；\n军分区负责指挥驻军、基干民兵要要组成抢险突击队日夜坚守大堤，查险除险；防汛物资储备单位要保证抢险物资的及时供应；\n交通部门要组织车辆、人员抢运防汛物资；\n公安部门人员要维护秩序，物加强保卫，严厉打击破坏抗洪抢险的违法犯罪行为。\n若伊洛河上游仍有较大来水，洪水下泄不畅，水位继续上涨，危胁到偃师城区、大唐首阳山电厂和陇海铁路的安全或夹河滩防洪大堤全线危急时，报请上级防汛指挥部批准后，从伊河右堤顾县杨村段和洛河右堤岳滩村段爆破分洪，使用伊河右滩和伊洛河夹河滩滞洪。"""
    elif (act_flag and lev == 'Ⅱ') or bms_ll >= 4000 or lm_ll >= 3000 or hsg_ll >= 2050:
        logger.debug("# 启动防汛二级应急响应")
        level = 2
        result = """按照《河南省黄河流域伊洛河防洪预案》，响应行动如下：\n洛阳市、郑州市防指领导成员到所负责河道坐阵指挥抢险。\n
        伊洛河沿河县（市、区）防汛指挥机构领导要到辖区河段坐阵指挥巡查，发现问题及时抢护，确保防洪大堤不漫溢、不决口，保证洪水安全通过。\n
        军分区要调动驻地部队、基干民兵组成抢险突击队待命，随时准备参加抢险。\n
        偃师区、洛龙区、伊滨区、巩义市夹河滩区和沿河低洼村要组织群众向安全地带转移，并抓紧抢运粮食和贵重物品等，确保人民群众生命财产安全"""
    elif (act_flag and lev == 'Ⅲ') or bms_ll >= 3000 or lm_ll >= 2000 or hsg_ll >= 1500:
        # 启动防汛三级应急响应
        level= 3
        logger.debug("# 启动防汛三级应急响应")
        result = """按照《河南省黄河流域伊洛河防洪预案》，响应行动如下：\n沿河乡镇防汛抗旱指挥部组织防汛队伍上堤查验，防汛抢险物资运送到达险工地段、重点防守部位。\n
        洛阳市偃师区、伊滨区、洛龙区、瀍河区、老城区、西工区、涧西区、宜阳县、伊川县和郑州市巩义市等伊洛河沿岸和夹河滩地区乡镇（街道），抢险队伍要日夜坚守大堤，确保洪水不漫堤决口。\n
        偃师区岳滩、翟镇、顾县、洛龙区佃庄、伊滨区庞村等乡镇做好洪水影响区内群众转移准备工作。"""
    elif (act_flag and lev == 'IV') or bms_ll >= 2000 or lm_ll >= 1500:
        # 启动防汛四级应急响应
        level = 4
        logger.debug("# 启动防汛四级应急响应")
        result = """按照《河南省黄河流域伊洛河防洪预案》，响应行动如下：洛龙区、伊滨区、瀍河区沿河地势较低及偃师区、洛龙区伊洛河滩区镇（街道）、村（社区）领导干部和工程技术人员要立即进入各自的防汛岗位堤段，禁止无关人员在滩地逗留，停止一切滩地作业，在建施工项目人员、机械撤离河道；\n
        组织人员严密监视险工堤段险情变化，随时采取加固措施；专业队伍值守穿堤涵（管）闸工程，并听从防汛指挥部统一指挥，及时关闭闸门或封堵闸孔。 \n
        上游仍有大雨大汛时，要通知偃师区伊洛河滩区群众做好转移贵重物品的准备工作。"""
    logger.debug("""预警等级: 按照《河南省黄河流域伊洛河防洪预案》，当前无预警响应措施""")
    return {"level":level,"result": result}

def gx_yujingdengji(
                 ls_ll=None,
                 gx_sw=None):
    logger.debug("预警等级")
    """
    bms_ll:卢氏流量
    gx_sw:故县水位
    """
    # 如果参数为 None，则默认为 0


    ls_ll = ls_ll if ls_ll is not None else 0
    gx_sw = gx_sw if gx_sw is not None else 0

    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑
    level = None
    result = """按照《故县水库应急抢险预案》，当前无需采取防御措施"""
    if (act_flag and lev == 'Ⅰ') or ls_ll >= 11400 or gx_sw>547.39:
        logger.debug("# 启动防汛一级应急响应")
        level = 1
        result = """按照《故县水库应急抢险预案》，启动一级应急响应，响应行动如下：\n（1）洛阳市防汛指挥长主持召开防汛会商会议，洛阳市防指和故县局防指成员参加，部署防汛工作。\n
                （2）向上下游沿河市、县防汛指挥机构通报汛情，传达黄委调度指令，由当地防汛指挥机构启动响应的预案并做好抗洪防抢汛险及迁安救护工作。\n
                （3）密切监视汛情，做好汛情预测预报。\n
                （4）按时准确执行黄委调度指令。\n
                （5）工程管理分局应对坝体排水、漏水和渗水情况及时进行检查和观测，加强对排水设备的巡回检查和运行维护工作；对水工建筑物、大坝、437 泵房、下游左右岸护坡、危险段山体加强监测，对出现的问题及时上报局防汛指挥部，由故县局防指组织有关单位研究落实对策。\n
                （6）在必要时可向黄委请示水库降低水位运用。\n
                （7）将实施结果及时向黄委、洛阳市防指和三门峡局防指汇报。"""
    elif (act_flag and lev == 'Ⅱ') or ls_ll >= 7450 or gx_sw>543.04:
        logger.debug("# 启动防汛二级应急响应")
        level = 2
        result = """按照《故县水库应急抢险预案》，启动二级应急响应，响应行动如下：\n（1）洛阳市防汛副指挥长到场指导，故县局防指指挥长主持召开防汛会商会议，部署防汛工作。副指挥长、指挥部成员坚守岗位，抢险队集合待命。\n
                （2）通知洛阳市及下游沿河县级防汛指挥部做好相应准备。向洛宁、卢氏两县通报水情，由当地防汛指挥机构做好抗洪抢险及迁安救护工作。\n
                （3）严格执行上级调度指令，故县局防指办按照指令要求，根据泄水建筑物实际情况，制订泄流方式，报故县局防指审批后执行，同时通知洛阳市防指做好相应准备。\n
                （4）通知洛河发电公司启动相应预案，做好防汛应急保障。\n
                （5）将实施结果和淹没损失情况及时向黄委、洛阳市防指和三门峡局防指汇报。\n"""
    elif (act_flag and lev == 'Ⅲ') or ls_ll >= 4750 or gx_sw>533.64:
        # 启动防汛三级应急响应
        level= 3
        logger.debug("# 启动防汛三级应急响应")
        result = """按照《故县水库应急抢险预案》，启动三级应急响应，响应行动如下：\n（1）故县局防指副指挥长主持召开防汛会商会议，部署防汛工作。各级防汛相关工作人员须全部到岗待命，随时准备做好各种作业或操作。\n
                    （2）严格执行上级调度指令，故县局防指办按照指令要求，根据泄水建筑物实际情况，制订泄流方案，报故县局防指审批后执行，同时通知下游沿河市、县防汛指挥部做好相应准备。\n
                    （3）各防汛单位按照各自防汛职责立即开展工作，加强防汛督查工作。\n
                    （4）通知洛河发电公司启动相应预案，做好防汛应急保障。\n
                    （5）将实施结果及时向黄委、洛阳市防指和三门峡局防指汇报。\n"""
    elif (act_flag and lev == 'IV') or ls_ll >= 2430 or gx_sw>533.14:
        # 启动防汛四级应急响应
        level = 4
        logger.debug("# 启动防汛四级应急响应")
        result = """按照《故县水库应急抢险预案》，启动四级应急响应，响应行动如下：\n（1）故县局防指副指挥长主持召开防汛会商会议，部署防汛工作。\n
        （2）故县局防汛办公室值班人员密切关注天气、雨情、水情变化，做好雨水情滚动预报，加强与卢氏、灵口水文站的联系。\n
        （3）工程管理分局加强防汛设施、设备巡回检查维护工作，确保防汛设备正常运行。加强上坝公路滑坡巡查工作。\n
        （4）库区管理分局密切关注库区水情变化和船只安全管理工作，加强库区周边巡逻巡查。\n
        （5）严格执行上级调度指令，故县局防指办按照指令要求，根据泄水建筑物实际情况，制订泄流方案，报故县局防指审批后执行，同时通知下游沿河市、县防汛指挥部做好相应准备。\n
        （6）通知洛河发电公司做好交通、通信、生活区地质灾害及防汛物资等后勤保障工作。\n
        （7）将实施结果及时向黄委、洛阳市防指和三门峡局防指汇报。\n
        """
    logger.debug("""预警等级: 按照《故县水库应急抢险预案》，当前无预警""")
    return {"level":level,"result": result}

def lh_yujingdengji(
                 lh_ll=None,
                 lh_sw=None):
    logger.debug("预警等级")
    """
    lh_ll:陆浑水库下泄流量
    lh_sw:故县水位
    """
    # 如果参数为 None，则默认为 0

    lh_ll =  lh_ll if  lh_ll is not None else 0
    lh_sw = lh_sw if lh_sw is not None else 0

    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑
    level = None
    result = """按照《2024陆浑水库防汛抢险应急预案》，当前无需采取防御措施"""
    if (act_flag and lev == 'Ⅰ') or lh_ll >= 5622 or lh_sw > 327.5:
        logger.debug("# 启动防汛一级应急响应")
        level = 1
        result = """按照《2024陆浑水库防汛抢险应急预案》，启动一级应急响应，响应行动如下：\n（（1）水库防汛指挥部指挥长（洛阳市主管领导）主持会商，水库防指各成员单位派人员参加，做出相应工作部署，在1小时内将情况上报洛阳市主要领导、黄河防总、省防指、省水利厅、省水文水资源中心、洛阳市防指，通知水库防指各成员单位按照职责分工，做好有关工作；\n
        （2）水库防办应密切监视突发事件变化情况，做好预测预报工作；\n
        （3）水库防办应加强对水库重点部位和重要基础设施的安全保卫，做好反恐工作；\n
        （4）各抢险队伍按照《陆浑水库防汛抢险措施和兵力部署方案》全力抢险；\n
        （5）水库防指通知洛阳市防指做好人员转工作。\n
        抢险措施：超标准洪水\n
        （1）当水位上升至326.91m，且仍有上涨趋势时，务必在6小时之内，将大坝东上游侧下坝梯口和西坝头防浪墙尽头处的路口，用麻袋装土堆垒至防浪墙顶高程。\n
        （2）当库水位上升至330.63m仍有上涨趋势时，务必在6小时之内，将大坝桩号0+271.4～1+170每隔4m在防浪墙后用麻袋装土做成1m宽的戗台，堆垒至防浪墙顶高程（334.7m），再用圆木杆（小头直径不小于13cm，长不小于3.8m）棚在戗台上。\n
        （3）当库水位上升至333.37m且仍有上涨趋势时，务必在8小时之内，将大坝沿防浪墙统长，在334.7m的基础上，再用编织袋装土加高130cm，使堰顶高程达到336m。\n     
        抢险措施：坝基渗流破坏发生管涌时\n
        （1）报告上级防止、全开闸门泄水，最大限度降低水位。\n
        （2）在采取上述措施的同时进行全力羌胡，抢护中分两步同时进行，第一步应派监测人员查探坝前水情，确定管涌进口位置，位置确定后迅速用装土麻袋向漏水点投抛，如果投抛后下游翻泉有减弱的情况，证明上游止漏有效，直至漏量较小或不漏为止。第二步与第一步同时进行，对下游冒水点区实施压坝脚做反滤处理，首先在翻泉点、区用麻袋或编织袋装砂料无缝密铺，压住漏水点、区，压铺砂袋厚度应不小于30cm，范围为漏水点、区边界线以外不小于3m的区域全部施铺；铺设砂袋的实施过程按流水作业法用麻袋或编织袋装碎石子无缝密铺压住砂袋，厚度不小于30cm，范围同砂袋。碎石子袋压好后，亦按流水线法在碎石子袋上加压大块石一层，如果压不住，应立即加大块石厚度，直至压住为止。 """
    elif (act_flag and lev == 'Ⅱ') or lh_ll >= 3240 or lh_sw>324.95:
        logger.debug("# 启动防汛二级应急响应")
        level = 2
        result = """按照《2024陆浑水库防汛抢险应急预案》，启动二级应急响应，响应行动如下：\n（1）水库防汛指挥部指挥长（洛阳市主管领导）主持会商，水库防指各成员单位派人员参加，做出相应工作部署，在1小时内将情况上报洛阳市主要领导、黄河防总、省防指、省水利厅、省水文水资源中心、洛阳市防指，通知水库防指各成员单位按照职责分工，做好有关工作；\n
        （2）水库防办应密切监视突发事件变化情况，做好预测预报工作；\n
        （3）抢险队伍按照《陆浑水库防汛抢险措施和兵力部署方案》全力抢险，抢险后备队人员进入现场待命；\n
        （4）水库防指通知洛阳市防指做好人员转移工作。\n
        抢险措施：上游坝坡发生滑坡\n
        （1）滑坡发生后，必须立即抢护，以免风浪冲击破坏斜墙。\n
        （2）在抢护过程中，应严禁人为对粘土斜墙表面造成损伤，不得在斜墙表面打桩、修路修阶、人行践踏、抛料滚石等。\n
        （3）抢护方法：第一，用麻袋或编织袋装砂料从滑坡部位的左右两侧沿斜墙面实施无缝密铺，向中心合拢，在铺垫过程中，若遇散落在斜墙面上的砼块或较大块石可渐次清除，这样可避免人为踏伤斜墙表面。砂袋铺垫厚度应不小于30cm。第二，采用流水做业法再铺垫一层袋装碎石子，厚度亦不小于30cm。第三，紧接着在碎石子袋上迅速压砌大块石，也可用砼块体，严防风浪冲击破坏反滤料层。\n
        （4）在遇到特别紧急，来不及采用上述方法抢护时，可以用透水土工布铺于滑坡表面，周围用大石块或砂石袋压紧，洪水退后再处理。\n
        （5）抢护完成后应专人监视，险情过后拆除临时抢护物并按原设计及时修复。\n
        抢险措施：泄水闸门突发性故障\n
        （1）电源中断时的应急处理\n
        在闸门启闭中，电源供给优先顺序为：\n
        ①水库电站自发电供电；\n
        ②备用的640千瓦柴油发电机组供电；\n
        ③国家电网系统电供电。\n
        （2）闸门机电设施突发性故障发生时的应急处理\n
        ①若溢洪道、泄洪洞闸门机电设施突发故障启闭受阻，因启闭力巨大，均无手摇机构，可按下述应急措施处理：其一，立即请示上级防指使灌溉洞提前投入泄洪，减少一部分库水位上涨的压力，同时组织机电工作人员或聘请专家抢修，使其恢复启用；其二，库水位上涨仍有可能造成漫坝威胁时，应按超标准洪水抢险方案进行抢护。\n
        ②若灌溉洞、输水洞闸门机电设施突发故障启闭受阻，应迅速组织机电工作人员或聘请专家进行抢修，使其恢复启用。\n"""
    elif (act_flag and lev == 'Ⅲ') or lh_ll >= 2299 or lh_sw>319.5:
        # 启动防汛三级应急响应
        level= 3
        logger.debug("# 启动防汛三级应急响应")
        result = """按照《2024陆浑水库防汛抢险应急预案》，启动三级应急响应，响应行动如下：\n
        （1）水库防指常务副指挥长（主任）主持会商，做出相应工作部署，在2小时内将情况上报水库防指指挥长（洛阳市主管领导）、黄河防总、省防指、省水利厅、省水文水资源中心、洛阳市防指，通知水库防指各成员单位按照职责分工，做好有关工作；\n
        （2）应急抢险队伍、负有特定职责的人员进入现场待命，动员后备人员做好参加抢险和处置工作的准备；\n
        （3）调集应急抢险所需材料、设备、工具，确保其随时可以投入正常使用；\n
        （4）水库防指通知洛阳市防指做好人员转移工作。\n
        抢险措施：上游坝坡发生滑坡\n
        （1）滑坡发生后，必须立即抢护，以免风浪冲击破坏斜墙。\n
        （2）在抢护过程中，应严禁人为对粘土斜墙表面造成损伤，不得在斜墙表面打桩、修路修阶、人行践踏、抛料滚石等。\n
        （3）抢护方法：第一，用麻袋或编织袋装砂料从滑坡部位的左右两侧沿斜墙面实施无缝密铺，向中心合拢，在铺垫过程中，若遇散落在斜墙面上的砼块或较大块石可渐次清除，这样可避免人为踏伤斜墙表面。砂袋铺垫厚度应不小于30cm。第二，采用流水做业法再铺垫一层袋装碎石子，厚度亦不小于30cm。第三，紧接着在碎石子袋上迅速压砌大块石，也可用砼块体，严防风浪冲击破坏反滤料层。\n
        （4）在遇到特别紧急，来不及采用上述方法抢护时，可以用透水土工布铺于滑坡表面，周围用大石块或砂石袋压紧，洪水退后再处理。\n
        （5）抢护完成后应专人监视，险情过后拆除临时抢护物并按原设计及时修复。"""
    elif (act_flag and lev == 'IV') or lh_ll >= 1000 or lh_sw>317:
        # 启动防汛四级应急响应
        level = 4
        logger.debug("# 启动防汛四级应急响应")
        result = """按照《2024陆浑水库防汛抢险应急预案》，启动四级应急响应，响应行动如下：（1）陆浑水库防汛指挥部常务副指挥长（主任）主持会商，做出相应工作部署，在2小时内将情况上报陆浑水库防汛指挥部指挥长（洛阳市主管领导）、黄河防总、省防指、省水利厅、省水文水资源中心、洛阳市防指，加强对水库的监测巡查；\n
        （2）水库防办应密切关注雨水情、工情、水质等的变化情况；\n
        （3）水库防指各成员单位应按照职责分工，做好有关工作；\n
        （4）水库防指通知洛阳市防指做好人员转移工作。\n
        抢险措施：临水崩塌\n
        （1）临水崩塌险情可能发生的部位\n
        机电管理中心建在弃垫的虚土区，如遇到高水位运用时，受风浪的冲击很可能造成院南填土坡面大量塌方，将危及机组安全。\n
        （2）抢护原则\n
        抢护原则:缓流消浪，增强抗冲能力；不要在坡面、坡顶堆放重物或打桩，以免加快崩塌；对淘刷滑动引起的险情，要先稳定坡脚，再处理岸坡。\n
        （3）抢护方法\n
        ①挂柳挂枕\n选择枝繁叶茂的柳树头，将根部系在岸坡顶部的木桩上，在树梢枝杈上捆扎块石，顺坡推入水中消浪，树颗间距和悬挂深度要根据流势和崩塌程度而定，也可将柳树头的根部悬挂大石块或土袋固定。然后按照由深到浅的顺序依次抛沉。还可用粗稍料，捆成直径0.5～0.8m，长6～8m的稍枕，两端用绳子系于坡顶的木桩上，推入水中消浪。风浪较大时，可将稍枕连起来，做成枕排防浪。\n
       ②竹木排防浪\n当水库风浪较大时，可将竹木条分层叠扎成竹木排，用绳拴在坡顶的木桩上，同时，排下坠一块石或土袋，以稳定和调整排位。排体和坡体之间，要有一定的距离，以免撞击坡体。排体较大时可抛铁锚定位。\n
       ③护脚固基\n临水护脚固基，最常用的办法是散抛块石。对于水深流急的抢护，可用铅丝笼、竹笼、柳条笼装石抛投。\n
       ④土工织物防冲\n先将坡面进行平整和清理，把拼好的土工布或篷布铺在平整好的坡面上，膜布高出洪水位，并在膜布上压盖砼块或土袋，以抵抗风浪冲刷。"""
    logger.debug("""预警等级: 按照《2024陆浑水库防汛抢险应急预案》，当前无预警""")
    return {"level":level,"result": result}

def sx_yujingdengji(lh_sw=None):
    logger.debug("预警等级")
    """
    嵩县预警等级
    lh_ll:陆浑水库下泄流量
    lh_sw:故县水位
    """
    # 如果参数为 None，则默认为 0

    lh_sw = lh_sw if lh_sw is not None else 0

    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑
    level= None
    result = """"""
    if (act_flag and lev == 'Ⅰ') or 321.5 < lh_sw <=323:
        level = 1
        result = """按照《嵩县陆浑水库汛期高水位应急预案》，人员转移安置措施如下：\n
        当库水位超过兴利水位（319.5m）并有持续上涨趋势时由陆浑水库防办提前向嵩县防办发出转移预警通知，由嵩县防办向相关部门发布转移指令，组织本辖区危险区域人员，按照本预案转移安置。共需转移饭坡镇和陆浑镇 2 个乡镇20 个村庄的 199 户，780 人；共淹没 1053 间房屋、13952亩耕地、472 亩林地、76 亩果园、50 眼机井、3 个提灌站。
        """
    elif (act_flag and lev == 'Ⅱ') or 319.5 < lh_sw <=321.5:
        level = 2
        result = """按照《嵩县陆浑水库汛期高水位应急预案》，人员转移安置措施如下：\n
        当库水位超过二十年一遇洪水位（321.5m）并有持续上涨趋势时，由陆浑水库防办提前向嵩县防办发出转移预警通知，由嵩县防办向相关部门发布转移指令，组织本辖区危险区域人员，按照本预案转移安置.在蓄洪限制水位 323 米以下共需转移饭坡镇和陆浑镇 2 个乡镇、20 个村庄的 618户，2397 人；共淹没3037 间房屋、16776 亩耕地、1014.5亩林地、211 亩果园、101 眼机井、6 个提灌站。
                    """
    elif (act_flag and lev == 'Ⅲ') or 323 < lh_sw <=325:
        level = 3
        result = """按照《嵩县陆浑水库汛期高水位应急预案》，人员转移安置措施如下：\n
                当库水位超过蓄洪限制水位（323.0m）并有持续上涨趋势时，由陆浑水库防办提前向嵩县防办发出转移预警通知，由嵩县防办向相关部门发布转移指令，组织本辖区危险区域人员，按照本预案转移安置.在百年一遇洪水位 325.0 米以下，共需转移饭坡、陆浑、城关 3 个乡镇 27 个村庄的9412 户，51440 人；共淹没 37460 间房屋、18225 亩耕地、1557.5 亩林地、316亩果园、135 眼机井、8 个提灌站。"""
    elif (act_flag and lev == 'IV') or 325 < lh_sw <=327.5:
        level = 4
        result = """按照《嵩县陆浑水库汛期高水位应急预案》，人员转移安置措施如下：\n
                    当库水位超过百年一遇洪水位（325.0m）并有持续上涨趋势时，由陆浑水库防办提前向嵩县防办发出转移预警通知，由嵩县防办向相关部门发布转移指令，组织本辖区危险区域人员，按照本预案转移安置.在设计洪水位 327.5 米以下，共需转移饭坡、陆浑、城关和纸房 4 个乡镇 32 个村庄的 24145 户，112064人；共淹没 81303 间房屋、21034 亩耕地、2982.5 亩林地、601 亩果园、187 眼机井、10 个提灌站。"""
    elif (act_flag and lev == 'V') or 327.5 < lh_sw <=331.8:
        level = 5
        result = """按照《嵩县陆浑水库汛期高水位应急预案》，人员转移安置措施如下：\n
                   当库水位超过设计洪水位（327.5m）并有持续上涨趋势时，由陆浑水库防办提前向嵩县防办发出转移预警通知，由嵩县防办向相关部门发布转移指令，组织本辖区危险区域人员，按照本预案转移安置。在校核洪水位 331.8 米以下，共需转移饭坡、陆浑、城关、纸房和何村共 5 个乡镇 35 个村庄的 39047户，181285 人；共淹没 133186 间房屋、42 个窑洞、22874亩耕地、3856.5 亩林地、1191 亩果园、267 眼机井、12个提灌站。 """
    logger.debug("""预警等级: 按照《2024陆浑水库防汛抢险应急预案》，当前无预警""")
    return {"level":level,"result": result}

# lh_res = lh_yujingdengji(lh_ll=5622)
# print(f"预警等级: {lh_res['level']}")  # 输出: 预警等级: 1
# print(f"响应措施: {lh_res['result'][:100]}...")  # 输出前100字符
# hh_res = hh_yujingdengji(lh_sw=317.5)
# print(f"预警等级: {hh_res['level']}")  # 输出: 预警等级: 1
# print(f"响应措施: {hh_res['result'][:100]}...")  #
# ylh_res = ylh_yujingdengji(bms_ll=4000)
# print(f"预警等级: {ylh_res['level']}")  # 输出: 预警等级: 1
# print(f"响应措施: {ylh_res['result'][:100]}...")  #
# gx_res = gx_yujingdengji(ls_ll=7450)
# print(f"预警等级: {gx_res['level']}")  # 输出: 预警等级: 1
# print(f"响应措施: {gx_res['result'][:100]}...")  #
# sx_ydcs = sx_yujingdengji(lh_sw=325)["result"]
# print(f"响应措施: {sx_ydcs}...")
