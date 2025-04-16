import requests
import json
from urllib.parse import urljoin
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, GeoType

def get_rain_polygon_geojson(base_url: str, stdt: str, dt: str, prtime: int) :
    # ...（保持之前的参数和请求部分不变）...
    endpoint = "/api/v1/ybrain/GetRainPolygonGeojson"
    url = urljoin(base_url, endpoint)
    params = {
        "stdt": stdt,
        "dt": dt,
        "prtime": str(prtime)  # 确保参数为字符串
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=(10, 30)
        )

        print(f"请求URL: {response.url}")
        print(f"状态码: {response.status_code}")

        response.raise_for_status()
        content = response.text.strip()

        # 调试：打印原始响应前200字符
        print("原始响应片段:", content[:200])

        # 修复步骤1：去除外层双引号（如果存在）
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]

        # 修复步骤2：处理转义字符
        content = content.encode().decode('unicode_escape')

        # 调试：打印处理后的前200字符
        print("处理后片段:", content[:200])

        # 解析JSON
        json_data = json.loads(content)

        # 验证数据结构
        if not isinstance(json_data, dict) or "features" not in json_data:
            return 500, {"error": "无效的GeoJSON格式", "data": json_data}

        return response.status_code, json_data

    except json.JSONDecodeError as e:
        # 提供更多调试信息
        error_position = e.pos
        context = content[max(0, error_position - 20):error_position + 20]
        return 500, {
            "error": f"JSON解析错误: {str(e)}",
            "position": error_position,
            "context": context,
            "full_response": content[:1000]  # 限制长度防止过大
        }
    except Exception as e:
        return 500, {"error": f"处理失败: {str(e)}"}


def render_rainfall_echarts(data, output_file):
    # 创建 Geo 图表对象
    geo = (
        Geo()
        .add_schema(
            maptype="china",
            itemstyle_opts=opts.ItemStyleOpts(
                color="rgba(255, 255, 255, 0)", border_color="rgba(0, 0, 0, 0.2)"
            ),
        )
    )

    # 遍历 features 中的每个 feature
    for feature in data["features"]:
        geometry = feature["geometry"]
        if geometry["type"] == "Polygon":
            coordinates = geometry["coordinates"]
            value = feature["properties"]["CONTOUR"]

            # 确保坐标有效
            for coord in coordinates:
                if isinstance(coord, list) and len(coord) > 0:
                    for point in coord:
                        if len(point) == 2:  # 确保点是二元组
                            try:
                                geo.add(
                                    series_name="降雨图斑",
                                    data_pair=[(tuple(point), value)],
                                    type_=ChartType.SCATTER,
                                )
                            except Exception as e:
                                print(f"添加坐标 {point} 时出错: {e}")
                        else:
                            print(f"无效的坐标格式: {point}")
                else:
                    print(f"无效的坐标数据: {coord}")

    # 设置全局选项
    geo.set_global_opts(
        title_opts=opts.TitleOpts(title="降雨图斑数据"),
        visualmap_opts=opts.VisualMapOpts(
            min_=min([f["properties"]["CONTOUR"] for f in data["features"]]),
            max_=max([f["properties"]["CONTOUR"] for f in data["features"]]),
            range_color=["#ffffff", "#00ff00", "#0000ff", "#ff0000"],
        ),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )

    # 渲染图表到 HTML 文件
    geo.render(output_file)
    return geo

if __name__ == "__main__":
    # 配置参数
    BASE_URL = "http://10.4.158.35:8093"
    START_DATE = "2024100308"
    END_DATE = "2024100408"
    TIME_SPAN = 24
    OUTPUT_FILE = "rainfall_echarts.html"

    try:
        # 1. 获取数据
        status, data = get_rain_polygon_geojson(BASE_URL, START_DATE, END_DATE, TIME_SPAN)
        print("geojson数据为：", data)
        # 2. 渲染ECharts图表
        chart = render_rainfall_echarts(data, OUTPUT_FILE)

        # 3. 可选：直接显示（需Jupyter环境）
        from pyecharts.render import make_snapshot
        from snapshot_selenium import snapshot
        make_snapshot(snapshot, chart.render(), "rainfall.png")

    except Exception as e:
        print(f"程序执行失败: {str(e)}")