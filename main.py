import os
import asyncio

from telethon import TelegramClient
from tg_parser import tg_parser
from tg_search import tg_search
from dotenv import load_dotenv

load_dotenv()

query = 'самолет'
url = os.getenv('URL')
client = TelegramClient(
        'test_session',
        os.getenv('API_ID'),
        os.getenv('API_HASH')
    )


asyncio.run(tg_parser(url, client, 10))
# asyncio.run(tg_search(client, query, 10))

