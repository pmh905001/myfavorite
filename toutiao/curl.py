import subprocess
import curlparser

if __name__ == '__main__':
    with open('curl_cmd.txt', 'r', encoding='utf-8') as f:
        curl_cmd = f.read().replace('--compressed', '')
    
    curl = curlparser.parse(curl_cmd)
    headers = {key: value.strip() for key, value in curl.header.items()}
    url = curl.url
    
    cmd = ['curl', '-s', url] + [item for k, v in headers.items() for item in ['-H', f'{k}: {v}']]
    
    # print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
