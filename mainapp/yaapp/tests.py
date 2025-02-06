from django.test import TestCase
import json
from api_yuan import huanghe_shuikushuiqing_generate_dfjson

# Create your tests here.
params = json.load("data/plans/HHZXY_api_data_2024-12-13.json")
res = huanghe_shuikushuiqing_generate_dfjson(context="黄河中下游洪水调度方案")
print(res)