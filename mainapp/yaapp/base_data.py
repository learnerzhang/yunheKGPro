# coding=utf-8

from django.forms import model_to_dict
from pydantic import BaseModel
from typing import List
import os
import json
from docx.shared import Mm
from docx import Document
from datetime import datetime
from datetime import date
import pandas as pd
from io import StringIO
import requests
import json
import codecs

class BaseDataFactory():

    def __init__(self, dataType=0):
        self.dataType = dataType
        self.date = date.today()
        self.dataJsonPool = {}
        pass
    
    def getYuQingData(self):
        """
            获取雨情数据
        """
        print("getYuQingData")
        return {}

    def getHedaoShuiQingData(self):
        """
            获取河道水情数据
        """
        print("getHedaoShuiQingData")
        return {}

    def getShuiKuShuiQingData(self):
        """
            获取水库水情数据
        """
        print("getShuiKuShuiQingData")
        return {}

    def getGongQingXianQingData(self):
        """
            工情险情
        """
        print("getGongQingXianQingData")
        return {}
    
    def getJiangYuYuBaoData(self):
        """
            降雨预报
        """
        print("getJiangYuYuBaoData")
        return {}
    
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

        # 获取可执行的方法
        for method_name in dir(self):
            # 仅需要执行get开头的自定义方法
            if callable(getattr(self, method_name)) and method_name.startswith("get"):
                # 执行方法
                result = getattr(self, method_name)()
                self.dataJsonPool.update(result)  # 合并数据
        
        print("收集数据执行结束")
        print("开始执行持久化操作")
        if self.dataType == 0:
            # 黄河中下游
            jsonFileName = f"data/plans/HHZXY_api_data_{self.date}.json"
        elif self.dataType ==1:
            # 小浪底秋汛
            jsonFileName = f"data/plans/XLDQX_api_data_{self.date}.json"
        elif self.dataType ==2:
            jsonFileName = f"data/plans/XLDTSTS_api_data_{self.date}.json"
        elif self.dataType ==3:
            jsonFileName = f"../data/plans/SHJ_api_data_{self.date}.json"

        with codecs.open(jsonFileName, "w", "utf-8") as f:
            json.dump(self.dataJsonPool, f, ensure_ascii=False, indent=4)
        print("持久化完成")
