import aiosqlite
from config import DATABASE_NAME

async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                anime_id INTEGER,
                anime_title TEXT,
                PRIMARY KEY (user_id, anime_id)
            )
        ''')
        await db.commit()

async def add_to_favorite(user_id, anime_id, title):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO favorites VALUES (?, ?, ?)", (user_id, anime_id, title))
        await db.commit()

async def get_favorites(user_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("SELECT anime_title FROM favorites WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()
