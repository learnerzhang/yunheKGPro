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

from yaapp.base_data import BaseDataFactory
#from mainapp.yaapp.base_data import BaseDataFactory

class LYHDataFactory(BaseDataFactory):

    def __init__(self, dataType=0):
        super().__init__(dataType)
    
    def getYuQingData(self):
        """
            获取雨情数据
        """
        print("HHZXY getYuQingData")
        return {}

    def getHedaoShuiQingData(self):
        """
            获取河道水情数据
        """
        print("HHZXY getHedaoShuiQingData")
        return {}

    def getShuiKuShuiQingData(self):
        """
            获取水库水情数据
        """
        print("HHZXY getShuiKuShuiQingData")
        return {}

    def getGongQingXianQingData(self):
        """
            工情险情
        """
        print("HHZXY getGongQingXianQingData")
        return {}
    
    def getJiangYuYuBaoData(self):
        """
            降雨预报
        """
        print("HHZXY getJiangYuYuBaoData")
        return {}
    
    def getDiaoDuFangAnData(self):
        """
            调度方案
        """
        print("HHZXY getDiaoDuFangAnData")
        return {}

    def getGongChengYanPanData(self):
        """
            工程研判
        """
        print("HHZXY getGongChengYanPanData")
        return {}
    
    def getShuNiuYingYongData(self):
        """
            枢纽运用方案
        """
        print("HHZXY getShuNiuYingYongData")
        return {}

    def getAnQuanJuChuoData(self):
        """
            安全举措
        """
        print("HHZXY getAnQuanJuChuoData")
        return {}
    
    def buildJsonData(self):
        super().buildJsonData()

# if __name__ == "__main__":
#     LYHDataFactory(dataType=4).buildJsonData()