import requests
from urllib.parse import urljoin
import json
from typing import Tuple, Dict, Any
import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matplotlib.colors import Normalize

from typing import Tuple, Dict, Any
import requests
import json

def get_qb_forprgis(base_url: str, stdt: str) -> Tuple[int, Dict[str, Any]]:
    """
    获取降水预报等值面的查询结果列表（QB_FORPRGIS）

    参数:
        base_url (str): API 基础地址
        stdt (str): 预报制作时间（格式：YYYYMMDDHH 或 YYYYMMDD，支持后缀模糊匹配）

    返回:
        Tuple[int, Dict]: (HTTP状态码, 响应数据)
    """
    endpoint = "/api/v1/ybrain/GetQB_FORPRGIS"
    url = f"{base_url}{endpoint}"
    print("url:",url)
    # 请求参数
    params = {"stdt": stdt}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.text.strip()

        # 特殊处理：如果返回的是字符串形式的 JSON，先去除首尾引号并转义
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        content = content.encode().decode('unicode_escape')

        # 解析为 Python 对象
        result = json.loads(content)

        # 包装成标准结构返回
        return response.status_code, {
            "status": "success",
            "data": result
        }

    except requests.exceptions.RequestException as e:
        return 500, {
            "status": "error",
            "message": f"请求失败: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return 500, {
            "status": "error",
            "message": f"JSON解析失败: {str(e)}",
            "raw_response": content
        }
    except Exception as e:
        return 500, {
            "status": "error",
            "message": f"未知错误: {str(e)}"
        }

def get_rain_polygon_geojson_v2(base_url: str, stdt: str, dt: str, prtime: int) -> Tuple[int, Dict[str, Any]]:
    """
    获取标准化降雨多边形GeoJSON数据（自动添加CRS并验证数据结构）

    参数:
        base_url: API基础地址
        stdt: 起始时间(YYYYMMDDHH)
        dt: 结束时间(YYYYMMDDHH)
        prtime: 时间间隔(小时)

    返回:
        (状态码, 标准化GeoJSON)
    """
    endpoint = "/api/v1/ybrain/GetRainPolygonGeojson"
    url = urljoin(base_url, endpoint)
    params = {"stdt": stdt, "dt": dt, "prtime": str(prtime)}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.text.strip()

        # 处理响应内容
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        content = content.encode().decode('unicode_escape')

        geojson = json.loads(content)

        if not isinstance(geojson.get("features"), list):
            raise ValueError("无效的FeatureCollection结构")

        # 添加 CRS 信息
        geojson.setdefault("crs", {
            "type": "name",
            "properties": {"name": "EPSG:4326"}
        })

        return response.status_code, geojson

    except Exception as e:
        return (500, {"error": str(e)})


# def load_geojson_with_crs(file_path: str, default_crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
#     """加载GeoJSON文件并确保有CRS"""
#     gdf = gpd.read_file(file_path)
#     if gdf.crs is None:
#         gdf = gdf.set_crs(default_crs)
#     return gdf.to_crs("EPSG:4326")
from matplotlib.colors import ListedColormap, BoundaryNorm
import warnings
import numpy as np
def plot_unified_map(
        rainfall_geojson: Dict[str, Any],
        basin_geojson_path: str,
        river_geojson_path: str,
        output_path: str = None
):
    try:
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['axes.labelsize'] = 1  # 隐藏图例标签文字

        # 忽略 Matplotlib 的警告
        warnings.filterwarnings("ignore")

        # 加载雨量面数据并修复几何
        rain_gdf = gpd.GeoDataFrame.from_features(
            rainfall_geojson["features"],
            crs="EPSG:4326"
        )
        rain_gdf = rain_gdf.set_geometry(rain_gdf.geometry.buffer(0))  # 修复几何

        # 加载流域和河流 GeoJSON 文件
        def load_geojson_with_crs(path):
            return gpd.read_file(path).to_crs("EPSG:4326")

        basin_gdf = load_geojson_with_crs(basin_geojson_path)
        river_gdf = load_geojson_with_crs(river_geojson_path)

        # 裁剪降雨数据到流域范围内
        rain_in_basin = gpd.clip(rain_gdf, basin_gdf.unary_union)

        # 创建绘图
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.set_facecolor('white')

        # 绘制流域边界
        basin_gdf.plot(ax=ax, color="lightgray", edgecolor="black", linewidth=0.5, alpha=0.5)

        # 定义降雨量等级与颜色
        bins = [0, 0.1, 10, 25, 50, 100, 250, np.inf]
        colors = ['white', '#eaffcc', '#b3f7a1', '#88d8ff', '#007fff', '#ff3300', '#9900cc']
        cmap = ListedColormap(colors)
        norm = BoundaryNorm(boundaries=bins, ncolors=len(colors))

        # 可视化降雨量，使用自定义分级
        if "CONTOUR" in rain_in_basin.columns:
            rain_plot = rain_in_basin.plot(
                ax=ax,
                column="CONTOUR",
                cmap=cmap,
                norm=norm,
                edgecolor='gray',
                linewidth=0.5,
                legend=False,
                legend_kwds={
                    "label": "",  # 去除标题
                    "shrink": 0.6,
                    "ticks": [(b + bins[i+1])/2 for i, b in enumerate(bins[:-1])],  # 中心点作为刻度
                    "values": bins[:-1],  # 显示范围
                    "format": "%.1f"
                }
            )

            # 自定义图例文本（可选）
            labels = ['0 - 0.1 mm', '0.1 - 10 mm', '10 - 25 mm', '25 - 50 mm',
                      '50 - 100 mm', '100 - 250 mm', '>250 mm']

            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor=color, edgecolor='gray', label=label)
                for color, label in zip(colors, labels)
            ]
            ax.legend(handles=legend_elements, loc='upper left', fontsize=8)

        else:
            rain_in_basin.plot(ax=ax, color="lightgreen", edgecolor="green", alpha=0.5)

        # 河流网络
        river_gdf.plot(ax=ax, color="darkblue", linewidth=0.8, label="河流网络")

        # 设置绘图范围为流域边界
        bounds = basin_gdf.total_bounds
        padding = 0.05
        ax.set_xlim(bounds[0] - padding, bounds[2] + padding)
        ax.set_ylim(bounds[1] - padding, bounds[3] + padding)

        # 图题
        ax.set_title("伊洛河流域降雨分布图", fontsize=14)

        # 显示或保存图像
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        #plt.show()

    except Exception as e:
        print(f"绘图错误: {str(e)}")
        import traceback
        traceback.print_exc()
