import asyncio
from datetime import datetime

from .monitorSites import check
from constsTask2 import WEBSITES, CHECK_INTERVAL

async def monitor():
    while True:
        print(f"\n Monitoring started at {datetime.now().strftime('%H:%M:%S')}")

        tasks = [check(url) for url in WEBSITES]
        # тут все результаты по сайтам

        results = await asyncio.gather(*tasks)
        # ждемммм потом вернем

        for url, (available, response_time, headers) in zip(WEBSITES, results):
            print(f"{url}: Available={available}, Response Time={response_time:.2f}s")
        # красиво выводим все

        await asyncio.sleep(CHECK_INTERVAL)
        # ждеммм минутку спим