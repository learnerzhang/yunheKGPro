import requests
def get_rainfall_data(basin=None, start_time=None, end_time=None):
    """
    获取实时雨量数据（带完整错误处理）

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
        params["basin"] = basin
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time

    try:
        # 添加超时和请求头
        response = requests.get(
            url="http://wt.hxyai.cn/fx/rainfall/hourrth/getRainfall",
            params=params,
            headers={"Accept": "application/json"},
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

from datetime import datetime, timedelta
if __name__ == "__main__":
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    status, data = get_rainfall_data()

    if status == 200:
        print("请求成功，数据样例:")
        print(data)
    else:
        print(f"请求失败 (状态码 {status}): {data}")