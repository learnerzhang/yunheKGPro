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

from mainapp.yaapp.base_data import BaseDataFactory

class SHJDataFactory(BaseDataFactory):

    def __init__(self, dataType=0):
        super().__init__(dataType)
    
    def getYuQingData(self):
        """
            获取雨情数据
        """
        print("getYuQingData")
        return {"huanghe_weather": "小雨"}

    def getHedaoShuiQingData(self):
        """
            获取河道水情数据
        """
        print("getHedaoShuiQingData")
        return {"HedaoShuiQingData": "河道水情"}

    def getShuiKuShuiQingData(self):
        """
            获取水库水情数据
        """
        print("getShuiKuShuiQingData")
        return {"ShuiKuShuiQingDatar": "水库水清"}

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
        super().buildJsonData()


if __name__=="__main__":
    SHJDataFactory(dataType=3).buildJsonData()