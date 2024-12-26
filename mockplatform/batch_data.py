import collections
import requests
from bs4 import BeautifulSoup
import json
import os

import django
from django.forms import model_to_dict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mockplatform.settings")
django.setup()

from hydapp.models import *


sw_stcds = [('40105150', '花园口'), ('40104450', '三门峡'), ('40104360', '潼关'), ('40104730', '西霞院')]
sk_stcds = [('40104720', '西霞院'), ('40104690', '小浪底')]


if __name__ == '__main__':
    pass

