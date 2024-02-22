import asyncio
import logging


async def print_hello():
    while True:
        logging.info('hello world')
        sleep_co = asyncio.sleep(1)  # 创建sleep协程
        await sleep_co

async def print_goodbye():
    while True:
        logging.info('goodbye world')
        sleep_co = asyncio.sleep(2)  # 创建sleep协程
        await sleep_co

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(filename)-8s: %(lineno)s line -%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
co1 = print_hello()  # 创建协程对象
co2 = print_goodbye()  # 创建协程对象

# asyncio.run(co1)
# asyncio.run(co2)
# asyncio.get_event_loop().run_until_complete(asyncio.gather(co1,co2))
asyncio.get_event_loop().run_until_complete(asyncio.gather(co1,co2))

