import asyncio
import logging
import sys
import os

# Root katalogni tanitish (Xatolikni oldini oladi)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers import search, sevimlilar  # Bu ishlashi uchun handlers/__init__.py bo'lishi kerak

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(search.router)
    dp.include_router(sevimlilar.router)

    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
