# coding=utf-8
import json
import random
import time

import requests


def read_cookie():
    with open('cookie.txt', 'r') as f:
        cookie = f.read().split(':')
    return {cookie[0]: cookie[1]}


def send_msgs1():
    url = 'https://community.cloud.databricks.com/notebook/3163019634332544/command/1484161255713383'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '192',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'smartling_redirect=(null); _vwo_uuid_v2=DD821CF26870F7C67DA05B96AF18F66F4|22021ec58f680921de2e1131c9850b4f; __q_state_KbmrrC8pEQRX5uYq=eyJ1dWlkIjoiYTQ5MzU4NjQtOGFmZS00MmM1LWE2MWYtMzQzYzYwMzgxOTNkIiwiY29va2llRG9tYWluIjoiZGF0YWJyaWNrcy5jb20ifQ==; _mkto_trk=id:094-YMS-629&token:_mch-databricks.com-1711696070655-99376; _gcl_au=1.1.1848985459.1711696071; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX18QQomzTk3FmW6H9FUxEKUlM6fgB%2BdNgKY%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2Fs4JSZeUXhMLUq6KUUGsh2hO4xlnGwqNA%3D; OptanonAlertBoxClosed=2024-03-29T07:08:03.211Z; _vwo_uuid=D137E84D78C62E2D0752E577F88007603; _vwo_ds=3%241711696101%3A22.78828856%3A%3A; _vis_opt_exp_393_combi=2; rs_ga=GA1.1.c6f682c7-583d-436a-b5b8-e1d00393f111; userty.core.p.5387b2=__2VySWQiOiI3NjEwYjU2NjU2ZDI2Y2IwNDRiMDViZmYzNjcxNjA5OSJ9eyJ1c; _vis_opt_exp_393_goal_1=1; _hp2_id.3428506230=%7B%22userId%22%3A%222045682190070831%22%2C%22pageviewId%22%3A%22384768027527140%22%2C%22sessionId%22%3A%226781360948139378%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; workspace-url=community.cloud.databricks.com; _vis_opt_s=2%7C; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Mar+30+2024+10%3A34%3A28+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202307.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=1ee22bd1-8026-49bd-8987-2185f695c953&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=CN%3BSC&AwaitingReconsent=false; rl_group_id=RudderEncrypt%3AU2FsdGVkX18uog1QYhUuoOYVhADKZErKY2jx17wstdA%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2FG5M2IC%2BNSdVm%2FvQmWVHFERx0mV7UCpQo%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2F5idKfQwh55x4StwQ9lnTGxQvC0Zp5f9%2BTlIU24rIFwaODXFFfPofKHH5AX51WxkYnY0DzbU8gcA%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX19Wj84ZIc8f3pBMrWp8QhupS1QCrv%2Bo8YA%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2FHpjUgphohTMEU9XECeXVUAa9KpmZiK%2FQ7ODW%2BTU8qhkTbnJQ02m41DGSBb3enc665pn4dzm1CW4K%2FdGSH78ydcBTZR464yaaqaS5gQ7OpJHhkkAoPG%2BXtBAuhoDp%2Bq0K64mRo9s5tiOVRjweHeDJZBdO06jhkgu8%3D; rl_session=RudderEncrypt%3AU2FsdGVkX1%2FR8v6OEdDg4XnkmIAtS%2BnAedZSHIg1vm895Dbnna0qb1f0O%2FOWxEeesxarzSBMPa1Q3ZLjXONXl9uZlBt4zfxM2osmjCGg668qlFY1gsubHcxdMDLrbvP2USbFz4FDW8c4SHMt1UuoHw%3D%3D; rs_ga_PQSEQ3RZQC=GS1.1.1711766069596.2.0.1711766070.60.0.0; JSESSIONID=auth-ce-788fd489d4-c7w92-m1xiym02icah3pn2rh9pqbyb.auth-ce-788fd489d4-c7w92-; _gid=GA1.2.1304538058.1711940995; _ga_ZRKMKEK030=GS1.1.1711940994.1.0.1711940994.0.0.0; _ga=GA1.1.247699851.1711940995; _uetsid=50b5c910efd511ee9551fb935d7d0de4; _uetvid=0ef1bb40ed9b11eeae6c9d71478bf168; _rdt_uuid=1711696072770.1e3fbc38-dd3d-4283-b083-29d5f14cbdb8; _db_utm_source__c=web; _db_utm_medium__c=direct',
        'Origin': 'https://community.cloud.databricks.com',
        'Referer': 'https://community.cloud.databricks.com/?o=5740491923789660',
        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Csrf-Token': 'bbb1b5c0-53a3-478f-a074-3ff6ddfcf338',
        'X-Databricks-Attribution-Tags': '%7B%22notebookId%22%3A3163019634332544%2C%22notebookLanguage%22%3A%22python%22%2C%22sparkVersion%22%3A%2212.2.x-scala2.12%22%2C%22clusterId%22%3A%220401-061132-f29zknei%22%2C%22clusterMemory%22%3A%2215616%22%2C%22clusterCreator%22%3A%22pmh905001%40126.com%22%2C%22clusterType%22%3A%22ondemand%22%2C%22browserTabId%22%3A%222fca5558-174c-4a50-ba73-2c4a6b56c4e8%22%2C%22browserHasFocus%22%3Atrue%2C%22browserIsHidden%22%3Afalse%2C%22browserHash%22%3A%22%23notebook%2F3163019634332544%2Fcommand%2F1484161255713383%22%2C%22browserPathName%22%3A%22%2F%22%2C%22browserHostName%22%3A%22community.cloud.databricks.com%22%2C%22browserUserAgent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F123.0.0.0%20Safari%2F537.36%22%2C%22eventWindowTime%22%3A20825410.1%2C%22clientTimestamp%22%3A1711955341928%2C%22clientBranchName%22%3A%22webapp_2024-03-16_09.56.29Z_master_861107d5_1704477292%22%2C%22clientLocale%22%3A%22en%22%2C%22browserLanguage%22%3A%22zh-CN%22%2C%22loadedUiVersions%22%3A%7B%22jaws%22%3A%22588f49741074fecd030ea57d4f26db317c320757%22%2C%22monolith%22%3A%22059eaa4c2ec35f4077d4db6aaa418691588e6547%22%7D%2C%22queryParameters%22%3A%22%3Fo%3D5740491923789660%22%2C%22browserIdleTime%22%3A86.69999999925494%7D',
        'X-Databricks-Org-Id': '5740491923789660',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        '@method': "runCmd",
        'newBindings': {},
        'newCommandText': "pairlist = [('Ana',['A']),('Bob',['B']),('Ana',['A2'])]\npairRDD = sc.parallelize(pairlist)\npairRDD.take(2)\n# pairRDD.collect()\n\n\n"
    }
    response = requests.post(url, headers=headers,json=data )
    # print(response.text)
    logging.info(response.status_code)



if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)-8s: %(lineno)s line -%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    for i in range(10000):
        send_msgs1()
        time.sleep(600)

