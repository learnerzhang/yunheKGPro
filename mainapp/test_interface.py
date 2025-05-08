import requests
#from yunheKGPro.settings import config
import requests
from datetime import datetime, timedelta
import json
from xml.etree import ElementTree
BASE_API_URL= "http://wt.hxyai.cn/fx/"#"http://10.4.158.35:8070/"

# _last_auth_token = None
# _last_token_time = None
# TOKEN_EXPIRY_MINUTES = 5  # token有效期5分钟
# def oauth_login(
#         access_key: str = "fxylh2",
#         secret_key: str = "899d657383d458a546bd80f1a0753263",
#         user_type: int = 3,
#         use_cache: bool = True  # 是否使用缓存token
# ):
#     """
#     获取认证token，支持缓存机制
#     """
#     global _last_auth_token, _last_token_time
#
#     # 如果使用缓存且缓存未过期，直接返回缓存的token
#     if use_cache and _last_auth_token and _last_token_time:
#         if datetime.now() - _last_token_time < timedelta(minutes=TOKEN_EXPIRY_MINUTES):
#             return _last_auth_token
#
#     url = f"{BASE_API_URL}oauth/login"
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }
#     payload = {
#         "accessKey": access_key,
#         "secretKey": secret_key,
#         "userType": user_type
#     }
#
#     try:
#         response = requests.post(
#             url=url,
#             headers=headers,
#             data=json.dumps(payload),
#             timeout=10
#         )
#         response.raise_for_status()
#         token_data = response.json().get('data')
#
#         # 更新缓存
#         if token_data:
#             _last_auth_token = token_data
#             _last_token_time = datetime.now()
#
#         return token_data
#
#     except requests.exceptions.RequestException as e:
#         # 如果请求失败但有有效缓存，返回缓存token
#         if use_cache and _last_auth_token and _last_token_time:
#             if datetime.now() - _last_token_time < timedelta(minutes=TOKEN_EXPIRY_MINUTES):
#                 print(f"获取新token失败，使用缓存的token。错误: {str(e)}")
#                 return _last_auth_token
#         return None
#
#     except ValueError:
#         # 如果解析失败但有有效缓存，返回缓存token
#         if use_cache and _last_auth_token and _last_token_time:
#             if datetime.now() - _last_token_time < timedelta(minutes=TOKEN_EXPIRY_MINUTES):
#                 print("解析新token失败，使用缓存的token")
#                 return _last_auth_token
#         return None

