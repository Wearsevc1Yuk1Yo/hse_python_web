import asyncio

from .monitorSites import check
from constsTask2 import WEBSITES, CHECK_INTERVAL

async def monitor():
    while True:
        tasks = [check(url) for url in WEBSITES]
        results = await asyncio.gather(*tasks)
        
        for url, (available, response_time, headers) in zip(WEBSITES, results):
            print(f"{url}: Available={available}, Response Time={response_time:.2f}s")
        
        await asyncio.sleep(CHECK_INTERVAL)