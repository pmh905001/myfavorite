# coding=utf-8
import json
import logging
import os
import random
import time

import requests

from fulldownload import read_curl, replace_url_param


def latest_ids_from_file():
    ids = []
    my_favorite_files = sorted([f for f in os.listdir('files') if f.startswith('myfavorites-')], reverse=True)
    for file_name in my_favorite_files:
        with open(f'files/{file_name}', 'r', encoding='utf-8') as f:
            page: dict = json.loads(f.readline())
            if page.get('data'):
                for record in page['data']:
                    if len(ids) <= 100:
                        ids.append(record['id'])
                    else:
                        return ids
    return ids


def increasement_download():
    url, headers = read_curl()
    latest_ids_downloaded = latest_ids_from_file()
    page = get_page(url, headers, 0, latest_ids_downloaded)
    try_num = 0
    file_name = f'myfavorites-{time.strftime("%Y%m%d-%H%M%S")}.txt'
    while page['has_more']:
        try_num += 1
        max_behot_time = page['next']['max_behot_time']
        write_page(page, f'files/{file_name}')
        sleep_time = random.randint(1, 10)
        print(f'-------------------------------------------page number: {try_num}, sleep {sleep_time} seconds')
        time.sleep(sleep_time)
        if try_num % 200==0:
            file_name = f'myfavorites-{time.strftime("%Y%m%d-%H%M%S")}.txt'
        page = get_page(url, headers, max_behot_time, latest_ids_downloaded)
    else:
        write_page(page, f'files/{file_name}')


def write_page(page, file_name):
    if not page.get('data'):
        return
    with open(file_name, 'a', encoding='utf-8') as fp:
        page_info = json.dumps(page, ensure_ascii=False)
        fp.write(page_info)
        fp.write('\n')

    for item in page['data']:
        try:
            print(f"{item['id']}: {item['title']}   => {item['share_url']}")
        # Fixme: UnicodeEncodeError
        except UnicodeEncodeError:
            logging.exception('occurred exception when print')


def get_page(url, headers, max_behot_time=0, latest_ids_downloaded=[]):
    url = replace_url_param(url, 'max_behot_time', max_behot_time)
    response = requests.get(url, headers=headers)
    page: dict = response.json()
    if page.get('data'):
        for index, record in enumerate(page.get('data')):
            if record['id'] in latest_ids_downloaded:
                page['data'] = page['data'][:index]
                page['has_more'] = False
    elif max_behot_time==0:        
        logging.warning('----------------------------------------------------------------------------')
        logging.warning('----------------------------------------------------------------------------')
        logging.warning('----------------------------------------------------------------------------')
        logging.warning('---------------Warning:curl_cmd.txt have expired----------------------------')
        logging.warning('---------------Warning:curl_cmd.txt have expired----------------------------')
        logging.warning('---------------Warning:curl_cmd.txt have expired----------------------------')
        logging.warning('---------------Warning:curl_cmd.txt have expired----------------------------')
        logging.warning('---------------Warning:curl_cmd.txt have expired----------------------------')
        logging.warning('---------------Warning:curl_cmd.txt have expired----------------------------')
        logging.warning('----------------------------------------------------------------------------')
        logging.warning('----------------------------------------------------------------------------')
        logging.warning('----------------------------------------------------------------------------')

    return page


if __name__ == '__main__':
    increasement_download()
