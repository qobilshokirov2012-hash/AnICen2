import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers import start, search, sevimlilar

logging.basicConfig(level=logging.INFO)

async def main():
    # MB yaratish
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_routers(
        search.router,
        sevimlilar.router
    )

    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
