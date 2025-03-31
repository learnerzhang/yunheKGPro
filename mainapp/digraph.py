import os
os.environ["GRAPHVIZ_DOT_ENCODING"] = "utf-8"  # 在代码开头添加

from graphviz import Digraph

def m1():
    # 创建有向图，设置中文字体支持
    dot = Digraph(name="Weather_Correction_Flow",  format="png", graph_attr={"rankdir": "LR", "fontname": "SimHei"}, node_attr={"style": "filled", "fontname": "SimHei"})
    
    # ----------------------
    # 定义节点（按流程顺序）
    # ----------------------
    # 输入模块
    dot.node("A", "气象数据输入\n(降雨、风速、能见度)",  shape="ellipse", color="#87CEEB")# 天蓝色

    # 模糊化处理
    dot.node("B", "模糊化处理\n- 定义隶属度函数\n- 生成模糊集合",  shape="box", color="#98FB98") # 淡绿色

    # 规则库
    dot.node("C", "规则库构建\n- IF-THEN规则\n- 专家经验+数据挖掘",  shape="box", color="#98FB98") # 淡绿色

    # 模糊推理
    dot.node("D", "模糊推理与解模糊化\n- Mamdani推理\n- 重心法计算α",  shape="box", color="#98FB98") # 淡绿色

    # 输出模块
    dot.node("E", "输出修正系数α\n(动态更新至列车控制系统)", shape="ellipse", color="#87CEEB") # 天蓝色

    # 数据库交互
    dot.node("F", "历史运行数据库\n(查询天气关联延误ΔT)",  shape="cylinder", color="#FFA07A") # 浅橙色

    # 动态更新
    dot.node("G", "动态更新机制\n(每15分钟刷新)",  shape="diamond", color="#FFD700") # 金色

    # ----------------------
    # 定义连接边
    # ----------------------
    dot.edge("A", "B", label="实时数据流")
    dot.edge("B", "C", label="模糊集合")
    dot.edge("C", "D", label="激活规则")
    dot.edge("D", "E", label="修正系数α")
    dot.edge("F", "B", label="历史数据调用", style="dashed")
    dot.edge("G", "E", label="GSM-R通信链路", color="#FF4500") # 橙红色

    # ----------------------
    # 渲染并保存图像
    # ----------------------
    print("# 渲染并保存图像:",dot.source)
    dot.render(filename="weather_correction_flow",  directory="./output",  cleanup=True, view=True) # 自动打开生成的PNG文件


def m2():
    from graphviz import Digraph
    dot = Digraph(name="防汛组织流程图",format="png", graph_attr={"rankdir": "LR", "fontname": "SimHei", 'dpi': '300'}, node_attr={"style": "filled", "fontname": "SimHei"})
    # TB（从上到下，默认）、LR（从左到右）、BT（从下到上）、RL（从右到左）。
    # dot.graph_attr['rankdir'] = 'TB'

    # 节点定义（根据条件分支）
    dot.node("A", shape="box", label="黄河河防总层级", color="#87CEEB")
    dot.node("A1", shape="box", label="指挥决策", color="#87CEEB")
    dot.node("A2", shape="box", label="应急响应启动", color="#87CEEB")
    dot.node("A3", shape="box", label="专业组运行", color="#87CEEB")
    dot.node("A4", shape="box", label="支援部署", color="#87CEEB")

    dot.node("B", shape="box", label="省区防汛指挥机构层级")
    dot.node("B1", shape="box", label="应急动员", color="#98FB98")
    dot.node("B2", shape="box", label="工程调度", color="#87CEEB")
    dot.node("B3", shape="box", label="抢险实施", color="#87CEEB")
    dot.node("B4", shape="box", label="跨部门协调", color="#87CEEB")

    dot.node("TJ", shape="diamond", label="四级预警?")
    
    dot.node("C", shape="box", label="受灾地区各级防汛机构层级")
    # dot.node("省区防汛指挥", shape="diamond", label="Condition?")
    dot.node("C1", shape="box", label="现场指挥", color="#87CEEB")
    dot.node("C2", shape="box", label="社会动员", color="#87CEEB")
    dot.node("C3", shape="box", label="抢险实施", color="#87CEEB")
    dot.node("C4", shape="box", label="基层执行", color="#87CEEB")

    # 边定义（根据条件分支）
    dot.edge("A", "B")
    dot.edge("B", "TJ")
    dot.edge("TJ", "C")

    dot.edge("A", "A1")
    dot.edge("A", "A2")
    dot.edge("A", "A3")
    dot.edge("A", "A4")

    dot.edge("B", "B1")
    dot.edge("B", "B2")
    dot.edge("B", "B3")
    dot.edge("B", "B4")

    dot.edge("C", "C1")
    dot.edge("C", "C2")
    dot.edge("C", "C3")
    dot.edge("C", "C4")

    dot.render("output/防汛组织流程图", cleanup=True, view=False)


if __name__ == "__main__":
    m1()
    m2()
    pass