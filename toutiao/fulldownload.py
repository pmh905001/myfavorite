# coding=utf-8
import json
import logging
import random
import time
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode

import curlparser
import requests


def read_curl():
    with open('curl_cmd2.txt', 'r') as f:
        # curlparser currently not support parameter 'compressed'
        curl_cmd = f.read().replace('--compressed', '')
    curl = curlparser.parse(curl_cmd)
    # trim the bank of string
    headers = {key: value.strip() for key, value in curl.header.items()}
    return curl.url, headers


def get_page(url, headers, max_behot_time=0):
    url = replace_url_param(url, 'max_behot_time', max_behot_time)
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def replace_url_param(url, param_name, new_value):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)
    query_params[param_name] = [new_value]
    new_query_string = urlencode(query_params, doseq=True)
    new_url = urlunsplit((scheme, netloc, path, new_query_string, fragment))
    return new_url


def write_page(page):
    with open('toutiao-myfavorites.txt', 'a', encoding='utf-8') as fp:
        page_info = json.dumps(page, ensure_ascii=False)
        fp.write(page_info)
        fp.write('\n')

    for item in page['data']:
        try:
            print(f"{item['id']}: {item['title']}   => {item['share_url']}")
        # Fixme: UnicodeEncodeError
        except UnicodeEncodeError:
            logging.exception('occurred exception when print')


if __name__ == '__main__':

    url, headers = read_curl()
    page = get_page(url, headers, 0)

    try_num = 0
    while page['has_more']:
        try_num += 1
        max_behot_time = page['next']['max_behot_time']
        write_page(page)
        sleep_time = random.randint(1, 10)
        print(f'-------------------------------------------page number: {try_num}, sleep {sleep_time} seconds')
        time.sleep(sleep_time)
        page = get_page(url, headers, max_behot_time)
    else:
        write_page(page)
