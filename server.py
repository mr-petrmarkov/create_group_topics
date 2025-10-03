from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from telethon import TelegramClient, functions
from telethon.tl.functions.messages import CreateChatRequest
import uvicorn

# 🔑 твои api_id и api_hash
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"
session_name = "my_session"  # должен совпадать с файлом my_session.session

app = FastAPI()

# создаём Telethon client один раз
client = TelegramClient(session_name, api_id, api_hash)


@app.on_event("startup")
async def startup_event():
    await client.connect()
    if not await client.is_user_authorized():
        raise RuntimeError("❌ Сессия не авторизована. Нужно заново авторизоваться локально и загрузить my_session.session")
    print("✅ Telethon подключен и авторизация успешна")


@app.on_event("shutdown")
async def shutdown_event():
    await client.disconnect()


@app.post("/create_group")
async def create_group(request: Request):
    try:
        data = await request.json()
        title = data.get("title")
        users = data.get("users", [])

        if not title or not users:
            return JSONResponse(
                status_code=400,
                content={"error": "title и users обязательны"}
            )

        # создаём группу
        result = await client(CreateChatRequest(users=users, title=title))

        return JSONResponse(
            status_code=200,
            content={"status": "ok", "chat": str(result)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# 🔥 локальный запуск
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
