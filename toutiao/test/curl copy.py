import subprocess
import curlparser
import re

if __name__ == '__main__':
    with open('curl_cmd.txt', 'r', encoding='utf-8') as f:
        curl_cmd = f.read().replace('--compressed', '')

    curl = curlparser.parse(curl_cmd)
    headers = {key: value.strip() for key, value in curl.header.items()}
    url = curl.url

    # Extract cookies from -b option if present
    cookie_match = re.search(r'-b\s+[\'"]([^\'"]+)[\'"]', curl_cmd)
    if cookie_match:
        cookie_value = cookie_match.group(1)
        headers['Cookie'] = cookie_value

    cmd = ['curl', '-s', url] + [item for k, v in headers.items() for item in ['-H', f'{k}: {v}']]

    # print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
