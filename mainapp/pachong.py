import requests
from bs4 import BeautifulSoup
import os
import urllib.request

for i in range(1, 387):
    print("正在下载第{}张图片".format(i))
    # 目标网站的URL
    url = f'http://10.4.58.17/resource/preview/2021001/{i}.webp'



    urllib.request.urlretrieve(url, f"images/{i}.png")
    print('Image downloading completed.')