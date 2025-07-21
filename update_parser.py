import asyncio
import time
import random
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import (
    FloodWaitError,
    UsernameNotOccupiedError,
    ChannelInvalidError,
    AuthKeyError,
    ForbiddenError,
)

import logging

log = logging.getLogger(__name__)


async def tg_parser(url: str, client: TelegramClient, limit: int = 10) -> dict:
    data = {}
    full_channel = None
    pinned_messages = None

    try:
        time.sleep(1)  # Антифлуд
        channel = await client.get_entity(url)
        log.debug(f"Получен channel: {channel.__dict__}")
        data["title"] = channel.title
        data["channel_id"] = channel.id
        data["username"] = channel.username
        data["verified"] = channel.verified
        data["creation_date"] = channel.date.isoformat() if channel.date else None

        try:
            last_messages = await client.get_messages(channel, limit=limit * 3)
        except Exception as e:
            log.error(f"Ошибка при получении сообщений для канала {url}: {e}")
            last_messages = []

        log.debug(
            f"Получены last_messages: {len(last_messages) if last_messages else 0} сообщений"
        )
        if last_messages:
            data["last_messages"] = [
                {"post_id": post.id, "post_text": post.text, "post_views": post.views}
                for post in last_messages[:limit]
            ]
            total_views = sum(
                post.views for post in last_messages if post.views is not None
            )
            total_posts = len(
                [post for post in last_messages if post.views is not None]
            )
            data["average_views"] = total_views // total_posts if total_posts > 0 else 0
        else:
            data["last_messages"] = []
            data["average_views"] = 0

    except FloodWaitError as e:
        log.error("Сработал антифлуд, нужно подождать")
        await asyncio.sleep(e.seconds + random.uniform(1.0, 2.0))
    except ChannelInvalidError:
        log.warning(f"Канал приватный или недоступен: {url}")
    except UsernameNotOccupiedError:
        log.error(f"Несуществующий юзернейм: {url}")
    except AuthKeyError:
        log.critical("Проблемы с сессией авторизации")

    if channel:
        try:
            full_channel = await client(GetFullChannelRequest(channel))
        except FloodWaitError as e:
            log.error("Сработал антифлуд, нужно подождать")
            await asyncio.sleep(e.seconds + random.uniform(1.0, 2.0))
        except ForbiddenError:
            log.warning("Ошибка доступа к полной информации канала")

        if full_channel:
            data["participants_count"] = (
                full_channel.full_chat.participants_count or "Нет участников"
            )
            data["description"] = full_channel.full_chat.about or "Нет описания"
            pinned_message_id = full_channel.full_chat.pinned_msg_id
            if pinned_message_id:
                pinned_messages = await client.get_messages(
                    channel, ids=pinned_message_id
                )
            data["pinned_messages"] = [
                {
                    "text": pinned_messages.message
                    if pinned_messages
                    else "Нет закрепленного сообщения",
                    "id": pinned_message_id if pinned_messages else None,
                }
            ]

    log.debug(f"Канал успешно спарсился: {data}")
    return data
