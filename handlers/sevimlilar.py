from aiogram import Router, types, F
from aiogram.filters import Command
from database.db import add_to_favorite, get_favorites

router = Router()

@router.callback_query(F.data.startswith("fav_"))
async def save_favorite(callback: types.CallbackQuery):
    _, anime_id, title = callback.data.split("_", 2)
    await add_to_favorite(callback.from_user.id, int(anime_id), title)
    await callback.answer(f"✅ {title} sevimlilarga qo'shildi!")

@router.message(Command("sevimlilar"))
async def show_favorites(message: types.Message):
    favs = await get_favorites(message.from_user.id)
    if not favs:
        return await message.answer("Sizda hali sevimlilar yo'q.")
    
    text = "🌟 Sizning sevimlilaringiz:\n\n" + "\n".join([f"• {f[0]}" for f in favs])
    await message.answer(text)
