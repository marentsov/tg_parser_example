from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest

async def tg_search(client, query, limit=10):

    try:
        await client.start()

        result = await client(SearchRequest(q=query, limit=limit))

        for channel in result.chats:
            print(channel.title, channel.participants_count, channel.id)


    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        await client.disconnect()
