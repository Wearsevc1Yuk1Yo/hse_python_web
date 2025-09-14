import asyncio
from datetime import datetime

from .monitorSites import check
from constsTask2 import WEBSITES, CHECK_INTERVAL

async def monitor():
    try:
        while True:
            print(f"\n Monitoring started at {datetime.now().strftime('%H:%M:%S')}")

            tasks = [check(url) for url in WEBSITES]
            # тут все результаты по сайтам

            results = await asyncio.gather(*tasks)
            # ждемммм потом вернем

            for url, (available, response_time, headers) in zip(WEBSITES, results):
                print(f"{url}: Available={available}, Response Time={response_time:.2f}s")
            # красиво выводим все

            for _ in range(CHECK_INTERVAL * 10):  # Проверяем каждые 0.1 секунду
                    await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        print("Monitoring finished")
        # raise
