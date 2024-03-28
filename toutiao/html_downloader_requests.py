import json
import logging
import random
import time

import requests


def read_cookie():
    with open('cookie.txt', 'r') as f:
        cookie = f.read().split(':')
    return {cookie[0]: cookie[1]}


def send_request(id, url, html_file_name):
    response: requests.Response = requests.get(url, headers=read_cookie(), allow_redirects=False)
    # while response.is_redirect:
    #     location = response.headers['Location']
    #     print(f'redirect to {location}')
    #     response = requests.get(location, headers=read_cookie(), allow_redirects=False)

    with requests.session() as session:
        response = session.get(url, headers=read_cookie(), allow_redirects=False)
        while response.is_redirect:
            location = response.headers['Location']
            print(f'redirect to {location}')
            response = session.get(location, headers=read_cookie(), allow_redirects=False)

    with open(html_file_name, 'a', encoding='utf-8') as file:
        record = json.dumps({id: response.text}, ensure_ascii=False)
        file.write(record)
        file.write('\n')
    sleep_seconds = random.randint(1, 10)
    print(f'start to sleep {sleep_seconds} seconds')
    time.sleep(sleep_seconds)


# 主函数
def read_id_urls(file_name):
    result = []
    with open(file_name, 'r', encoding='utf-8') as index_file:
        lines = index_file.readlines()
        for line in lines:
            page: dict = json.loads(line)
            records = page['data']
            if records:
                id_urls_in_page = [(record['id'], url(record)) for record in records]
                result.extend(id_urls_in_page)
    return result


def url_from_content(record):
    content = record.get('content')
    if content and isinstance(content, dict):
        return content.get('share_info', {}).get('share_url')


def url(record: dict):
    return (record.get('url')
            or record.get('share_url')
            or record.get('share_info', {}).get('share_url')
            or url_from_content(record)
            )


def main():
    # id_urls = read_id_urls('myfavorites-20231118-164500.txt')
    file_name = 'myfavorites-20240324-180714.txt'
    id_urls = read_id_urls(file_name)
    html_file_name = f'htmlcontent-{file_name}'
    for id, url in id_urls:
        print(f'id={id}, url={url}')
        send_request(id, url, html_file_name)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)-8s: %(lineno)s line -%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main()