import os
from datetime import datetime
from typing import List, Dict, Any

def generate_rainfall_maps(stdt: str, output_folder: str = None):
    """
    根据给定的预报时间获取多个降水预报并生成地图图片

    参数:
        stdt (str): 预报制作时间，格式 YYYYMMDDHH 或 YYYYMMDD
        output_folder (str): 输出文件夹路径，如果为None则使用当前日期

    返回:
        List[str]: 成功生成的地图文件路径列表
    """
    BASE_URL = "http://10.4.158.35:8093"

    # 设置默认输出目录
    if output_folder is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_folder = os.path.join("data", "yuan_data", "4", "yubao", today)

    os.makedirs(output_folder, exist_ok=True)

    # 1. 获取预报任务列表
    status_code, result = get_qb_forprgis(base_url=BASE_URL, stdt=stdt)
    #print("result:", result)

    if status_code != 200 or result.get("status") != "success":
        print(f"获取预报任务失败: {result.get('message')}")
        return []

    tasks: List[Dict] = result.get("data", [])
    if not tasks:
        print("没有找到符合条件的预报任务。")
        return []

    #print(f"共找到 {len(tasks)} 个预报任务，开始逐个生成降雨图...")

    image_paths = []

    # 2. 遍历所有任务，生成降雨图
    for idx, task in enumerate(tasks, start=1):
        proid = task.get("PROID")
        st_dt = task.get("STDT")
        dt = task.get("DT")
        prtime = task.get("PRTIME")

        #print(f"\n处理第 {idx} 个任务：{proid} | STDT={st_dt}, DT={dt}, PRTIME={prtime}")

        # 获取降雨面数据
        status, rain_data = get_rain_polygon_geojson_v2(
            base_url=BASE_URL,
            stdt=st_dt,
            dt=dt,
            prtime=prtime
        )
        #print("rain_data", rain_data)

        if status != 200:
            print(f"获取降雨数据失败: {rain_data.get('error')}")
            continue

        # 定义流域和河流 GeoJSON 文件路径
        BASIN_FILE = "data/geojson/洛河流域.json"
        RIVER_FILE = "data/geojson/WTRIVRL25_洛河流域.json"

        # 生成图片名称
        output_path = os.path.join(output_folder, f"{idx}.png")

        # 调用统一绘图函数
        try:
            plot_unified_map(
                rainfall_geojson=rain_data,
                basin_geojson_path=BASIN_FILE,
                river_geojson_path=RIVER_FILE,
                output_path=output_path
            )
            image_paths.append(output_path)
            print(f"✅ 第 {idx} 张图已保存至: {output_path}")
        except Exception as e:
            print(f"❌ 绘图失败 (任务 {idx}): {e}")

    return image_paths
# 使用示例
if __name__ == "__main__":
    # 1. 获取降雨数据
    # BASE_URL = "http://10.4.158.35:8093"
    # stdt = "2025042808"
    #
    # status_code, result = get_qb_forprgis(base_url=BASE_URL, stdt=stdt)
    # print("result:",result)
    # status, rain_data = get_rain_polygon_geojson_v2(
    #     BASE_URL,"2025042808", "2025050508", 168# "2025050708", "2025050808", 24#
    # )
    # # status, rain_data = get_rain_polygon_geojson_v2(
    # #     BASE_URL, "2025042808", "2025042908", 24  # "2025050708", "2025050808", 24#
    # # )
    # print("rain_data", rain_data)
    # if status != 200:
    #     print(f"获取降雨数据失败: {rain_data.get('error')}")
    #     exit()
    #
    # # 2. 定义本地GeoJSON路径
    # BASIN_FILE = "data/geojson/洛河流域.json"
    # RIVER_FILE = "data/geojson/WTRIVRL25_洛河流域.json"
    #
    # # 3. 绘制统一地图
    # plot_unified_map(
    #     rainfall_geojson=rain_data,
    #     basin_geojson_path=BASIN_FILE,
    #     river_geojson_path=RIVER_FILE,
    #     output_path="unified_rainfall_map.png"
    # )
    stdt = "2025042808"  # 支持模糊匹配，如 "20250428"

    # 调用主函数生成降雨图
    image_files = generate_rainfall_maps(stdt=stdt)

    # 打印生成结果
    print("\n生成完成，以下图片已成功保存：")
    for f in image_files:
        print(f)
