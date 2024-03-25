import aiohttp
import asyncio

# 异步请求函数
async def send_async_request(url):
    headers = {
        'authority': 'www.toutiao.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Cookie': 'csrftoken=a0b46616bea4129283c472d913348d0d; tt_webid=6964941546656253453; _S_DPR=1; _S_IPAD=0; n_mh=cex_woIpAKNtUm7nK0CJhJlOET0O0_tHio9alXAcaAA; store-region-src=uid; _ga=GA1.1.378711725.1650155063; store-region=cn-sc; _S_WIN_WH=2560_919; _S_UA=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F120.0.0.0%20Safari%2F537.36; passport_csrf_token=464821ac9bc96d6c44817918e1dfe461; passport_csrf_token_default=464821ac9bc96d6c44817918e1dfe461; sso_uid_tt=9a500ce8e562fcdae7ed03a3a86ada0a; sso_uid_tt_ss=9a500ce8e562fcdae7ed03a3a86ada0a; toutiao_sso_user=223021ee09575eb85be21575a8bc076b; toutiao_sso_user_ss=223021ee09575eb85be21575a8bc076b; sid_ucp_sso_v1=1.0.0-KDdkYTI1YTUwZmY0YzgxMmI2NTBjYjc1NTE4Yzg2ZGI2NWVmNTdhZTAKHAj17JG14wEQ-a6hrgYYGCAMMKyfnskFOAZA9AcaAmhsIiAyMjMwMjFlZTA5NTc1ZWI4NWJlMjE1NzVhOGJjMDc2Yg; ssid_ucp_sso_v1=1.0.0-KDdkYTI1YTUwZmY0YzgxMmI2NTBjYjc1NTE4Yzg2ZGI2NWVmNTdhZTAKHAj17JG14wEQ-a6hrgYYGCAMMKyfnskFOAZA9AcaAmhsIiAyMjMwMjFlZTA5NTc1ZWI4NWJlMjE1NzVhOGJjMDc2Yg; sid_guard=f798b4b2b60dc2c97c9a3bff8b34feb2%7C1707628411%7C5184000%7CThu%2C+11-Apr-2024+05%3A13%3A31+GMT; uid_tt=02d29322e358ab198234fd61460872d5; uid_tt_ss=02d29322e358ab198234fd61460872d5; sid_tt=f798b4b2b60dc2c97c9a3bff8b34feb2; sessionid=f798b4b2b60dc2c97c9a3bff8b34feb2; sessionid_ss=f798b4b2b60dc2c97c9a3bff8b34feb2; sid_ucp_v1=1.0.0-KDU1ZmI2NDU3NTcwMTg4NGRiNTE3YzVjNDMwMGZhMTI5MmQ3NDA1ZTQKFgj17JG14wEQ-66hrgYYGCAMOAZA9AcaAmxmIiBmNzk4YjRiMmI2MGRjMmM5N2M5YTNiZmY4YjM0ZmViMg; ssid_ucp_v1=1.0.0-KDU1ZmI2NDU3NTcwMTg4NGRiNTE3YzVjNDMwMGZhMTI5MmQ3NDA1ZTQKFgj17JG14wEQ-66hrgYYGCAMOAZA9AcaAmxmIiBmNzk4YjRiMmI2MGRjMmM5N2M5YTNiZmY4YjM0ZmViMg; local_city_cache=%E6%88%90%E9%83%BD; s_v_web_id=verify_lttjo787_m1p9Xw3S_8aFJ_4F84_8wkF_v4G2qnAlkbhm; odin_tt=81f10a192a097dc5738843ac844c5aedde5934d5cf4be01118473d284706f506e526986171580468c8efa06d46ee4029; _ga_QEHZPBE5HH=GS1.1.1711090774.297.0.1711090774.0.0.0; tt_scid=ADt31rLDFXhu76o52ekgEbG1cgbX9DpmMH6EuhssOo2e8HXg1PLlo2n0ZL3t6aLu5896; tt_anti_token=t2OmkTqp9bJdLWQ-4010fd2cdc64f4697c9201ae5abf93a9709639fc7e424ffe5946b3ed1302bbea; ttwid=1%7CNWDCK1ApBIE-qURzrWxDn-xfqCUUmNNzLuQddJ7Gf9Q%7C1711090776%7Ce2259f53683fdf27eba20c414683ee29d0d64c02a166400f2135c8d35650b818; msToken=wA6YOUoAALET06Z2zUjFuepokYqwtYcCwwnEAR2bMlHvJXc7ObuXE5LE3iPFbRNHQiY4UQ_RvWLMbMlQjf9VyGmMAJrqKwez_WKLTg6Mdg==',
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
    async with aiohttp.ClientSession(headers=headers) as session:
        # 发出异步 GET 请求
        response = await session.get(url)
        html_content = await response.text()
        # 在异步回调处理中保存 HTML 内容到文件
        with open('001.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

# 主函数
async def main():
    url = 'https://www.toutiao.com/article/7347962717489152531/'
    task = asyncio.create_task(send_async_request(url))
    await task

# 运行主函数
asyncio.run(main())