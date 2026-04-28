from aiogram import Router, types
from aiogram.filters import Command
from utils.jikan_helper import get_anime_info
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("search"))
async def search_handler(message: types.Message):
    query = message.text.replace("/search", "").strip()
    if not query:
        return await message.answer("Qidirish uchun nom yozing...")

    anime = await get_anime_info(query)
    if anime:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Sevimlilarga qo'shish", callback_data=f"fav_{anime['mal_id']}_{anime['title'][:15]}")]
        ])
        
        caption = f"🎬 {anime['title']}\n🌟 Reyting: {anime['score']}\n\n{anime['synopsis'][:300]}..."
        await message.answer_photo(anime['images']['jpg']['large_image_url'], caption=caption, reply_markup=kb)
    else:
        await message.answer("Hech narsa topilmadi.")