def oauth_login(
        access_key: str = "fxylh",#"fxylh2",
        secret_key: str = "656ed363fa5513bb9848b430712290b2",#"899d657383d458a546bd80f1a0753263",#
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


# def oauth_login():
#     url = "http://10.4.158.35:8091/map/xiaoyu/getTK"
#     params = {"auth": "ylh"}
#
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # 检查HTTP错误
#
#         json_data = response.json()
#         if json_data.get("code") == 200:
#             return json_data.get("msg")
#         else:
#             print(f"API returned non-200 code: {json_data.get('code')}")
#             return None
#
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {str(e)}")
#         return None
#     except ValueError:
#         print("Failed to parse JSON response")
#         return None


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
    # 如果当前时间小于8点，则开始时间是昨天8点，否则是今天8点
    now = datetime.now()
    if now.hour < 8:
        start_default = (now.replace(hour=8, minute=0, second=0, microsecond=0))- timedelta(days=1)
    else:
        start_default = now.replace(hour=8, minute=0, second=0, microsecond=0)

    end_default = now#start_default + timedelta(days=1)
    # 设置默认时间范围（今天和昨天）
    # today = datetime.now().strftime("%Y-%m-%d")
    # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    # # 处理时间参数
    # params["endDate"] = end_default #end_time if end_time else today
    # params["startDate"] = start_default #start_time if start_time else yesterday
    params["endDate"] = end_time if end_time else end_default.strftime("%Y-%m-%d %H:%M:%S")
    params["startDate"] = start_time if start_time else start_default.strftime("%Y-%m-%d %H:%M:%S")
    print("params:",params)
    if basin:
        params["stcd"] = basin
    try:
        # 使用提供的JWT token
        auth_token = auth_token#oauth_login()

        # 添加超时和请求头
        response = requests.get(
            url=f"{BASE_API_URL}/rainfall/hourrth/getRainfall",#dayrt
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

def get_max_rainfall_station(data):
    """
    从降雨量数据中找出降雨量最大的站点

    参数:
        data: 列表，包含各个站点的数据字典，格式见示例

    返回:
        dict: 包含最大降雨量站点的 'stnm'(站名), 'lgtd'(经度), 'lttd'(纬度)
        或 None（如果所有站点降雨量都为0）
    """
    max_rainfall = -1
    max_station = None
    yiluo_stations = [station for station in data
                      if str(station['stcd']).startswith('416')]
    for station in yiluo_stations:
        rainfall = station.get("rf", 0)
        if rainfall > max_rainfall:
            max_rainfall = rainfall
            max_station = station

    # 如果所有站点的降雨量都是0，则返回None
    if max_rainfall == 0:
        return None

    return {
        "stnm": max_station["stnm"],
        "lgtd": max_station["lgtd"],
        "lttd": max_station["lttd"],
        "rf": max_station["rf"]
    }

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


def get_ylh_rainfall():
    """
    获取伊洛河流域面雨量数据
    返回格式：字符串 "伊洛河流域面雨量XX毫米" 或错误信息字符串
    """
    # 计算时间范围（昨天8点到今天8点）
    now = datetime.now()
    end_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=1)

    # 格式化时间参数
    params = {
        "startTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "endTime": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # 发送请求
        response = requests.get(
            #"http://10.4.158.35:8092/rfFace/YLH/RainAnalysis",#经过nginx转发的地址
            "http://10.4.158.36:9091/YLH/RainAnalysis",#原始地址
            params=params,
            #timeout=10
        )
        response.raise_for_status()

        # 解析响应数据
        data = response.json()
        if data.get("code") == "200":
            return f"伊洛河流域面雨量{data.get('meanrain', 0)}毫米"
        return data.get("message", "接口返回数据异常")

    except requests.exceptions.Timeout:
        return "请求超时，请稍后重试"
    except requests.exceptions.RequestException as e:
        return f"请求失败：{str(e)}"
    except (KeyError, ValueError) as e:
        return "数据解析错误"
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
    today = datetime.now()
    if not response_data or 'data' not in response_data:
        return f"{today.month}月{today.day}日，未获取到伊洛河流域降雨数据。"

    # 筛选伊洛河流域站点(416开头)
    yiluo_stations = [station for station in response_data['data']
                      if str(station['stcd']).startswith('416')]

    if not yiluo_stations:
        return f"{today.month}月{today.day}日，伊洛河流域无降雨。"#"伊洛河流域无降雨监测数据"

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
        return f"{today.month}月{today.day}日，伊洛河流域无降雨。"

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
    meanrain = get_ylh_rainfall()
    print("面雨量：",meanrain)
    report_parts = [f"{today.month}月{today.day}日"]
    if isinstance(meanrain, str) and "面雨量" in meanrain:
        report_parts.append(f"，{meanrain}")
    else:
        pass
    report_parts.append("，伊洛河流域")
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
        report_parts.append(f"，最大点雨量{max_station}站{max_rainfall}毫米。")

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


import requests
from typing import Optional, Dict


def get_access_token(
        username: str = "admin1",
        password: str = "Yrec!@#2025",
        client_id: str = "e5cd7e4891bf95d1d19206ce24a7b32e",
        grant_type: str = "password",
        base_url: str = "http://10.4.158.35:8091"  # 根据实际环境修改
) -> Optional[str]:
    """
    获取认证Token

    参数:
        username: 用户名 (默认示例值)
        password: 密码 (默认示例值)
        client_id: 客户端ID (默认示例值)
        grant_type: 授权类型 (固定password)
        base_url: 接口基础地址

    返回:
        str: 成功返回access_token，失败返回None
    """
    url = f"{base_url}/auth/login"
    payload = {
        "username": username,
        "password": password,
        "clientId": client_id,
        "grantType": grant_type
    }
    try:
        response = requests.post(
            url=url,
            json=payload,  # 使用json参数自动设置Content-Type为application/json
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 200:
            return data["data"]["access_token"]
        else:
            print(f"登录失败: {data.get('msg')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求异常: {str(e)}")
        return None
    except (KeyError, ValueError) as e:
        print(f"数据解析错误: {str(e)}")
        return None

# 使用示例
def get_weather_warning(auth_token: str, timeout: int = 10):
    """
    获取天气预警信息并生成描述文本（带去重功能）

    参数:
        auth_token (str): 认证Token
        timeout (int): 请求超时时间(秒)，默认10秒

    返回:
        dict: 包含响应状态和数据的字典，格式:
        {
            "status_code": int,    # HTTP状态码
            "data": dict | str,    # 成功时为JSON数据，失败时为错误信息
            "description": str     # 生成的预警描述文本
        }
    """
    url = "http://10.4.158.35:8091/pre/getWeatherWarning"
    try:
        response = requests.get(
            url=url,
            headers={
                "ClientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
                "Authorization": f"Bearer {auth_token}"
            },
            timeout=timeout
        )
        response.raise_for_status()
        result = response.json()

        # 初始化预警分类字典（使用集合自动去重）
        warning_levels = {
            "红色": set(),
            "橙色": set(),
            "黄色": set(),
            "蓝色": set()
        }

        # 处理数据并生成描述
        description = "根据伊洛河流域县区气象台发布的预警信息"

        if result.get("code") == 200 and result.get("data"):
            # 提取并分类预警信息（自动去重）
            for warning in result["data"]:
                city_name = warning.get("cityName", "")
                warning_name = warning.get("warningName", "")

                # 提取县区名称（改进的提取逻辑）
                county = extract_county_name(city_name)

                # 分类预警级别
                if county:  # 只有有效县区名称才添加
                    if "红色" in warning_name:
                        warning_levels["红色"].add(county)
                    elif "橙色" in warning_name:
                        warning_levels["橙色"].add(county)
                    elif "黄色" in warning_name:
                        warning_levels["黄色"].add(county)
                    elif "蓝色" in warning_name:
                        warning_levels["蓝色"].add(county)

            # 构建描述文本
            parts = []
            for level, counties in warning_levels.items():
                if counties:
                    # 将集合转为列表并排序，确保输出顺序一致
                    sorted_counties = sorted(list(counties))
                    counties_str = "、".join(sorted_counties)
                    # 单数/复数处理
                    if len(sorted_counties) > 1:
                        parts.append(f"{counties_str}等{len(sorted_counties)}个县区发布了暴雨{level}预警")
                    else:
                        parts.append(f"{counties_str}发布了暴雨{level}预警")

            if parts:
                description += "，" + "，".join(parts) + "。"
            else:
                description += "当前无暴雨预警。"
        else:
            description += "当前无暴雨预警。"

        return {
            "status_code": response.status_code,
            "data": result,
            "description": description
        }

    except requests.exceptions.Timeout:
        return {
            "status_code": 408,
            "data": "请求超时",
            "description": "获取预警信息超时"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 500,
            "data": f"请求失败: {str(e)}",
            "description": "获取预警信息失败"
        }
    except ValueError:
        return {
            "status_code": 500,
            "data": "返回数据格式异常",
            "description": "预警信息解析错误"
        }

def get_rain_analysis(auth_token: str, timeout: int = 10):
    """
    获取降雨分析信息并生成描述文本（自动根据当前时间设置时间段）

    参数:
        auth_token (str): 认证Token
        timeout (int): 请求超时时间(秒)，默认10秒

    返回:
        dict: 包含响应状态和数据的字典，格式:
        {
            "status_code": int,    # HTTP状态码
            "data": dict | str,    # 成功时为JSON数据，失败时为错误信息
            "description": str     # 生成的降雨分析描述文本
        }
    """
    url = "http://10.4.158.35:8091/rainfall/chy/rainAnalysis"

    # 获取当前时间
    now = datetime.now()
    current_hour = now.hour

    # 自动判断开始时间和结束时间
    if current_hour < 8:
        # 当前时间小于 8 点，取昨天 08:00 到当前时间
        start_time = (now - timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        # 当前时间大于等于 8 点，取今天 08:00 到当前时间
        start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

    end_time = now

    # 格式化时间字符串（ISO格式）
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    # start_time_str = "2025-05-04 08:00:00"
    # end_time_str = "2025-05-05 01:00:00"
    full_url = f"{url}?startTime={start_time_str}&endTime={end_time_str}"
    print("full_url：",full_url)
    try:
        response = requests.get(
            url=full_url,
            headers={
                "ClientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
                "Authorization": f"Bearer {auth_token}"
            },
            timeout=timeout
        )
        response.raise_for_status()

        result = response.json()
        print("result:",result)
        print("type(result[data])",type(result['data']))
        # 初始化描述文本
        return {
            "status_code": response.status_code,
            "data":result['data']
        }

    except requests.exceptions.Timeout:
        return {
            "status_code": 408,
            "data": "访问接口超时"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status_code": 500,
            "data": f"请求失败: {str(e)}"
        }
    except ValueError:
        return {
            "status_code": 500,
            "data": "返回数据格式异常"
        }
import os
from shapely.geometry import Point
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
def plot_yuliangmian(
    rain_geojson_result,
    max_rainfall_station,
    basin_geojson_path="data/geojson/洛河流域.json",
    water_geojson_path="data/geojson/WTRIVRL25_洛河流域.json"
):
    """
    绘制洛河流域边界、雨量分布面数据、水系（河流）、最大降雨站点

    参数:
        rain_geojson_result (dict): get_rain_analysis 返回结果，可能为 None
        max_rainfall_station (dict): get_max_rainfall_station 返回的最大降雨站点信息
        basin_geojson_path (str): 流域 GeoJSON 文件路径
        water_geojson_path (str): 水系 GeoJSON 文件路径
    """

    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['axes.labelsize'] = 1  # 隐藏默认标签

    # 提取雨量面数据（兼容 None）
    data = None
    if rain_geojson_result and isinstance(rain_geojson_result.get("data"), dict):
        data = rain_geojson_result["data"]
    else:
        print("未获取到有效的雨量面数据，将不绘制雨量分布。")

    # 加载洛河流域边界 GeoJSON（如果存在）
    basin_gdf = None
    if os.path.exists(basin_geojson_path):
        try:
            basin_gdf = gpd.read_file(basin_geojson_path)
        except Exception as e:
            print(f"读取洛河流域 GeoJSON 失败: {e}")
    else:
        print(f"未找到洛河流域 GeoJSON 文件: {basin_geojson_path}")

    # 加载水系数据（河流线状数据）
    water_gdf = None
    if os.path.exists(water_geojson_path):
        try:
            water_gdf = gpd.read_file(water_geojson_path).to_crs("EPSG:4326")
        except Exception as e:
            print(f"读取水系 GeoJSON 失败: {e}")
    else:
        print(f"未找到水系 GeoJSON 文件: {water_geojson_path}")

    # 创建绘图
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('white')

    # 绘制洛河流域边界（蓝色）
    if basin_gdf is not None:
        basin_gdf.boundary.plot(ax=ax, color='lightgray', linewidth=1)

    # 定义降雨量等级与颜色
    bins = [0, 0.1, 10, 25, 50, 100, 250, float('inf')]
    colors = ['white', '#eaffcc', '#b3f7a1', '#88d8ff', '#007fff', '#ff3300', '#9900cc']
    labels = ['0 - 0.1 mm', '0.1 - 10 mm', '10 - 25 mm', '25 - 50 mm',
              '50 - 100 mm', '100 - 250 mm', '>250 mm']

    # 添加图例元素（Patch + 红点）
    legend_elements = [
        Patch(facecolor=color, edgecolor='gray', label=label)
        for color, label in zip(colors, labels)
    ]

    # 如果没有有效雨量数据，在图例顶部加一个提示项
    # if data is None or 'features' not in data:
    #     legend_elements.insert(0, Patch(facecolor='lightgray', edgecolor='black', label='无雨量数据'))

    # 如果有最大降雨站点，加入图例
    # if max_rainfall_station:
    #     legend_elements.append(
    #         Line2D([0], [0], marker='o', color='none', label='最大降雨站点',
    #                markerfacecolor='red', markersize=10, linestyle='')
    #     )
    # 解析并绘制雨量分布面数据（如有）
    if data and 'features' in data:
        try:
            rain_gdf = gpd.GeoDataFrame.from_features(data['features'])
            if 'value' in rain_gdf.columns:
                cmap = ListedColormap(colors)
                norm = BoundaryNorm(boundaries=bins, ncolors=len(colors))
                rain_gdf.plot(
                    ax=ax,
                    column='value',
                    cmap=cmap,
                    norm=norm,
                    edgecolor='gray',
                    linewidth=0.5,
                    legend=False,
                    zorder=2
                )
        except Exception as e:
            print(f"解析雨量面数据失败: {e}")

    # 绘制水系（河流）
    if water_gdf is not None:
        water_gdf.plot(
            ax=ax,
            color='darkblue',
            linewidth=0.8,
            zorder=1,
            label='河流网络'
        )
        # legend_elements.append(
        #     Line2D([0], [0], color='darkblue', lw=1.5, label='河流网络')
        # )

    # 绘制最大降雨站点（红点 + 站名标注）
    if max_rainfall_station:
        point = Point(max_rainfall_station['lgtd'], max_rainfall_station['lttd'])
        point_gdf = gpd.GeoDataFrame([{'geometry': point, 'name': max_rainfall_station['stnm']}],
                                     crs="EPSG:4326")
        point_gdf.plot(ax=ax, color='red', marker='o', markersize=70, zorder=3)

        # 添加站名和雨量标注
        ax.text(max_rainfall_station['lgtd'], max_rainfall_station['lttd'],
                f" {max_rainfall_station['stnm']}\n{max_rainfall_station['rf']}mm",
                fontsize=11, ha='left', va='bottom', color='darkred')

    # 设置标题
    ax.set_title("伊洛河流域面雨量", fontsize=14)
    ax.set_axis_off()  # 不显示坐标轴

    # 添加图例（放在右下角）
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9, title="降雨量等级")

    plt.tight_layout()

    # 自动创建输出文件夹并保存图片
    today = datetime.now().strftime("%Y-%m-%d")
    output_folder = os.path.join("data", "yuan_data", "4", "yubao", today)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "yuliang.png")

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ 图片已保存至: {output_path}")

    # 关闭图像以释放内存
    plt.close()

def extract_county_name(city_name: str) -> str:
    """
    从cityName字段中提取县区名称

    参数:
        city_name: 原始城市名称字符串（如"河南省洛阳市嵩县气象台发布..."）

    返回:
        提取后的县区名称（如"嵩县"），提取失败返回空字符串
    """
    if not city_name:
        return ""

    # 尝试按"气象台"分割
    parts = city_name.split("气象台")
    if len(parts) > 0:
        # 尝试按省市区分割
        address_parts = parts[0].split("省")[-1].split("市")
        if len(address_parts) > 1:
            return address_parts[-1]
        return parts[0]
    return ""


def get_formatted_jlyb_data(auth_token, dateTime=None):
    """
    获取格式化后的降雨预报数据

    参数:
    dateTime -- 查询时间字符串，格式为'YYYY-MM-DD HH:MM:SS'，默认为当天8点

    返回:
    格式化后的降雨数据列表，或None(如果出错)
    """
    # API基础URL
    base_url = "http://10.4.158.35:8091/pre/getPreRainDataByTime"

    # 设置默认时间为当天8点
    if dateTime is None:
        today = datetime.now().strftime("%Y-%m-%d")
        dateTime = f"{today} 08:00:00"

    try:
        # 发送GET请求带参数
        params = {"dateTime": dateTime}
        response = requests.get(base_url,  headers={
                "ClientId": "e5cd7e4891bf95d1d19206ce24a7b32e",
                "Authorization": f"Bearer {auth_token}"
            }, params=params)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON响应
        data = response.json()

        # 检查返回状态码
        if data.get("code") != 200:
            raise ValueError(f"API返回错误: {data.get('msg', '未知错误')}")

        # 转换数据格式
        formatted_data = []
        for item in data.get("data", []):
            formatted_item = {
                "区域": item.get("stationName", ""),
                "0-24小时": item.get("value24", ""),
                "24-48小时": item.get("value48", ""),
                "48-72小时": item.get("value72", "")
            }
            formatted_data.append(formatted_item)
        return formatted_data

    except requests.exceptions.RequestException as e:
        print(f"请求API时出错: {e}")
        return None
    except ValueError as e:
        print(f"数据处理错误: {e}")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


from yaapp.ylh_interface import create_flood_control_plan,call_llm_yuan_user_plan,call_llm_yuan_user_word
from datetime import datetime, timedelta
if __name__ == "__main__":
    # plan_id = create_flood_control_plan()
    # print("planid:",plan_id)
    # plan_data = call_llm_yuan_user_plan(ptid=plan_id)
    # print(plan_data)
    # word_data = call_llm_yuan_user_word(id=plan_id)
    # print(word_data)
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
    # res = get_formatted_rain_data()
    # print("径流预报:",res)
    # meanrain = get_ylh_rainfall()
    # print("面雨量：",meanrain)


    token = get_access_token()
    # if token:
    #     print("获取Token成功:", token)
    # else:
    #     print("获取Token失败")
    # result = get_weather_warning(auth_token=token)
    # # 3. 处理结果
    # if result["status_code"] == 200:
    #     print("获取预警数据成功:", result["description"])
    # else:
    #     print(f"请求失败 (状态码 {result['status_code']}):", result["data"])
    #
    rain_geojson_result = get_rain_analysis(auth_token=token)
    if rain_geojson_result["status_code"] == 200:
        print("获取降雨分析数据成功:")
        #print("降雨数据:", result["data"])
    else:
        print(f"请求失败 (状态码 {rain_geojson_result['status_code']}):", rain_geojson_result["data"])



    # res = get_formatted_jlyb_data(auth_token=token)
    # print("径流预报:",res)
    #
    #
    #
    auth_token = oauth_login()
    #auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxODk0Mjk4NDU4Njk0MTk3MjUwIiwicm5TdHIiOiJMQmw0N0JFRTlGNDFSNTFjODNSTVRnN3Z2cTFYY0xwViIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjAwMDAwMCIsInVzZXJJZCI6MTg5NDI5ODQ1ODY5NDE5NzI1MCwidXNlck5hbWUiOiJhZG1pbjEifQ.XzncDlKU08IBtfF4rz5crL1irC6skMv2DtxtkI3rJis"
    print("auth_token:",auth_token)
    if auth_token:
        auth_token = auth_token
    else:
        auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDcyMTU5MDEsImFjY291bnQiOiJmeHlsaCIsImN1cnJlbnRUaW1lTWlsbHMiOiIxNzQ2NjExMTAxNzE5In0.wJfe9cduJYkXUp4Aqb-9O_LVJpI9X6nZM95BmArimr8"
    status, data = get_rainfall_data_day(auth_token=auth_token)
    print("data：",data)
    max_rainfall_station = get_max_rainfall_station(data['data'])
    print("最大降雨站点：",max_rainfall_station)
    res = generate_rainfall_report(response_data=data)
    print("降雨报告：",res)
    plot_yuliangmian(rain_geojson_result, max_rainfall_station)
    # data = get_hydrometric_station(auth_token=auth_token)
    # print("河道实时水情:",data)
    # code, res = format_hydrometric_data(auth_token=auth_token)
    # print("格式化后的河道实时水情：",res)
    #
    # # #
    # code,res = get_reservoir_kurong(auth_token=auth_token,resname="BDA00000121")
    # print("res:",res)
    # code , res = get_sk_data(auth_token)
    # print("水库数据：",res)
    #
    # res = format_reservoir_data(auth_token=auth_token)
    # print("水库数据格式化：",res)

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