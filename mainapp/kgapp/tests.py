from django.test import TestCase

# Create your tests here.
from yunheKGPro.neo import Neo4j
import pandas as pd
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunheKGPro.settings')
# neo4j = Neo4j()
# res =neo4j.entityLabels()
# print(res)

sheets = pd.read_excel(io="../media/docs/template.xlsx", sheet_name=None, keep_default_na=False)
for kEntType, vDat in sheets.items():
    print("aaaaaaaaa:",kEntType)
    print("bbbbbbbbb:",vDat)