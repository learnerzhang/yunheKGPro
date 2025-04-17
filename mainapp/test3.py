import requests
import json
from urllib.parse import urljoin
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import ChartType, GeoType
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
django.setup()
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

from yaapp.yautils import excel_to_dict,excel_to_dict_v2
from yaapp.api_yuan import query_question
from langchain.llms import Ollama
# def query_question(text):
#     llm = Ollama(model="qwq:latest")
#     res = llm(text)
#     return res
if __name__ == "__main__":
    # 配置参数
    RESERVOIR_NAME = "小浪底"
    sknames = {'三门峡', '小浪底', '陆浑', '故县', '河口村', '西霞院', '万家寨', '龙口'}
    swznames = {'花园口', '小花间', "潼关", "古贤坝址"}
    skMapData, swMapData, date_list = excel_to_dict("data/yuan_data/4/ddfad/default.xlsx")
    swData = skMapData[RESERVOIR_NAME]["水位"]
    print(swData[69])
    print(date_list[69])
    print("len(swData)", len(swData))
    print("len(date_list",len(date_list))
    prompt = f"""
        请根据提供的水库水位数据，专门分析{RESERVOIR_NAME}水库的调度过程，严格按照以下要求输出：

        输入数据：
        - 水库名称：{RESERVOIR_NAME}
        - 水位数据：{swData}
        - 时间序列：{date_list}

        输出要求：
        1. 只分析给定的水库{RESERVOIR_NAME}
        2. 找出水位最高点及其对应时间
        3. 使用以下固定格式：
           "预计{RESERVOIR_NAME}将于[yyyy-mm-dd HH:MM:SS]达到最高水位[XXX.XXXX]m"
        4. 水位值保留4位小数
        5. 时间格式必须精确到秒

        请直接输出结果字符串，不要包含任何解释、注释或额外信息。
        """

    res = query_question(prompt)
    print(res)

# if __name__ == "__main__":
#     # 配置参数
#     sknames = {'三门峡', '小浪底', '陆浑', '故县', '河口村', '西霞院', '万家寨', '龙口'}
#     swznames = {'花园口', '小花间', "潼关", "古贤坝址"}
#     skMapData, swMapData, date_list = excel_to_dict_v2("data/yuan_data/4/ddfad/default.xlsx")
#     prompt = f"""
#     请严格按照以下要求处理水文数据并生成JSON报告：
#
#     【输入数据】
#     水库数据（值,时间戳格式）：
#     { {name: {metric: [(value, timestamp), ...]} for name, metrics in skMapData.items() for values, value in metrics.items() if name in sknames} }
#
#     水文站数据（值,时间戳格式）：
#     { {name: values for name, values in swMapData.items() if name in swznames} }
#
#     【处理规则】
#     1. 水库调度：
#        - 对每个水库的"水位"数据：
#          - 找出(value,timestamp)中value最大的记录
#          - 当最高水位 > 初始水位(第一个值) + 0.5m时输出
#          - 水位值保留4位小数
#
#     2. 水文站预测：
#        - 对每个水文站的流量数据：
#          - 找出(value,timestamp)中value最大的记录
#          - 当洪峰流量 > 1000m³/s时输出
#          - 流量取整数
#
#     【输出格式要求】
#     {
#     "水库调度": [
#         {
#     "名称": "水库名称",
#           "调度过程": "预计[水库名称]将于[yyyy-mm-dd HH:MM:SS]达到最高水位[XXX.XXXX]m"
#         }
#       ],
#       "水文站预测": [
#         {
#     "名称": "站点名称",
#           "调度过程": "预计[yyyy-mm-dd HH:MM:SS]，[站点名称]出现[XXXX]立方米每秒的洪峰流量"
#         }
#       ]
#     }
#
#     【示例数据】
#     水库示例：
#     - 河口村水位从238m升至285.43m
#     - 最高水位出现在2021-07-21 19:59:59
#
#     水文站示例：
#     - 花园口洪峰20606m³/s
#     - 出现在2021-07-22 11:59:59
#
#     【输出要求】
#     1. 只输出最终的JSON格式结果
#     2. 不要包含任何解释或处理过程
#     3. 严格使用指定的字段名和格式
#     4. 时间戳保持原始精度
#     5. 无符合条件数据时返回空列表
#
#     请直接输出符合上述要求的JSON结果：
#     """
#     res = query_question(prompt)
#     print("res:", res)

    # print("skMapData", skMapData)
    # print("swMapData", swMapData)
    # print("date_list", date_list)
    # BASE_URL = "http://10.4.158.35:8093"
    # START_DATE = "2024100308"
    # END_DATE = "2024100408"
    # TIME_SPAN = 24
    # OUTPUT_FILE = "rainfall_echarts.html"
    #
    # try:
    #     # 1. 获取数据
    #     status, data = get_rain_polygon_geojson(BASE_URL, START_DATE, END_DATE, TIME_SPAN)
    #     print("geojson数据为：", data)
    #     # 2. 渲染ECharts图表
    #     chart = render_rainfall_echarts(data, OUTPUT_FILE)
    #
    #     # 3. 可选：直接显示（需Jupyter环境）
    #     from pyecharts.render import make_snapshot
    #     from snapshot_selenium import snapshot
    #     make_snapshot(snapshot, chart.render(), "rainfall.png")
    #
    # except Exception as e:
    #     print(f"程序执行失败: {str(e)}")





