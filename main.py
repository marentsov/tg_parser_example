import os
import asyncio

from telethon import TelegramClient
from tg_parser import tg_parser
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')
client = TelegramClient(
        'test_session',
        os.getenv('API_ID'),
        os.getenv('API_HASH')
    )


asyncio.run(tg_parser(url, client, 10))