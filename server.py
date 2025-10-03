from fastapi import FastAPI
from telethon import TelegramClient, functions, types

app = FastAPI()

# Конфиг для клиента
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"
client = TelegramClient("my_session", api_id, api_hash)


@app.on_event("startup")
async def startup_event():
    await client.start()


@app.on_event("shutdown")
async def shutdown_event():
    await client.disconnect()


@app.get("/")
async def root():
    return {"status": "ok"}


# === Примеры вызовов Telethon ===

# Создать топик в форуме
async def create_forum_topic(channel, title: str):
    return await client(functions.channels.CreateForumTopicRequest(
        channel=channel,
        title=title,
    ))


# Включить/выключить режим форума в канале
async def toggle_forum(channel, enabled: bool = True):
    return await client(functions.channels.ToggleForumRequest(
        channel=channel,
        enabled=enabled
    ))


# Задать дефолтные ограничения для чата
async def set_default_banned_rights(chat, ban_messages=True):
    rights = types.ChatBannedRights(
        send_messages=ban_messages,
        until_date=None
    )
    return await client(functions.messages.EditChatDefaultBannedRightsRequest(
        peer=chat,
        banned_rights=rights
    ))
