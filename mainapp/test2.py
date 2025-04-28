import requests
import json
from urllib.parse import urljoin
from typing import Tuple, Dict, Any
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import os
from datetime import datetime
def get_rain_polygon_geojson(base_url: str, stdt: str, dt: str, prtime: int) -> Tuple[int, Dict[str, Any]]:
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

def get_china_geojson() -> gpd.GeoDataFrame:
    """获取中国行政区划GeoJSON数据"""
    try:
        # 从本地文件或URL获取中国地图数据
        # 这里使用一个公开的GeoJSON数据源（省级行政区划）
        china_url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
        response = requests.get(china_url, timeout=10)
        response.raise_for_status()
        china_geojson = response.json()
        return gpd.GeoDataFrame.from_features(china_geojson["features"])
    except Exception as e:
        print(f"获取中国地图数据失败: {str(e)}")
        # 如果在线获取失败，可以尝试从本地文件加载
        try:
            return gpd.read_file("data/geojson/china.geojson")  # 假设有本地文件
        except:
            raise Exception("无法加载中国地图数据")


def plot_rainfall_data(geojson_data: Dict[str, Any], output_path: str = None) -> None:
    """
    可视化降雨多边形数据（带中国地图背景）
    修改：将降雨数据颜色设置为绿色

    参数:
        geojson_data: GeoJSON格式的降雨数据
        output_path: 图片保存路径 (可选)
    """
    try:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']
        plt.rcParams['axes.unicode_minus'] = False

        # 获取中国地图数据
        china_gdf = get_china_geojson()

        # 转换降雨数据为GeoDataFrame
        rain_gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

        # 创建图形和坐标轴
        fig, ax = plt.subplots(figsize=(14, 12))

        # 先绘制中国地图背景
        china_gdf.plot(
            ax=ax,
            color="lightgray",
            edgecolor="black",
            linewidth=0.5,
            alpha=0.5
        )

        # 绘制降雨数据（如果有CONTOUR字段）
        if "CONTOUR" in rain_gdf.columns:
            # 计算颜色范围
            vmin = rain_gdf["CONTOUR"].min()
            vmax = rain_gdf["CONTOUR"].max()
            norm = Normalize(vmin=vmin, vmax=vmax)

            # 修改：使用绿色渐变颜色映射
            cmap = plt.get_cmap("Greens")  # 将"Blues"改为"Greens"

            # 绘制降雨多边形
            rain_gdf.plot(
                ax=ax,
                column="CONTOUR",
                cmap=cmap,
                norm=norm,
                alpha=0.7,
                edgecolor="none",
                legend=False
            )

            # 添加颜色条
            sm = ScalarMappable(norm=norm, cmap=cmap)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, shrink=0.6)
            cbar.set_label("降雨量 (mm)")
        else:
            # 如果没有CONTOUR字段，使用统一颜色（改为绿色）
            rain_gdf.plot(
                ax=ax,
                color="green",  # 将"blue"改为"green"
                alpha=0.5
            )

        # 设置图形属性
        # title = f"降雨分布图\n时间范围: {geojson_data.get('name', '未知')}"
        # ax.set_title(title, fontsize=16, pad=20)
        # ax.set_xlabel("经度", fontsize=12)
        # ax.set_ylabel("纬度", fontsize=12)
        # 删除x轴和y轴的标签和刻度
        ax.set_xticks([])  # 删除x轴刻度
        ax.set_yticks([])  # 删除y轴刻度
        ax.set_xlabel("")  # 删除x轴标签
        ax.set_ylabel("")  # 删除y轴标签
        # 设置显示范围为中国大陆大致范围
        ax.set_xlim(70, 140)
        ax.set_ylim(15, 55)

        # 添加网格
        ax.grid(True, linestyle='--', alpha=0.5)

        # 保存或显示
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"地图已保存到: {output_path}")

        plt.tight_layout()
        #plt.show()

    except ImportError:
        print("可视化需要安装 geopandas 和 matplotlib")
        print("请运行: pip install geopandas matplotlib")
    except Exception as e:
        print(f"可视化失败: {str(e)}")


