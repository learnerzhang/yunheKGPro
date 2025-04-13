import requests


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
            url="http://10.4.158.35:8070/rainfall/hourrth/getRainfall",
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

import json
# def oauth_login(
#         access_key: str = "fxylh",
#         secret_key: str = "656ed363fa5513bb9848b430712290b2",
#         user_type: int = 3
# ) :
#     """
#     """
#     url = "http://10.4.158.35:8070/oauth/login"
#     headers = {"Content-Type": "application/json",
#         "Accept": "application/json"}
#     payload = {"accessKey": access_key, "secretKey": secret_key, "userType": user_type}
#     try:
#         response = requests.post(url=url,headers=headers,data=json.dumps(payload),timeout=10)
#         response.raise_for_status()
#         return response.json()['data']
#
#     except requests.exceptions.RequestException as e:
#         return {"code": 500,"data": None,"msg": f"请求失败: {str(e)}"}
#     except ValueError:
#         return {"code": 500,"data": None,"msg": "响应数据解析失败"}

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
                    "入库流量": round(float(reservoir.get("inflow", 0)), 2),
                    "出库流量": round(float(reservoir.get("outflow", 0)), 2)
                }
                formatted_data["sksq"].append(formatted_entry)

        return formatted_data

    except Exception as e:
        print(f"数据格式化错误: {str(e)}")
        return {"sksq": []}

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
    # res = oauth_login()
    # print("res:",res)
    # status, data = get_rainfall_data_day()
    # print("res:",data)
    # res = generate_rainfall_report(data)
    # print("降雨报告：",res)
    data = get_hydrometric_station()
    print("水文站实时水情:",data)
    code, res = format_hydrometric_data()
    print("河道站实时水情格式化:",res)

    code , res = get_sk_data()
    print("水库数据：",res)

    res = format_reservoir_data()
    print("水库数据格式化：",res)