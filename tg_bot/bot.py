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
            resp = await resp.json()

        for update in resp['result']:
            print("Updates")
            print(update)

        for update in resp['result']:
            if "text" not in update['message']:
                continue
            async with session.post('https://api.telegram.org/bot{}/sendMessage'.format(TG_BOT_TOKEN), json={
                'chat_id': update['message']['chat']['id'],
                'text': update['message']['text']
            }) as resp:
                print(resp.status)
                print(await resp.json())

        # Clear updates from queue



asyncio.run(main())
