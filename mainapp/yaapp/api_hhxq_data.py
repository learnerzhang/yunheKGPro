# coding=utf-8

from django.forms import model_to_dict
from pydantic import BaseModel
from typing import List
import os
import json
from docx.shared import Mm
from docx import Document
from datetime import datetime, timedelta
from datetime import date
import pandas as pd
from io import StringIO
import requests
import json
import codecs
import random

from mainapp.yaapp.base_data import BaseDataFactory

class HHXQDataFactory(BaseDataFactory):

    def __init__(self, dataType=0):
        super().__init__(dataType)
    
    def getYuQingData(self):
        """
            获取雨情数据
        """
        print("getYuQingData")
        weather_options = ["晴天", "多云", "小雨", "中雨", "大雨", "暴雨", "雷阵雨", "阴天", "小雪", "中雪", "大雪"]

        # 随机选择天气描述
        huanghe_weather = random.choice(weather_options)
        lanzhou_weather = random.choice(weather_options)
        yuliang = f"最大点雨量出现在黄河上游凉坪站和石骨岔站，均为{random.randint(5, 50)}毫米。"

        # 返回生成的字典
        return {
            "huanghe_weather": huanghe_weather,
            "lanzhou_weather": lanzhou_weather,
            "yuliang": yuliang
        }

    def getHedaoShuiQingData(self):
        """
            获取河道水情数据
        """
        print("getHedaoShuiQingData")
        hdsq = [
            {"站名": "唐乃亥", "当日8时流量(m³/s)": 881.0},
            {"站名": "兰州", "当日8时流量(m³/s)": 1090.0},
            {"站名": "石嘴山", "当日8时流量(m³/s)": 764.0},
            {"站名": "巴彦高勒", "当日8时流量(m³/s)": 526.0},
            {"站名": "包头", "当日8时流量(m³/s)": 461.0},
            {"站名": "头道拐", "当日8时流量(m³/s)": 397.0},
            {"站名": "龙门", "当日8时流量(m³/s)": 273.0},
            {"站名": "潼关", "当日8时流量(m³/s)": 364.0},
            {"站名": "三门峡", "当日8时流量(m³/s)": 111.0},
            {"站名": "小浪底", "当日8时流量(m³/s)": 680.0},
            {"站名": "花园口", "当日8时流量(m³/s)": 668.0},
            {"站名": "夹河滩", "当日8时流量(m³/s)": 885.0},
            {"站名": "高村", "当日8时流量(m³/s)": 1180.0},
            {"站名": "孙口", "当日8时流量(m³/s)": 1230.0},
            {"站名": "艾山", "当日8时流量(m³/s)": 1240.0},
            {"站名": "泺口", "当日8时流量(m³/s)": 906.0},
            {"站名": "利津", "当日8时流量(m³/s)": 562.0},
            {"站名": "华县", "当日8时流量(m³/s)": 84.1},
            {"站名": "黑石关", "当日8时流量(m³/s)": 155.0},
            {"站名": "武陟", "当日8时流量(m³/s)": 13.2}
        ]

        # 对每个站点的流量进行随机波动
        for station in hdsq:
            original_flow = station["当日8时流量(m³/s)"]
            # 随机波动 ±5，且确保不为负值
            fluctuation = random.uniform(-5, 5)
            new_flow = max(0, original_flow + fluctuation)  # 确保流量不为负
            station["当日8时流量(m³/s)"] = round(new_flow, 1)  # 保留一位小数

        return {"hdsq": hdsq}

    def getShuiKuShuiQingData(self):
        """
            获取水库水情数据
        """
        print("getShuiKuShuiQingData")
        sksq = [
            {"水库名称": "龙羊峡", "水位（m）": 2583.94, "蓄量（亿m³）": 180.13, "汛限水位（m）": 2600,
             "相应蓄量（亿m³）": 242.85, "超蓄水量（亿m³）": -29.1, "剩余防洪库容（亿m³）": -29.1},
            {"水库名称": "刘家峡", "水位（m）": 1720.54, "蓄量（亿m³）": 22.89, "汛限水位（m）": 1735,
             "相应蓄量（亿m³）": 39.93, "超蓄水量（亿m³）": -14.01, "剩余防洪库容（亿m³）": -14.01},
            {"水库名称": "万家寨", "水位（m）": 964.53, "蓄量（亿m³）": 2.65, "汛限水位（m）": 305, "相应蓄量（亿m³）": 0.35,
             "超蓄水量（亿m³）": -0.25, "剩余防洪库容（亿m³）": -0.25},
            {"水库名称": "三门峡", "水位（m）": 304.46, "蓄量（亿m³）": 0.801, "汛限水位（m）": 305, "相应蓄量（亿m³）": 0.35,
             "超蓄水量（亿m³）": -0.25, "剩余防洪库容（亿m³）": -0.25},
            {"水库名称": "小浪底", "水位（m）": 226.57, "蓄量（亿m³）": 6.07, "汛限水位（m）": 248, "相应蓄量（亿m³）": 35.47,
             "超蓄水量（亿m³）": 37.3, "剩余防洪库容（亿m³）": 37.3},
            {"水库名称": "陆浑", "水位（m）": 315.08, "蓄量（亿m³）": 4.974, "汛限水位（m）": 317.5, "相应蓄量（亿m³）": 5.87,
             "超蓄水量（亿m³）": -0.21, "剩余防洪库容（亿m³）": -0.21},
            {"水库名称": "故县", "水位（m）": 521.44, "蓄量（亿m³）": 4.24, "汛限水位（m）": 534.3, "相应蓄量（亿m³）": 6.16,
             "超蓄水量（亿m³）": -0.98, "剩余防洪库容（亿m³）": -0.98},
            {"水库名称": "河口村", "水位（m）": 231.8, "蓄量（亿m³）": 0.6766, "汛限水位（m）": 275, "相应蓄量（亿m³）": 2.51,
             "超蓄水量（亿m³）": 0.04, "剩余防洪库容（亿m³）": 0.04},
            {"水库名称": "东平湖", "水位（m）": 42.05, "蓄量（亿m³）": 3.34, "汛限水位（m）": 41.72, "相应蓄量（亿m³）": 6.15,
             "超蓄水量（亿m³）": 0.08, "剩余防洪库容（亿m³）": 0.08}
        ]

        # 对每个水库的数据进行随机波动
        for reservoir in sksq:
            # 随机波动水位（m）
            reservoir["水位（m）"] = round(reservoir["水位（m）"] + random.uniform(-1, 1), 2)

            # 随机波动蓄量（亿m³）
            reservoir["蓄量（亿m³）"] = round(reservoir["蓄量（亿m³）"] + random.uniform(-0.5, 0.5), 3)

            # 随机波动汛限水位（m）
            reservoir["汛限水位（m）"] = round(reservoir["汛限水位（m）"] + random.uniform(-0.5, 0.5), 2)

            # 随机波动相应蓄量（亿m³）
            reservoir["相应蓄量（亿m³）"] = round(reservoir["相应蓄量（亿m³）"] + random.uniform(-0.5, 0.5), 2)

            # 计算超蓄水量（亿m³）
            reservoir["超蓄水量（亿m³）"] = round(reservoir["蓄量（亿m³）"] - reservoir["相应蓄量（亿m³）"], 2)

            # 计算剩余防洪库容（亿m³）
            reservoir["剩余防洪库容（亿m³）"] = round(reservoir["相应蓄量（亿m³）"] - reservoir["蓄量（亿m³）"], 2)

        return {"sksq": sksq}

    def getGongQingXianQingData(self):
        """
            工情险情
        """
        print("getGongQingXianQingData")
        current_date = datetime.now()

        # 随机生成日均流量和水量
        tng_rjll = f"{random.randint(1200, 1350)}～{random.randint(1250, 1400)}m3/s"
        tng_zhl = f"{round(random.uniform(7.0, 8.0), 2)}亿m3"
        llqujian = f"{round(random.uniform(1.0, 1.5), 2)}亿m3"
        llqj = f"{round(random.uniform(1.0, 1.3), 2)}亿m3"
        tgd_rjll = f"{random.randint(350, 550)}～{random.randint(450, 650)}m3/s"
        tg_rjll = f"{random.randint(450, 650)}～{random.randint(550, 750)}m3/s"

        # 随机生成历史流量数据
        lsyg = []
        for i in range(7):
            date = (current_date - timedelta(days=6 - i)).strftime("%Y/%m/%d")  # 从当前日期往前推7天
            data = {
                "日期": date,
                "唐乃亥": random.randint(1200, 1350),
                "龙刘区间": random.randint(180, 250),
                "刘兰区间": random.randint(160, 220),
                "头道拐": random.randint(350, 550),
                "潼关": random.randint(450, 650),
                "小花区间": random.randint(20, 35)
            }
            lsyg.append(data)

        # 计算 7 天总水量
        total_data = {
            "日期": "7天总水量（亿m3）",
            "唐乃亥": round(sum([d["唐乃亥"] for d in lsyg]) / 10000, 2),  # 转换为亿m³
            "龙刘区间": round(sum([d["龙刘区间"] for d in lsyg]) / 10000, 2),
            "刘兰区间": round(sum([d["刘兰区间"] for d in lsyg]) / 10000, 2),
            "头道拐": round(sum([d["头道拐"] for d in lsyg]) / 10000, 2),
            "潼关": round(sum([d["潼关"] for d in lsyg]) / 10000, 2),
            "小花区间": round(sum([d["小花区间"] for d in lsyg]) / 10000, 2)
        }
        lsyg.append(total_data)

        # 返回生成的字典
        return {
            "tng_rjll": tng_rjll,
            "tng_zhl": tng_zhl,
            "llqujian": llqujian,
            "llqj": llqj,
            "tgd_rjll": tgd_rjll,
            "tg_rjll": tg_rjll,
            "lsyg": lsyg
        }
    
    def getJiangYuYuBaoData(self):
        """
            降雨预报
        """
        print("getJiangYuYuBaoData")
        qh_aqghll = f"{random.randint(3500, 4000)}m3/s"  # 青海河段
        gs_aqghll = f"{random.randint(3600, 4100)}m3/s"  # 甘肃河段
        nx_aqghll = f"{random.randint(5500, 6000)}m3/s"  # 宁夏河段
        nm_aqghll = f"{random.randint(5400, 5900)}m3/s"  # 内蒙古河段
        xbgl_aqghll = f"{random.randint(2900, 3200)}m3/s"  # 小北干流
        hhxx_aqghll = f"{random.randint(4500, 4800)}m3/s"  # 黄河下游

        # 返回生成的字典
        return {
            "qh_aqghll": qh_aqghll,
            "gs_aqghll": gs_aqghll,
            "nx_aqghll": nx_aqghll,
            "nm_aqghll": nm_aqghll,
            "xbgl_aqghll": xbgl_aqghll,
            "hhxx_aqghll": hhxx_aqghll
        }
    
    def getDiaoDuFangAnData(self):
        """
            调度方案
        """
        print("getDiaoDuFangAnData")
        return {}

    def getGongChengYanPanData(self):
        """
            工程研判
        """
        print("getGongChengYanPanData")
        return {}
    
    def getShuNiuYingYongData(self):
        """
            枢纽运用方案
        """
        print("getShuNiuYingYongData")
        return {}

    def getAnQuanJuChuoData(self):
        """
            安全举措
        """
        print("getAnQuanJuChuoData")
        return {}
    
    def buildJsonData(self):
        super().buildJsonData()


if __name__=="__main__":
    HHXQDataFactory(dataType=3).buildJsonData()