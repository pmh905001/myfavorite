from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(7))
def stop_after_7_attempts():
    print("重试7次后停止")
    raise Exception

if __name__=='__main__':
    stop_after_7_attempts()
    print('hello')