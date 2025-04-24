import requests
#from yunheKGPro.settings import config
import requests
from datetime import datetime, timedelta
import json
from xml.etree import ElementTree
BASE_API_URL= "http://wt.hxyai.cn/fx/"#"http://10.4.158.35:8070/"
def get_rainfall_data_hour(basin=None, start_time=None, end_time=None):
    """
    获取实时雨量数据（带完整错误处理和JWT鉴权）

    参数:
        basin: 流域编码 (如"RH01")
        start_time: 开始时间 (如"2024-03-01 08:00:00")
        end_time: 结束时间 (如"2024-03-02 08:00:00")

    返回:
        (status_code, response_data) 元组
    """
    # 构造请求参数
    params = {}
    if basin:
        params["stcd"] = basin
    if start_time:
        params["startDate"] = start_time
    if end_time:
        params["endDate"] = end_time

    try:
        # 使用提供的JWT token
        auth_token = oauth_login()

        # 添加超时和请求头
        response = requests.get(
            url=f"{BASE_API_URL}/rainfall/hourrth/getRainfall",
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


def get_rainfall_data_day(auth_token,basin=None, start_time=None, end_time=None):
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
        auth_token = auth_token#oauth_login()

        # 添加超时和请求头
        response = requests.get(
            url=f"{BASE_API_URL}/rainfall/dayrt/getRainfall",
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


def generate_rainfall_report_v1(response_data):
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


def generate_rainfall_report(response_data):
    """
    生成降雨量报告文本(版本1)
    按照新的规则生成降雨报告:
    1. 优先判断大部降雨(≥50%站点)
    2. 其次判断局部降雨(≥20%站点)
    3. 再次判断个别地区降雨(>0%站点)
    4. 最后判断无降雨

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

    # 统计降雨等级和站点总数
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
    total_stations = len(yiluo_stations)
    rain_stations = 0  # 有降雨的站点数

    for station in yiluo_stations:
        rf = station['rf']

        if rf == 0:
            continue

        rain_stations += 1

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
    if rain_stations == 0:
        today = datetime.now()
        return f"{today.month}月{today.day}日，伊洛河流域无降雨"

    # 计算各雨型的站点比例
    ratios = {
        '小雨': rainfall_stats['小雨'] / total_stations,
        '中雨': rainfall_stats['中雨'] / total_stations,
        '大雨': rainfall_stats['大雨'] / total_stations,
        '暴雨': rainfall_stats['暴雨'] / total_stations,
        '大暴雨': rainfall_stats['大暴雨'] / total_stations,
        '特大暴雨': rainfall_stats['特大暴雨'] / total_stations
    }

    # 生成报告文本
    today = datetime.now()
    report_parts = [f"{today.month}月{today.day}日，伊洛河流域"]

    # 判断降雨范围
    # 1. 优先判断大部降雨(≥50%)
    # 大部暴雨
    if ratios['暴雨'] >= 0.5:
        report_parts.append("大部地区降暴雨")
    # 大部大雨
    elif ratios['大雨'] >= 0.5:
        report_parts.append("大部地区降大雨")
    # 大部中雨
    elif ratios['中雨'] >= 0.5:
        report_parts.append("大部地区降中雨")
    # 大部小雨
    elif ratios['小雨'] >= 0.5:
        report_parts.append("大部地区降小雨")
    # 大部大到暴雨
    elif (ratios['大雨'] + ratios['暴雨']) >= 0.5:
        report_parts.append("大部地区降大到暴雨")
    # 大部中到大雨
    elif (ratios['中雨'] + ratios['大雨']) >= 0.5:
        report_parts.append("大部地区降中到大雨")
    # 大部小到中雨
    elif (ratios['小雨'] + ratios['中雨']) >= 0.5:
        report_parts.append("大部地区降小到中雨")

    # 2. 其次判断局部降雨(≥20%)
    elif ratios['暴雨'] >= 0.2:
        report_parts.append("局部地区降暴雨")
    elif ratios['大雨'] >= 0.2:
        report_parts.append("局部地区降大雨")
    elif ratios['中雨'] >= 0.2:
        report_parts.append("局部地区降中雨")
    elif ratios['小雨'] >= 0.2:
        report_parts.append("局部地区降小雨")
    elif (ratios['大雨'] + ratios['暴雨']) >= 0.2:
        report_parts.append("局部地区降大到暴雨")
    elif (ratios['中雨'] + ratios['大雨']) >= 0.2:
        report_parts.append("局部地区降中到大雨")
    elif (ratios['小雨'] + ratios['中雨']) >= 0.2:
        report_parts.append("局部地区降小到中雨")

    # 3. 再次判断个别地区降雨(>0%)
    elif rainfall_stats['暴雨'] > 0:
        report_parts.append("个别地区降暴雨")
    elif rainfall_stats['大雨'] > 0:
        report_parts.append("个别地区降大雨")
    elif rainfall_stats['中雨'] > 0:
        report_parts.append("个别地区降中雨")
    elif rainfall_stats['小雨'] > 0:
        report_parts.append("个别地区降小雨")

    # 添加最大降雨点
    if max_rainfall > 0:
        report_parts.append(f"，最大点雨量{max_station}站{max_rainfall}毫米")

    return "".join(report_parts)

def get_hydrometric_station(auth_token=None, station_code=None, ):
    """
    获取河道水文站基本信息

    参数:
        station_code: 水文站代码 (String, 可选)
        auth_token: JWT认证令牌 (String)

    返回:
        (status_code, response_data) 元组
    """
    auth_token = auth_token#oauth_login()

    try:
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"
        }

        params = {}
        if station_code:
            params["stcd"] = station_code
        HYDROMETRIC_API_URL = f"{BASE_API_URL}/hydrometric/hourrt/listLatest"
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



def oauth_login(
        access_key: str = "fxylh",
        secret_key: str = "656ed363fa5513bb9848b430712290b2",
        user_type: int = 3
) :
    """
    """
    #url = "http://10.4.158.35:8070/oauth/login"
    url = f"{BASE_API_URL}/oauth/login"
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



def format_hydrometric_data_v1(auth_token=None,station_code=None):
    """
    获取并格式化水文站数据（仅返回YLH_HD列表中的站点）
    参数:
        station_code: 水文站代码 (可选)
    返回:
        (status_code, formatted_data) 元组
        formatted_data格式示例:
        {
            "hdsq": [
                {
                    "站名": "站名1",
                    "当日8时流量(m³/s)": 100.5,  # 仅8点数据有值，否则为None
                    "昨日日均流量": 95.2
                },
                ...
            ]
        }
    """
    # 首先获取原始数据
    auth_token = auth_token#oauth_login()
    status_code, raw_data = get_hydrometric_station(auth_token=auth_token,station_code=station_code)
    lyh_hd = ["卢氏", "长水", "宜阳", "白马寺", "黑石关", "东湾", "陆军", "龙门镇", "花园口"]
    # 如果请求不成功，直接返回原始结果
    if status_code != 200:
        return status_code, raw_data
    # 初始化格式化后的数据
    formatted_data = {"hdsq": []}
    try:
        # 处理数据
        if 'data' in raw_data and isinstance(raw_data['data'], list):
            for station in raw_data['data']:
                # 只处理416开头的站点且在YLH_HD列表中的站点
                if str(station.get('stcd', '')).startswith('416') and station.get('stnm') in lyh_hd:
                    # 获取昨日日均流量
                    hysta = station.get('stcd')
                    dayrt_status, dayrt_data = get_hydrometric_dayrt_list(auth_token=auth_token,hysta=hysta)
                    yesterday_avg_flow = None
                    if dayrt_status == 200 and dayrt_data.get('data') and len(dayrt_data['data']) > 0:
                        yesterday_avg_flow = dayrt_data['data'][0]["flow"]
                    # 检查时间是否为当日8点
                    timestamp = station.get('date')
                    eight_am_flow = None
                    if timestamp:
                        dt = datetime.fromtimestamp(timestamp / 1000)
                        now = datetime.now()
                        if dt.date() == now.date() and dt.hour == 8:  # 仅当日期为今日且时间为8点时记录流量
                            eight_am_flow = station.get('dstrvm')
                    # 构建格式化条目
                    formatted_entry = {
                        "站名": station.get('stnm', '未知站名'),
                        "当日8时流量(m³/s)": eight_am_flow,  # 非8点数据为None
                        "昨日日均流量": yesterday_avg_flow
                    }
                    formatted_data["hdsq"].append(formatted_entry)
        return status_code, formatted_data

    except Exception as e:
        return 500, {"error": f"数据处理错误: {str(e)}"}


def format_hydrometric_data(auth_token=None, station_code=None):
    """
    获取并格式化水文站数据（固定返回9个指定站点）
    修改：返回所有指定站点的数据，没有数据的站点设为None

    参数:
        auth_token: 认证令牌
        station_code: 水文站代码 (可选)
    返回:
        (status_code, formatted_data) 元组
        formatted_data格式示例:
        {
            "hdsq": [
                {
                    "站名": "卢氏",
                    "流量(m³/s)": 100.5  # 有数据则为数值，无数据则为None
                },
                {
                    "站名": "长水",
                    "流量(m³/s)": None  # 无数据
                },
                ...  # 共9个站点
            ]
        }
    """
    # 定义固定的10个水文站列表
    lyh_hd = ["栾川","灵口","东湾", "卢氏", "陆军","长水","龙门镇",  "宜阳", "白马寺", "黑石关"]
    # 首先获取原始数据
    auth_token = auth_token  # oauth_login()
    status_code, raw_data = get_hydrometric_station(auth_token=auth_token, station_code=station_code)
    # 初始化格式化后的数据（包含所有9个站点）
    formatted_data = {"hdsq": []}
    # 创建站点数据字典，方便查找
    station_data_map = {}
    if status_code == 200 and 'data' in raw_data and isinstance(raw_data['data'], list):
        for station in raw_data['data']:
            if str(station.get('stcd', '')).startswith('416') and station.get('stnm') in lyh_hd:
                station_data_map[station['stnm']] = station
    try:
        # 确保返回所有9个站点
        for station_name in lyh_hd:
            flow_value = None

            # 如果该站点有数据且是8点数据
            if station_name in station_data_map:
                station = station_data_map[station_name]
                timestamp = station.get('date')

                if timestamp:
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    if dt.hour == 8:  # 仅当时间为8点时记录流量
                        flow_value = station.get('flow')

            formatted_data["hdsq"].append({
                "站名": station_name,
                "流量(m³/s)": flow_value
            })
        return status_code, formatted_data
    except Exception as e:
        # 出错时也返回完整结构
        for station_name in lyh_hd:
            formatted_data["hdsq"].append({
                "站名": station_name,
                "流量(m³/s)": None
            })
        return 500, {"error": f"数据处理错误: {str(e)}", "hdsq": formatted_data["hdsq"]}

def get_sk_data(auth_token):
    """
    获取河道水文站基本信息

    参数:
        station_code: 水文站代码 (String, 可选)
        auth_token: JWT认证令牌 (String)

    返回:
        (status_code, response_data) 元组
    """
    auth_token = auth_token#oauth_login()

    try:
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"
        }

        params = {}
        HYDROMETRIC_API_URL = f"{BASE_API_URL}/hydrometric/rhourrt/listLatest"
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


def get_reservoir_properties(auth_token,ennmcd=None):
    """
    获取水库特征值信息列表

    参数:
        ennmod: 水库编码 (String, 可选)

    返回:
        (status_code, response_data) 元组
        成功时返回数据结构示例:
        {
            "code": 200,
            "data": [
                {
                    "capImmilv1": "",
                    "capNormallv1": 242.9,
                    "lvIiceMax": "",
                    "lvIFldDes": 2602.25,
                    # ...其他字段见接口文档
                }
            ]
        }
    """
    auth_token = auth_token#oauth_login()  # 获取认证token

    try:
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"
        }
        params = {}
        if ennmcd:
            params["ennmcd"] = ennmcd
        API_URL = f"{BASE_API_URL}/project/rprop/list"
        response = requests.get(
            API_URL,
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


def get_reservoir_kurong(auth_token,resname):
    """
    获取水库水位-库容曲线信息
    参数:
        resname: 水库编码 (字符串，可选)
    返回:
        (status_code, response_data) 元组:
        - status_code: HTTP状态码
        - response_data: 接口返回的JSON数据或错误信息
    异常处理:
        - 处理超时、请求异常和数据格式错误
        - 返回标准化的错误信息
    示例:
        >>> status, data = get_reservoir_kurong("BDA00000121")
        >>> if status == 200:
        ...     print(data["data"][0]["capactiy"])  # 输出库容数据
    """
    # 获取认证令牌
    auth_token = auth_token
    try:
        # 构造请求头
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"  # 使用Bearer Token认证
        }

        # 构造查询参数
        params = {}
        if resname:
            params["resname"] = resname.strip()  # 去除前后空格

        # 设置API端点
        API_URL = f"{BASE_API_URL}/project/resvzv/list"

        # 发送请求（设置双超时）
        response = requests.get(
            API_URL,
            params=params,
            headers=headers,
            timeout=(3.05, 10)  # 连接超时3.05秒，读取超时10秒
        )

        # 验证响应
        response.raise_for_status()
        return response.status_code, response.json()

    except requests.exceptions.Timeout:
        return 408, {"error": "请求超时，请检查网络连接"}
    except requests.exceptions.HTTPError as e:
        return e.response.status_code, {"error": f"HTTP错误: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return 500, {"error": f"请求异常: {str(e)}"}
    except ValueError as e:
        return 500, {"error": f"响应数据解析失败: {str(e)}"}

def format_reservoir_data_v1(auth_token):
    """
    获取并格式化水库数据（包含汛限水位信息）

    返回:
        dict: 格式化后的水库数据，结构如下:
        {
            "sksq": [
                {
                    "水库名称": str,
                    "水位（m）": float,
                    "蓄量（亿m³）": float,
                    "汛限水位": Optional[float],  # 允许为None
                    "相应蓄量": Optional[float],  # 允许为None
                    "超蓄水量（亿m³）": float,
                    "剩余防洪库容（亿m³）": float
                },
                ...
            ]
        }
    """
    status_code, raw_data = get_sk_data(auth_token=auth_token)
    lyh_sk = ["三门峡", "小浪底", "陆浑", "故县", "河口村"]
    formatted_data = {"sksq": []}
    try:
        if (
            status_code == 200
            and isinstance(raw_data, dict)
            and "data" in raw_data
            and isinstance(raw_data["data"], list)
        ):
            for reservoir in raw_data["data"]:
                if reservoir.get("ennm") in lyh_sk:
                    wq = reservoir.get("wq", "")
                    ennmcd = reservoir.get("ennmcd", "")
                    flood_level = None  # 默认None
                    flood_capacity = None  # 默认None
                    shengyukurong = None
                    if ennmcd:
                        prop_status, prop_data = get_reservoir_properties(auth_token=auth_token,ennmcd=ennmcd)
                        if (prop_status == 200 and prop_data.get("data")and len(prop_data["data"]) > 0):
                            # 处理汛限水位（允许None）
                            flood_level_str = prop_data["data"][0].get("lvlFldCtr", "")
                            try:
                                flood_level = float(flood_level_str) if flood_level_str else None
                            except (ValueError, TypeError):
                                flood_level = None  # 转换失败则设为None

                            # 处理相应蓄量（允许None）
                            flood_capacity_str = prop_data["data"][0].get("capCtrfldlvl", "")
                            try:
                                flood_capacity = float(flood_capacity_str) if flood_capacity_str else None
                            except (ValueError, TypeError):
                                flood_capacity = None  # 转换失败则设为None
                        kurong_status, kurong_data = get_reservoir_kurong(auth_token=auth_token,resname=ennmcd)
                        if (kurong_status == 200 and kurong_data.get("data")
                                and len(kurong_data["data"]) > 0):
                            # 使用正确的字段名（根据实际接口返回）
                            kurong = float(kurong_data['data'][-1].get("capactiy", 0))
                            shengyukurong = round(kurong - wq, 3) if kurong > wq else 0
                    # 构建格式化条目（None值不进行round计算）
                    formatted_entry = {
                        "水库名称": reservoir.get("ennm", "未知水库"),
                        "水位（m）": round(float(reservoir.get("level", 0)), 2),
                        "蓄量（亿m³）": round(float(reservoir.get("wq", 0)), 3),
                        "汛限水位（m）": round(flood_level, 2) if flood_level is not None else None,
                        "相应蓄量（亿m³）": round(flood_capacity, 3) if flood_capacity is not None else None,
                        "超蓄水量（亿m³）":round(wq-flood_capacity ,3) if flood_capacity is not None else shengyukurong,
                        "剩余防洪库容（亿m³）":shengyukurong
                    }
                    formatted_data["sksq"].append(formatted_entry)
        return formatted_data
    except Exception as e:
        print(f"数据格式化错误: {str(e)}")
        return {"sksq": []}


def format_reservoir_data(auth_token):
    """
    获取并格式化水库数据（包含汛限水位信息）
    修改：添加河名字段，简化返回字段

    返回:
        dict: 格式化后的水库数据，结构如下:
        {
            "sksq": [
                {
                    "河名": str,
                    "水库名称": str,
                    "水位（m）": float,
                    "蓄量（亿m³）": float
                },
                ...
            ]
        }
    """
    status_code, raw_data = get_sk_data(auth_token=auth_token)
    lyh_sk = ["陆浑", "故县"]
    # 水库与河名对应关系
    reservoir_to_river = {
        "陆浑": "伊河",
        "故县": "洛河"
    }

    formatted_data = {"sksq": []}
    try:
        if (
                status_code == 200
                and isinstance(raw_data, dict)
                and "data" in raw_data
                and isinstance(raw_data["data"], list)
        ):
            for reservoir in raw_data["data"]:
                reservoir_name = reservoir.get("ennm", "未知水库")
                if reservoir_name in lyh_sk:
                    # 获取对应河名
                    river_name = reservoir_to_river.get(reservoir_name, "")

                    # 构建简化后的格式化条目
                    formatted_entry = {
                        "河名": river_name,
                        "水库名称": reservoir_name,
                        "水位（m）": round(float(reservoir.get("level", 0)), 2),
                        "蓄量（亿m³）": round(float(reservoir.get("wq", 0)), 3)
                    }
                    formatted_data["sksq"].append(formatted_entry)
        return formatted_data
    except Exception as e:
        print(f"数据格式化错误: {str(e)}")
        return {"sksq": []}

def get_hydrometric_dayrt_list(auth_token,hysta=None, start_date=None, end_date=None):
    """
    获取水文站日均水情信息列表

    参数:
        hysta: 水文站代码 (String, 可选)
        start_date: 开始日期 (String, 格式: YYYY-MM-DD, 默认昨天)
        end_date: 结束日期 (String, 格式: YYYY-MM-DD, 默认今天)

    返回:
        (status_code, response_data) 元组
    """
    auth_token = auth_token#oauth_login()  # 获取认证token
    try:
        # 设置默认日期
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        if not start_date:
            start_date = yesterday.strftime('%Y-%m-%d')
        if not end_date:
            end_date = today.strftime('%Y-%m-%d')
        headers = {
            "Accept": "application/json",
            "Authorization": f"{auth_token}"
        }
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        if hysta:
            params["hysta"] = hysta
        API_URL = f"{BASE_API_URL}/hydrometric/dayrt/list"
        response = requests.get(
            API_URL,
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

    # 示例2：自定义部分参数
    # success, data = get_rain_polygon(
    #     base_url="http://10.4.1.98:8401",
    #     stdt="2023100108",  # 字符串格式
    #     prtime=12
    # )

import geopandas as gpd
import matplotlib.pyplot as plt
import json
from urllib.parse import urljoin


def get_rain_polygon_geojson(base_url, stdt, dt, prtime):
    """
    获取降雨多边形GeoJSON数据
    """
    endpoint = "/api/v1/ybrain/GetRainPolygonGeojson"
    url = urljoin(base_url, endpoint)
    print(f"请求URL: {url}")  # 调试输出

    params = {
        "stdt": stdt,
        "dt": dt,
        "prtime": prtime
    }
    print(f"请求参数: {params}")  # 调试输出

    try:
        # 增加超时时间并添加重试机制
        for attempt in range(3):  # 重试3次
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=(10, 60),  # 连接10秒，读取60秒
                    headers={'Accept': 'application/json'}  # 明确要求JSON
                )
                response.raise_for_status()
                break  # 成功则跳出重试循环
            except requests.exceptions.Timeout:
                if attempt == 2:  # 最后一次尝试
                    return 408, {"error": "请求超时"}
                print(f"请求超时，第{attempt + 1}次重试...")
                continue

        print(f"HTTP状态码: {response.status_code}")
        print(f"响应头: {response.headers}")

        content = response.text
        print(f"原始响应(前500字符):\n{content[:500]}")

        # 更健壮的JSON提取
        json_str = content
        if '<' in content:  # 如果是XML包装
            json_start = max(content.find('{'), content.find('['))
            if json_start == -1:
                return 500, {"error": "未找到JSON数据"}
            json_end = max(content.rfind('}'), content.rfind(']')) + 1
            json_str = content[json_start:json_end]

        # 尝试解析JSON
        try:
            geojson_data = json.loads(json_str)
            return response.status_code, geojson_data
        except json.JSONDecodeError as e:
            # 尝试修复常见JSON格式问题
            json_str = json_str.replace("_", "").replace(" ", "")  # 处理_和空格
            try:
                geojson_data = json.loads(json_str)
                return response.status_code, geojson_data
            except:
                return 500, {"error": f"JSON解析失败: {str(e)}"}

    except Exception as e:
        return 500, {"error": f"请求异常: {str(e)}"}


def plot_rain_polygon(geojson_data, output_image_path=None):
    """
    渲染降雨多边形GeoJSON数据

    参数:
        geojson_data: GeoJSON格式的数据
        output_image_path: 输出图片路径 (可选)
    """
    # 将GeoJSON数据转换为GeoDataFrame
    try:
        gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 10))

        # 绘制多边形，使用CONTOUR值作为颜色
        if "CONTOUR" in gdf.columns:
            gdf.plot(ax=ax, column="CONTOUR", cmap="Blues", legend=True,
                     legend_kwds={'label': "降雨量(mm)", 'shrink': 0.6})
        else:
            gdf.plot(ax=ax, color="blue", alpha=0.5)

        # 添加标题和标签
        ax.set_title(f"降雨分布图\n时间: {geojson_data.get('name', '')}")
        ax.set_xlabel("经度")
        ax.set_ylabel("纬度")

        # 保存或显示图像
        if output_image_path:
            plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
            print(f"图片已保存到 {output_image_path}")

        plt.show()

    except Exception as e:
        print(f"渲染失败: {str(e)}")


def fetch_and_plot_rainfall(base_url, stdt, dt, prtime, output_path=None):
    """
    完整流程：获取数据并渲染降雨多边形

    参数:
        base_url: 基础API地址
        stdt: 开始时间
        dt: 结束时间
        prtime: 时间跨度
        output_path: 输出图片路径 (可选)
    """
    # 1. 获取数据
    status_code, data = get_rain_polygon_geojson(base_url, stdt, dt, prtime)

    if status_code != 200:
        print(f"获取数据失败 (状态码: {status_code}): {data}")
        return

    # 2. 渲染地图
    plot_rain_polygon(data, output_path)

from datetime import datetime, timedelta
if __name__ == "__main__":
    # end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # start_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    #
    # status, data = get_rainfall_data()
    #
    # if status == 200:
    #     print("请求成功，数据样例:")
    #     print(data)
    # else:
    #     print(f"请求失败 (状态码 {status}): {data}")
    #

    auth_token = oauth_login()
    print("auth_token:",auth_token)
    # status, data = get_rainfall_data_day(auth_token=auth_token)
    # print("data：",data)
    # res = generate_rainfall_report(response_data=data)
    # print("降雨报告：",res)
    data = get_hydrometric_station(auth_token=auth_token)
    print("河道实时水情:",data)
    code, res = format_hydrometric_data(auth_token=auth_token)
    print("格式化后的河道实时水情：",res)

    # #
    code,res = get_reservoir_kurong(auth_token=auth_token,resname="BDA00000121")
    print("res:",res)
    code , res = get_sk_data(auth_token)
    print("水库数据：",res)

    res = format_reservoir_data(auth_token=auth_token)
    print("水库数据格式化：",res)

    # 示例1：全部使用默认参数（STDT=现在，DT=明天此时，PRTIME=24）
    # BASE_URL = "http://10.4.158.35:8093"  # 替换为实际API地址
    # START_TIME = "2021100308"  # 开始时间
    # END_TIME = "2021100408"  # 结束时间
    # TIME_SPAN = 24  # 时间跨度(小时)
    # OUTPUT_PATH = "rainfall_polygon.png"  # 输出图片路径
    #
    # # 执行
    # fetch_and_plot_rainfall(
    #     base_url=BASE_URL,
    #     stdt=START_TIME,
    #     dt=END_TIME,
    #     prtime=TIME_SPAN,
    #     output_path=OUTPUT_PATH
    # )