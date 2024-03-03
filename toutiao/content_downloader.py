import requests

def get_webpage_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("请求失败，状态码：", response.status_code)

# 要爬取的网页 URL
url = "https://www.toutiao.com/article/7340558904604181043"
page_content = get_webpage_content(url)
print(page_content)