prompt_v1 = f"""
    请根据以下水文监测数据生成简洁的水库调度和水文站预测报告，并严格按指定JSON格式输出：

    【输入数据】
    - 水库列表：{sknames}
    - 水文站列表：{swznames}
    - 时间序列：{date_list}

    【数据格式要求】
    1. 水库数据（包含水位、蓄量、流量等）：
    {skMapData}

    2. 水文站数据（包含流量等）：
    {swMapData}

    【分析要求】
    精确匹配时间索引：
       - 水位/流量的第i个值对应时间序列的第i个时刻
       - 例如：date_list[29]对应河口村水位skMapData["河口村"]["水位"][29]

    【输出要求】
    1. 只输出以下两个字段：
       - "水库调度"：包含各水库的最高水位预测
       - "水文站预测"：包含各站的洪峰流量预测

    2. 严格使用以下格式：
    {{
      "水库调度": [
        {{
          "名称": "水库名称",
          "调度过程": "预计[水库名称]将于[yyyy-mm-dd HH:MM:SS]达到最高水位[XXX]m"
        }},
        ...
      ],
      "水文站预测": [
        {{
          "名称": "站点名称",
          "调度过程": "预计[yyyy-mm-dd HH:MM:SS]，[站点名称]出现[XXXX]立方米每秒的洪峰流量"
        }},
        ...
      ]
    }}

    【生成规则】
    1. 时间格式必须统一为：yyyy-mm-dd HH:MM:SS（24小时制）
    2. 水位值保留4位小数，流量值取整数
    3. 只输出有显著变化的水库/水文站（水位变化>0.5m或流量变化>500m³/s）
    4. 若无显著变化，返回空列表
    """

prompt_v2 = f"""
        请根据以下水文监测数据生成简洁的水库调度和水文站预测报告，并严格按指定 JSON 格式输出：

        【输入数据】
        - 水库列表：{sknames}
        - 水文站列表：{swznames}
        - 时间序列：{date_list}

        【数据格式要求】
        1. 水库数据（包含水位、蓄量、流量等）：
        {skMapData}
        2. 水文站数据（包含流量等）：
        {swMapData}

        【分析要求】
        精确匹配时间索引：
           - 水位/流量的第 i 个值对应时间序列的第 i 个时刻
           - 例如：date_list[29]对应河口村水位 skMapData["河口村"]["水位"][29]

        【思维链引导】
        1. 首先，对于每个水库，遍历其水位数据，记录水位的最大值以及对应的时间索引。
        2. 然后，对于每个水文站，遍历其流量数据，记录流量的最大值以及对应的时间索引。
        3. 最后，根据上述标记和记录，生成符合要求的水库调度和水文站预测内容。

        【输出要求】
        1. 只输出以下两个字段：
           - "水库调度"：包含各水库的最高水位预测
           - "水文站预测"：包含各站的洪峰流量预测
        2. 严格使用以下格式：
        {{
          "水库调度": [
            {{
              "名称": "水库名称",
              "调度过程": "预计[水库名称]将于[yyyy-mm-dd HH:MM:SS]达到最高水位[XXX]m"
            }},
            ...
          ],
          "水文站预测": [
            {{
              "名称": "站点名称",
              "调度过程": "预计[yyyy-mm-dd HH:MM:SS]，[站点名称]出现[XXXX]立方米每秒的洪峰流量"
            }},
            ...
          ]
        }}

        【生成规则】
        1. 时间格式必须统一为：yyyy-mm-dd HH:MM:SS（24 小时制）
        2. 水位值保留 4 位小数，流量值取整数
        3. 只输出有显著变化的水库/水文站（水位变化 > 0.5m 或流量变化 > 500m³/s）
        4. 若无显著变化，返回空列表
        """

prompt_v3 = f"""
    请根据以下水文监测数据生成简洁的水库调度和水文站预测报告，并严格按指定 JSON 格式输出：

    【数据输入】
    1. 水库数据（包含水位、蓄量、流量等）：
    {skMapData}
    2. 水文站数据（包含流量等）：
    {swMapData}

    【严格数据匹配要求】
    1. 水库名称严格匹配：{sknames}（仅处理表格中存在的5个水库）
    2. 水文站名称严格匹配：{swznames}（仅处理表格中存在的4个水文站）
    3. 时间格式统一转换为：%Y-%m-%d %H:%M:%S，必须与表格中「时间」列完全一致

    【水库调度分析步骤】
    1. 对每个水库的「水位」列表，找到最大值对应的索引i
    2. 提取{date_list}[i]作为最高水位时间，水位值保留4位小数（不足补0），记录最高水位出现的时间


    【水文站预测分析步骤】
    1. 对每个水文站的「流量」列表，找到最大值对应的索引i
    2. 提取date_list[i]作为洪峰时间，流量值取整数（示例：12381.2→12381）

    【输出格式校验点】
    1. 水库调度数组：每个对象必须包含「名称」和符合格式的「调度过程」
    2. 水文站预测数组：每个对象必须包含「名称」和符合格式的「调度过程」
    3. 严格按表格数据生成，禁止添加表格外的水库/水文站（如西霞院、小花间等表格中无数据）

    【输出要求】
    1. 只输出以下两个字段：
       - "水库调度"：包含各水库的最高水位预测
       - "水文站预测"：包含各站的洪峰流量预测
    2. 严格使用以下格式：
    {{
      "水库调度": [
        {{
          "名称": "水库名称",
          "调度过程": "预计[水库名称]将于[yyyy-mm-dd HH:MM:SS]达到最高水位[XXX]m"
        }},
        ...
      ],
      "水文站预测": [
        {{
          "名称": "站点名称",
          "调度过程": "预计[yyyy-mm-dd HH:MM:SS]，[站点名称]出现[XXXX]立方米每秒的洪峰流量"
        }},
        ...
      ]
    }}

    请根据上述步骤和表格数据，生成严格符合要求的JSON数据。
    """