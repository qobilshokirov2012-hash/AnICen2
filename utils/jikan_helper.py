import aiohttp

BASE_URL = "https://api.jikan.moe/v4"

async def get_anime_info(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/anime?q={query}&limit=1") as resp:
            data = await resp.json()
            return data['data'][0] if data.get('data') else None

async def get_seasonal_anime():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/seasons/now?limit=5") as resp:
            return await resp.json()
