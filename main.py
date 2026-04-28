import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Tokenni Railway "Variables" qismidan oladi
API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
BASE_URL = "https://api.jikan.moe/v4"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🎬 Anime Botga xush kelibsiz!\n\n/search [nomi] - Qidirish\n/random - Tasodifiy anime")

@dp.message(Command("search"))
async def search_anime(message: types.Message):
    query = message.text.replace("/search", "").strip()
    if not query:
        return await message.answer("Anime nomini yozing. Masalan: `/search One Piece`")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/anime?q={query}&limit=1") as response:
            data = await response.json()
            if not data.get('data'):
                return await message.answer("Topilmadi 😕")

            anime = data['data'][0]
            caption = f"🎬 **{anime['title']}**\n⭐ Reyting: {anime['score']}\n🎞 Qismlar: {anime['episodes']}\n\n{anime['synopsis'][:300]}..."
            await message.answer_photo(photo=anime['images']['jpg']['large_image_url'], caption=caption)

@dp.message(Command("random"))
async def random_anime(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/random/anime") as response:
            data = await response.json()
            anime = data['data']
            await message.answer_photo(photo=anime['images']['jpg']['large_image_url'], caption=f"🎲 Tavsiya: **{anime['title']}**")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
