def yujingdengji(smx_sw=None, xld_sw=None, lh_sw=None, gx_sw=None,
                 hkc_sw=None, dph_sw=None,
                 knh_ll=None, lz_ll=None, szs_ll=None,
                 lm_ll=None, tg_ll=None, hx_ll=None,
                 hyk_ll=None, gc_ll=None, wl_ll=None):
    print("预警等级")

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
    act_flag, lev = None, None  # 这里可以加入其他的函数逻辑

    result = """按照《黄河防汛抗旱应急预案》，当前无预警"""
    if (act_flag and lev == 'Ⅰ') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or xld_sw >= 275 or smx_sw >= 335 or knh_ll >= 5000 or lz_ll >= 6500 or szs_ll >= 5500 or lm_ll >= 18000 or tg_ll >= 15000 or hyk_ll >= 15000 or hx_ll >= 8000 or wl_ll >= 4000:
        print("# 启动防汛一级应急响应")
        retsult = """按照《黄河防汛抗旱应急预案》，启动一级应急响应，响应行动如下：（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛一级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导，动员社会力量支援黄河抗洪抢险救灾。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作，各职能组充实人员。黄委全体职工全力投入抗洪抢险工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 3 次，每日至少提供12 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖、北金堤滞洪区运用的分析研判；宣传组适时举行新闻发布会，向社会报道黄河抗洪抢险动态，做好新闻宣传工作。（4）黄河防总根据汛情需要，及时增派司局级领导带队的工作组、专家组赶赴现场，指导抗洪抢险救灾工作。（5）根据各地抗洪抢险需要，黄河防总按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险，必要时请求国家防总调动流域内外抢险队、物资支援黄河抗洪抢险。（6）有关省区防汛抗旱指挥机构的主要负责同志主持会商，动员部署防汛工作；按照权限组织调度水工程；根据预案转移安置危险地区群众，组织强化巡堤查险和堤防防守，及时控制险情；增派工作组、专家组赴一线指导防汛工作；受灾地区的各级防汛抗旱指挥机构负责人、成员单位负责人，应按照职责到分管的区域组织指挥防汛工作，或驻点具体帮助重灾区做好防汛工作；可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险；将工作情况上报省区人民政府及黄河防总。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期，动员一切社会力量投入黄河抗洪抢险"""
    if (act_flag and lev == 'Ⅱ') or lh_sw >= 327.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 - 0.5 or gx_sw >= 547.39 or xld_sw >= 274 or smx_sw >= 335 or knh_ll >= 4000 or lz_ll >= 5000 or szs_ll >= 4000 or lm_ll >= 12000 or tg_ll >= 10000 or hyk_ll >= 8000 or hx_ll >= 6000 or wl_ll >= 3000:
        print("# 启动防汛二级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动二级应急响应，响应行动如下：（1）黄河防总总指挥或常务副总指挥坐镇指挥黄河抗洪工作，主持抗洪抢险会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛二级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。黄委全体职工做好随时投入抗洪抢险工作的准备。（4）黄河防总实时掌握雨情、水情、汛情（凌情）、工情、险情、灾情动态。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 2 次，每日至少提供 6 次干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度和东平湖滞洪区运用的分析研判；宣传组定期举行新闻发布会，向社会公布黄河抗洪抢险动态。（5）黄河防总办公室根据汛情需要，及时派出司局级领导带队的工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（7）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府主要负责同志、国家防总及黄河防总。按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。根据汛情，相关县级以上人民政府防汛抗旱指挥部宣布进入紧急防汛期。"""
    if (act_flag and lev == 'Ⅲ') or lh_sw >= 319.5 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 3000 or lz_ll >= 4000 or szs_ll >= 3000 or lm_ll >= 8000 or tg_ll >= 8000 or hyk_ll >= 6000 or hx_ll >= 4000 or wl_ll >= 2000:
        # 启动防汛三级应急响应
        print("# 启动防汛三级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动三级应急响应，响应行动如下：（1）黄河防总秘书长主持防汛会商会，研究部署抗洪抢险工作。视情与相关省区进行异地会商。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛三级应急响应的命令及黄河汛情，对防汛工作提出要求，并向黄河防总总指挥、常务副总指挥报告。黄河防总向国家防总、水利部报告有关情况，为国家防总和水利部提供调度参谋意见，请求加强对黄河抗洪抢险指导。（3）黄河防总办公室各成员单位按照黄委防御大洪水职责分工和机构设置上岗到位，全面开展工作。水情测报组滚动进行洪水预测预报，每日至少制作发布气象水情预报 1 次，每日至少提供 3 次（8 时、14 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报；综合调度组根据预报滚动计算水利工程调度方案，做好干流及重要支流水库调度；宣传组加强黄河抗洪抢险宣传。（4）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。黄委防汛物资、黄河机动抢险队支援抗洪抢险。（5）根据各地抗洪抢险需要，黄河防总办公室按程序调度黄委防汛物资、黄河机动抢险队支援抗洪抢险。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；根据预案做好巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府分管负责同志和黄河防总。可按照预案和程序适时请调人民解放军和武警部队支援黄河抗洪抢险。在省级主要媒体及新媒体平台发布防汛抗旱有关情况。"""
    if (act_flag and lev == 'IV') or lh_sw >= 331.8 or hkc_sw >= 285.43 or dph_sw >= 43.22 or gx_sw >= 549.86 or smx_sw >= 335 or knh_ll >= 2500 or lz_ll >= 2500 or szs_ll >= 2000 or lm_ll >= 5000 or tg_ll >= 5000 or hyk_ll >= 4000 or hx_ll >= 2500 or wl_ll >= 1000:
        # 启动防汛四级应急响应
        print("# 启动防汛四级应急响应")
        result = """按照《黄河防汛抗旱应急预案》，启动四级应急响应，响应行动如下：（1）黄河防总秘书长主持会商，研究部署抗洪抢险工作，确定运行机制。响应期间，根据汛情发展变化，受黄河防总秘书长委托，可由黄河防总办公室副主任主持会商，并将情况报黄河防总秘书长。（2）根据会商意见，黄河防总办公室向相关省区防指通报关于启动防汛四级应急响应的命令及黄河汛情，对防汛工作提出要求，并向国家防办、水利部报告有关情况，必要时向黄河防总总指挥、常务副总指挥报告。（3）黄河防总办公室成员单位人员坚守工作岗位，加强防汛值班值守。按照黄委防御大洪水职责分工和机构设置，综合调度、水情测报和工情险情组等人员上岗到位。其余成员单位按照各自职责做好技术支撑、通信保障、后勤及交通保障，加强宣传报道。水情测报组及时分析天气形势并结合雨水情发展态势，做好雨情、水情、沙情的预测预报，加强与水利部信息中心、黄河流域气象中心、省区气象水文部门会商研判，每日至少制作发布气象水情预报 1 次，每日至少提供 2 次（8 时、20 时）干支流重要测站监测信息，情况紧急时根据需要加密测报。（4）黄委按照批准的洪水调度方案，结合当前汛情做好水库等水工程调度，监督指导地方水行政主管部门按照调度权限做好水工程调度。（5）黄河防总办公室根据汛情需要，及时派出工作组、专家组赶赴现场，检查、指导抗洪抢险救灾工作，核实汛情灾情。（6）有关省区防汛抗旱指挥机构负责同志主持会商，具体安排防汛工作；按照权限组织调度水工程；按照预案做好辖区内巡堤查险、抗洪抢险、群众转移安置等抗洪救灾工作，必要时请调解放军和武警部队、民兵参加重要堤段、重点工程的防守或突击抢险；派出工作组、专家组赴一线指导防汛工作；将防汛工作情况上报省级人民政府和黄河防总办公室。"""
    print("""预警等级: 按照《黄河防汛抗旱应急预案》，当前无预警""")
    return {"result": result}


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


def xld_sk(xld_sw: int = None, hyk_liuliang: int = None, tongguan_liuliang: int = None):
    xld_sw = xld_sw if xld_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0
    tongguan_liuliang = tongguan_liuliang if tongguan_liuliang is not None else 0

    rate_p = float(tongguan_liuliang) / (float(hyk_liuliang) + 0.001)
    print("小浪底SK", hyk_liuliang, tongguan_liuliang, xld_sw)
    """
    小浪底库
    :return: dict
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
    陆浑水库
    :return: dict
    """
    lh_sw = lh_sw if lh_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    print("陆浑水库SK", hyk_liuliang, lh_sw)

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
    故县水库
    :return: dict
    """
    gx_sw = gx_sw if gx_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    print("故县SK", hyk_liuliang, gx_sw)

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
    河口村水库
    :return: dict
    """
    hkc_sw = hkc_sw if hkc_sw is not None else 0
    hyk_liuliang = hyk_liuliang if hyk_liuliang is not None else 0

    print("河口村SK", hyk_liuliang, hkc_sw)

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

def tanquyanmo(hyk_liuliang):
    """
    滩区淹没（参数【花园口流量】）
    :return: dict
    """
    print("滩区淹没（参数【花园口流量】）")

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
    elif hyk_liuliang <= 22000:
        main_str = "河南省预计进水村庄{}个、人口{}万人，淹没滩地{}万亩，淹没耕地{}万亩，经济损失{}亿元；".format(
            int(k_value(12370, 15700, 1196, hyk_liuliang)),
            k_value(12370, 15700, 144.66, hyk_liuliang),
            k_value(12370, 15700, 365.00, hyk_liuliang),
            k_value(12370, 15700, 253.10, hyk_liuliang),
            k_value(12370, 15700, 529.20, hyk_liuliang),
        ) + "山东省预计漫滩面积234.71万亩，淹没耕地176.90万亩，109个滩区进水，243个自然村进水，157个自然村被水围困，涉及31.68万人，其中需转移安置20.09万人，就地或就近安置11.59万人。"

    return {"result": main_str}