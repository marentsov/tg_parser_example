import time
import json
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest


async def tg_parser(url: str, client: TelegramClient, limit: int = 10) -> dict:
    """
    Функция-парсер телеграм каналов, позволяет получить данные о телеграм канале,
    включая: название, id, описание, количество подписчиков, закрепленное сообщение, последние посты.
    Параметры:
    url (str): ссылка на телеграм канал в любом из удобных видов (https://t.me/example, t.me/example, @example, example)
    client (TelegramClient): клиент телеграма из библиотеки telethon
    limit (int): количество сообщений для парсинга, по умолчанию 10
    Возвращаемое значение:
    data (dict): словарь с данными телеграм канала
    Примечание:
    Для работы данной функции необходима регистрация приложения telegram API
    """

    try:

        time.sleep(1)
        # получаем информацию о канале
        channel = await client.get_entity(url)
        # получаем полную информацию о канале
        full_channel = await client(GetFullChannelRequest(channel))
        # получаем число участников
        participants_count = full_channel.full_chat.participants_count
        # получаем описание канала
        description = full_channel.full_chat.about
        # получаем дату создания канала
        creation_date = channel.date.isoformat(),
        # булево значение, верифицирован канал или нет
        verified =  channel.verified,
        # получаем id закрепленного сообщения
        pinned_message_id = full_channel.full_chat.pinned_msg_id
        # получаем закрепленное сообщение
        pinned_message = None
        if pinned_message_id:
            pinned_message = await client.get_messages(channel, ids=pinned_message_id)
        # получаем 10 последних постов из канала
        last_messages = await client.get_messages(channel, limit=limit*3)
        # получаем среднее количество просмотров последних постов
        total_views = 0
        total_posts = 0
        for post in last_messages:
            total_views += post.views
            total_posts += 1
        average_views = total_views // total_posts

        data = {
            'title': channel.title,
            'channel_id': channel.id,
            'description': description if description else 'Нет описания',
            'username': channel.username,
            'participants_count': participants_count if participants_count else 'Нет участников',
            'creation_date': creation_date,
            'verified': verified,
            'pinned_messages': [{
                'text': pinned_message.message if pinned_message else 'Нет закрепленного сообщения',
                'id': pinned_message_id if pinned_message else None
            }],
            'last_messages': [{'post_id': post.id, 'post_text': post.text, 'post_views': post.views}
                                        for post in last_messages[:limit]],
            'average_views': average_views,
        }
        print(data['pinned_messages'])
        return data

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        pass