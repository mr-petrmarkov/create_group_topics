from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest

# 🔑 Укажите свои api_id и api_hash
api_id = 21334519      # замените на ваш api_id
api_hash = 'ad90b94b00185c6d9b0341af99121cf2'  # замените на ваш api_hash

# создаём клиент
client = TelegramClient('my_session', api_id, api_hash)

async def create_group():
    # создаём группу с указанными пользователями
    result = await client(CreateChatRequest(
        users=['grimmneg', '@philip_777','SmileMedia_SPb_bot'],  # логины или user_id участников
        title="Моя новая группа"
    ))
    print("Группа создана:", result)

# запуск
with client:
    client.loop.run_until_complete(create_group())
