import json
import logging
import os
import random
import time

import requests


def read_cookie():
    with open('cookie.txt', 'r') as f:
        cookie = f.read().split(':')
    return {cookie[0]: cookie[1]}


def send_request(id, url, html_file_name):
    response: requests.Response = requests.get(url, headers=read_cookie(), allow_redirects=False)
    while response.is_redirect:
        location = response.headers['Location']
        print(f'redirect to {location}')
        response = requests.get(location, headers=read_cookie(), allow_redirects=False)

    with open(html_file_name, 'a', encoding='utf-8') as file:
        record = json.dumps({id: response.text}, ensure_ascii=False)
        file.write(record)
        file.write('\n')
    sleep_seconds = random.randint(1, 2)
    print(f'start to sleep {sleep_seconds} seconds')
    time.sleep(sleep_seconds)


def read_id_urls(file_name, line_number, record_number):
    result = []
    with open(file_name, 'r', encoding='utf-8') as index_file:
        lines = index_file.readlines()[line_number:]
        for line in lines:
            page: dict = json.loads(line)
            records = page['data']
            if records:
                id_urls_in_page = [(record['id'], url(record)) for record in records[record_number:] if url(record)]
                result.extend(id_urls_in_page)
            record_number = 0
    return result


def url_from_content(record):
    content = record.get('content')
    if content and isinstance(content, dict):
        return content.get('share_info', {}).get('share_url')


def url(record: dict):
    result = (record.get('url')
              or record.get('share_url')
              or record.get('share_info', {}).get('share_url')
              or url_from_content(record)
              or record.get('schema')
              )
    # if not result:
    #     logging.warning(f"generated URL is null, please check! {record} ")
    return result


def download_htmls():
    next_positions = find_to_download_html_files()
    for next_pos in next_positions:
        logging.info(f'start to download html files for {next_pos}')
        download_html_from_one_file(*next_pos)


def find_last_id_from_html_file(html_file_name):
    if html_file_name:
        with open(html_file_name, 'r', encoding='utf-8') as html_file:
            lines = html_file.readlines()
            if lines:
                last_line = lines[len(lines) - 1]
                return list(json.loads(last_line).keys())[0]
    return None


def find_to_download_html_files():
    all_html_files = {f'htmlcontent-{f}' for f in os.listdir('.') if f.startswith('myfavorites-')}
    html_files = {f for f in os.listdir('.') if f.startswith('htmlcontent-myfavorites-')}
    to_download_files = all_html_files - html_files

    last_html_file = sorted(html_files)[0] if html_files else None
    next_pos = _next_position(last_html_file)

    result = sorted([(file_name.replace('htmlcontent-', ''), 0, 0) for file_name in to_download_files])
    if next_pos:
        result.insert(0, next_pos)
    return result


def _next_position(last_html_file):
    last_id = find_last_id_from_html_file(last_html_file)
    if not last_id:
        return None
    index_file_name = last_html_file.replace('htmlcontent-', '')
    with open(index_file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line_number, line in enumerate(lines):
            page = json.loads(line)
            if page['data']:
                for record_number, record in enumerate(page['data']):
                    if record['id'] == last_id:
                        if line_number == len(lines) - 1 and record_number == len(page['data']):
                            return None
                        elif record_number == len(page['data']):
                            return (index_file_name, line_number + 1, 0)
                        else:
                            return (index_file_name, line_number, record_number + 1)
    raise FileNotFoundError(f'not found by id: {last_id} from {index_file_name}')


def download_html_from_one_file(file_name, line_number, record_number):
    # file_name = 'myfavorites-20240324-180714.txt'
    id_urls = read_id_urls(file_name, line_number, record_number)
    html_file_name = f'htmlcontent-{file_name}'
    for id, url in id_urls:
        print(f'id={id}, url={url}')
        try:
            send_request(id, url, html_file_name)
        except:
            logging.exception(f'ignore the exception for id: {id} url: {url}')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)-8s: %(lineno)s line -%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    download_htmls()
