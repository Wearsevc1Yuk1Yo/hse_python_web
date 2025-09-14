import aiohttp
import asyncio
import time

from typing import Tuple

async def check(url: str) -> Tuple[bool, float, str]:
    #                  доступен/ноу, время ответа, тип контента/error

    try:
        async with aiohttp.ClientSession() as session:
            
            start_time = asyncio.get_event_loop().time()
            # начало сессии 
            async with session.get(url, timeout=10) as response:
                response_time = asyncio.get_event_loop().time() - start_time
                # время назапрос 
                return True, response_time, response.headers.get('Content-Type', '')
            
    except Exception as e:
        return False, 0.0, str(e)