def generate_rainfall_map(start_date: str, end_date: str, time_span: int, sequence_num: int = 1,
                          output_folder: str = None):
    """
    生成并保存降雨地图

    参数:
        start_date: 开始日期，格式YYYYMMDDHH
        end_date: 结束日期，格式YYYYMMDDHH
        time_span: 时间跨度(小时)
        sequence_num: 序列号，一般为1,2,3,4,5等 (默认1)
        output_folder: 输出文件夹路径，如果为None则使用当前日期
    """
    BASE_URL = "http://10.4.158.35:8093"

    # 确定输出文件夹
    if output_folder is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_folder = os.path.join("data", "yuan_data", "4", "yubao", today)

    # 创建文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 生成输出文件名，加入序列号
    output_filename = f"{sequence_num}.png"
    output_path = os.path.join(output_folder, output_filename)

    # 获取数据
    status, data = get_rain_polygon_geojson(BASE_URL, start_date, end_date, time_span)
    print("data:",data)
    if status == 200:
        print("成功获取数据！")
        print(f"包含 {len(data['features'])} 个特征")

        # 可视化并保存
        plot_rainfall_data(data, output_path)
        return True, output_path
    else:
        print(f"失败 (状态码 {status}): {data}")
        if "JSON" in str(data.get("error", "")):
            print("\n调试信息：")
            print(f"错误位置: {data.get('position')}")
            print(f"错误上下文: {data.get('context')}")
            print(f"响应片段: {data.get('full_response')}")
        return False, None

def download_map_images(base_url="http://10.4.158.34:8090/iserver/services/map-YRGP_YLH_2D_ZT/rest/maps",
                        start_num=18, end_num=24, output_dir="data/yuan_data/4/yubao"):
    """
    下载从T7_{start_num}到T7_{end_num}的地图图片，保存为1.png到N.png

    参数:
        base_url (str): 地图服务基础URL（不包含编号）
        start_num (int): 起始编号（如18）
        end_num (int): 结束编号（如24）
        output_dir (str): 保存图片的基础目录（会自动追加日期）
    """
    # 获取当前日期（格式：年-月-日）
    today = datetime.now().strftime("%Y-%m-%d")
    full_output_dir = os.path.join(output_dir, today)

    # 判断目录是否存在，不存在则创建
    if not os.path.exists(full_output_dir):
        os.makedirs(full_output_dir)
        #print(f"目录 {full_output_dir} 不存在，已创建")
    else:
        print(f"目录 {full_output_dir} 已存在，直接使用")

    # 确保编号范围有效
    if start_num > end_num:
        #print("错误：起始编号不能大于结束编号")
        return

    for i, map_num in enumerate(range(start_num, end_num + 1), start=1):
        # 构造完整URL
        map_name = f"T7_{map_num}"
        url = f"{base_url}/{map_name}/entireImage.jpg"
        filename = os.path.join(full_output_dir, f"{i}.png")

        # 发送请求
        # print(f"\n正在处理 {map_name}...")
        # print(f"URL: {url}")
        # print(f"将保存为: {filename}")

        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # 检查请求是否成功

            # 保存图片
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            #print(f"✅ 成功保存 {filename} (大小: {os.path.getsize(filename) / 1024:.1f} KB)")
        except requests.exceptions.RequestException as e:
            #print(f"❌ 下载失败: {str(e)}")
            # 如果失败，删除可能存在的空文件
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    # download_map_images()
    BASE_URL = "http://10.4.158.35:8093"
    START_DATE = "2024071008"
    END_DATE = "2024071108"
    TIME_SPAN = 24#24
    generate_rainfall_map("2024071008", "2024071108", 24, sequence_num=1)
    status, data = get_rain_polygon_geojson(BASE_URL, START_DATE, END_DATE, TIME_SPAN)

    if status == 200:
        print("成功获取数据！")
        print(f"包含 {len(data['features'])} 个特征")

        # 可视化
        plot_rainfall_data(data, "rainfall_map_with_china_green_copy.png")  # 修改输出文件名以反映绿色主题
    else:
        print(f"失败 (状态码 {status}): {data}")

        # 如果是JSON解析错误，输出更多细节
        if "JSON" in str(data.get("error", "")):
            print("\n调试信息：")
            print(f"错误位置: {data.get('position')}")
            print(f"错误上下文: {data.get('context')}")
            print(f"响应片段: {data.get('full_response')}")