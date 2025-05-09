import requests
import json
from urllib.parse import urljoin
from typing import Tuple, Dict, Any
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
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


def create_flood_control_plan(uid=1, text="伊洛河流域防汛调度初步方案", date=None, base_url="http://127.0.0.1:8000"):
    """
    创建防汛预案并返回预案ID（带默认参数）

    参数:
        uid (int): 用户ID，默认为1
        text (str): 预案名称/文本，默认为"伊洛河防汛预案"
        date (str): 日期，格式为"YYYY-MM-DD"，默认为当天日期
        base_url (str): API基础URL，默认为"http://127.0.0.1:8000"

    返回:
        int: 创建的预案ID
        None: 如果创建失败
    """
    # 如果没有提供日期，则使用当天日期
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    url = f"{base_url}/yaapp/yuAnUserRecom"
    payload = {
        "uid": uid,
        "text": text,
        "date": date
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查HTTP错误

        data = response.json()
        if data.get("success") and data.get("data"):
            return data["data"]["id"]
        else:
            print(f"创建失败: {data.get('msg', '未知错误')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"解析响应数据出错: {e}")
        return None


def call_llm_yuan_user_plan(ptid: int = 0, base_url: str = "http://127.0.0.1:8000"):
    """
    调用 /yaapp/llmYuANUserPlan 接口

    参数:
        ptid (int): 预案类型ID，默认为0
        base_url (str): API基础URL，默认为"http://127.0.0.1:8000"

    返回:
        dict: 包含完整API响应数据的字典
        None: 如果请求失败
    """
    url = f"{base_url}/yaapp/llmYuANUserPlan"
    payload = {"ptid": ptid}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {str(e)}")
        return None
    except ValueError as e:
        print(f"JSON解析失败: {str(e)}")
        return None

def call_llm_yuan_user_word(id: int = 0, base_url: str = "http://127.0.0.1:8000"):
    """
    调用 /yaapp/makeUserYuAnWord 接口

    参数:
        ptid (int): 预案类型ID，默认为0
        base_url (str): API基础URL，默认为"http://127.0.0.1:8000"

    返回:
        dict: 包含完整API响应数据的字典
        None: 如果请求失败
    """
    url = f"{base_url}/yaapp/makeUserYuAnWord"
    payload = {"id": id}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查HTTP错误
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {str(e)}")
        return None
    except ValueError as e:
        print(f"JSON解析失败: {str(e)}")
        return None


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
        #plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']
        plt.rcParams['font.sans-serif'] = [
            'WenQuanYi Micro Hei',  # 文泉驿微米黑
            'Noto Sans CJK JP',  # Noto 日文（兼容简体中文）
            'Noto Serif CJK JP'  # Noto 衬线体
        ]
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