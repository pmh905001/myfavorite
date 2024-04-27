import requests

from test.toutiao.html_content_download2 import read_cookie


def send_msgs():
    url = 'https://www.toutiao.com/article/7347962717489152531/'
    headers = {
        'authority': 'www.toutiao.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        **read_cookie(),
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
    response = requests.get(url, headers=headers)
    print(response.text)
    # with open('myfav.html', 'w', encoding='utf-8') as f:
    #     f.write(response.text)


def parse_html():
    from bs4 import BeautifulSoup
    with open('myfav.html','r',encoding='utf-8') as f:
        html_doc=f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        content=soup.select('.article-content')
        print(content[0].get_text())
        # print(content)
        # with open('myfav002_part.html','w',encoding='utf-8') as txt_f:
        #     txt_f.write(str(content[0]))





if __name__ == '__main__':
    # send_msgs()
    parse_html()
