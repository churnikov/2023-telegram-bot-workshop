import os
import asyncio

from dotenv import load_dotenv
import aiohttp


load_dotenv()
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.telegram.org/bot{}/getMe'.format(TG_BOT_TOKEN)) as resp:
            print(resp.status)
            print(await resp.json())

        async with session.get('https://api.telegram.org/bot{}/getUpdates'.format(TG_BOT_TOKEN)) as resp:
            print(resp.status)
            print(await resp.json())

asyncio.run(main())
