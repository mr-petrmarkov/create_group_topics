from telethon import TelegramClient

api_id = 21334519 # ваш api_id
api_hash = 'ad90b94b00185c6d9b0341af99121cf2'  # ваш api_hash

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    await client.start()
    print("Вы вошли как:", (await client.get_me()).username)

with client:
    client.loop.run_until_complete(main())