from telethon.tl.functions.messages import SearchGlobalRequest
from telethon.tl.types import InputMessagesFilterEmpty, InputPeerEmpty


async def tg_search(client, query, limit=10):
    try:
        await client.start()

        result = await client(SearchGlobalRequest(
            q=query,
            filter=InputMessagesFilterEmpty(),
            min_date=None,
            max_date=None,
            offset_rate=0,
            offset_peer=InputPeerEmpty(),
            offset_id=0,
            limit=limit,
            broadcasts_only=True  # Только каналы
        ))

        channels = set()  # Используем set для уникальности
        for message in result.messages:
            if message.peer_id and hasattr(message.peer_id, 'channel_id'):
                channel = await client.get_entity(message.peer_id)
                if channel.broadcast:  # Проверяем, что это действительно канал
                    channels.add((channel.id, channel.title))

        for channel_id, channel_title in channels:
            print(f"Найден канал: {channel_title}")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        await client.disconnect()
