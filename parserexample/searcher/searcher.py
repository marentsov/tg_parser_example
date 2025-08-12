import asyncio
import time
import random
from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest

import logging

log = logging.getLogger(__name__)



async def tg_search(query: str, client: TelegramClient, limit: int = 20) -> list:

    channels_list = []

    try:
        await client.start()

        # Anti-flood - remove when dedicated number is assigned
        time.sleep(1)
        # Search for channels
        search_result = await client(SearchRequest(q=query, limit=limit))

        print(search_result)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        await client.disconnect()



