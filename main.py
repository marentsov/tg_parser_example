import os
import asyncio


from telethon import TelegramClient
from telethon.sessions import StringSession


from dotenv import load_dotenv

from tg_search import tg_search

TELEGRAM_API_ID=29779188
TELEGRAM_API_HASH="174c9cd117a35e4eda4cfe89b15e3389"
TELEGRAM_SESSION_STRING="1ApWapzMBuzLMAQ98siIq-K2JGKzqp_9KkOp8ZGjnQQ4cnHkeXIY-J-YMCH9DyqZqBs-yW9mNc_ezv8vyBs91O7sn5HS2_VDe93GizdVWdJEmXnv8e-GdgvmCvIIyRiB1BvGfU7epaW_5NM4Ii6QQZsDM6EB1C5RPdhKPhvxDIHbHk_6rSHYVzvUxJ8kzBVrkx7ySHgMe0FBEEJF8eWCQ9gO9XSbvM6IY4ZEDZSfphE4zzzqBMh2J7EPWLq4lImAUKSZUL5FMNuDnkR0YJWNanz4Saah5m5Lnjsx4ZyXuXMI0NjOoa9jr5Pu74afM9af-3biYjLLLzEI5YW68SvnTJ_ZA_Ucdt9I="

query = "Строительство"

client = TelegramClient(
            StringSession(TELEGRAM_SESSION_STRING),
            TELEGRAM_API_ID,
            TELEGRAM_API_HASH,
        )


#asyncio.run(tg_parser(url, client, 10))
asyncio.run(tg_search(client, query))
