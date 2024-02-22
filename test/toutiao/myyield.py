def consumer():
    msg = ''
    while True:
        # 返回consumer消息
        # 接收外部传入值
        n = yield msg
        if not n:
            return
        print(f"消费者消费:{n}")
        msg = '消费完成'

# 生产者
def produce(c):
    # 启动协程
    # c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print(f"生产者生产: {n}")
        # 发送数据给生成器
        # 并接收协程返回的参数
        msg = c.send(n)
        print(f"收到消费者消息: {msg}")
    c.close()

# 调用生产者
produce(consumer())