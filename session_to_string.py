import asyncio
from telethon.sessions import StringSession
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

SESSION_NAME = 'test_session'
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


async def main():
    # Инициализация клиента с существующей файловой сессией
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    await client.connect()  # Подключаемся без полного старта

    # Конвертируем сессию в строку
    if client.session:
        session_str = StringSession.save(client.session)
        print("\n" + "=" * 50)
        print("✅ ВАША СТРОКА СЕССИИ:")
        print(session_str)
        print("=" * 50)

        # Сохраняем в файл
        with open(f"{SESSION_NAME}.txt", "w") as f:
            f.write(session_str)
    else:
        print("❌ Сессия не найдена!")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())