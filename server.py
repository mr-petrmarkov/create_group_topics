from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest, MigrateChatRequest
from telethon.tl.functions.channels import CreateForumTopicRequest

# Fallback для включения форумов (ToggleForum не всегда доступен)
try:
    from telethon.tl.functions.channels import ToggleForum
    HAS_TOGGLE_FORUM = True
except ImportError:
    from telethon.tl.functions.messages import EditChatDefaultBannedRights
    from telethon.tl.types import ChatBannedRights
    HAS_TOGGLE_FORUM = False

import uvicorn

# 🔑 Твои данные (лучше хранить в Render Secrets!)
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"
session_name = "my_session"

# создаём FastAPI
app = FastAPI()
client = TelegramClient(session_name, api_id, api_hash)


@app.on_event("startup")
async def startup_event():
    await client.start()


@app.post("/create_supergroup")
async def create_supergroup(request: Request):
    """
    Создаёт супергруппу и включает форумы
    """
    try:
        data = await request.json()
        title = data.get("title")
        users = data.get("users", [])

        if not title or not users:
            return JSONResponse(status_code=400, content={"error": "title и users обязательны"})

        # создаём обычную группу
        chat = await client(CreateChatRequest(users=users, title=title))
        chat_id = chat.chats[0].id

        # мигрируем в супергруппу
        migrated = await client(MigrateChatRequest(chat_id))
        channel_id = migrated.chats[0].id

        # включаем форумы
        if HAS_TOGGLE_FORUM:
            await client(ToggleForum(channel=channel_id, enabled=True))
        else:
            rights = ChatBannedRights(until_date=None, send_messages=False)
            await client(EditChatDefaultBannedRights(channel_id, rights))

        return JSONResponse(
            status_code=200,
            content={"status": "ok", "supergroup_id": channel_id}
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/create_topic")
async def create_topic(request: Request):
    """
    Создаёт топик в супергруппе
    """
    try:
        data = await request.json()
        channel_id = data.get("channel_id")
        topic_title = data.get("topic_title")

        if not channel_id or not topic_title:
            return JSONResponse(status_code=400, content={"error": "channel_id и topic_title обязательны"})

        topic = await client(CreateForumTopic(channel=channel_id, title=topic_title))

        return JSONResponse(
            status_code=200,
            content={"status": "ok", "topic_id": topic.updates[0].id}
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
