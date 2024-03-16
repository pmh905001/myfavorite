import json
import random
import time

import requests

def send_msgs():
    url = 'https://www.toutiao.com/article/7341212957709238794'
    headers={
    'authority': 'www.toutiao.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1'
    }
    for i in range(1):
        response = requests.get(url, headers=headers)
        time.sleep(random.randint(1, 10))
        print(response.text)


if __name__ == '__main__':
    send_msgs()





