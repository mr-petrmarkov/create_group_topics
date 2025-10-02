from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannel, ToggleForum, InviteToChannel
from telethon.tl.functions.messages import CreateForumTopic
import asyncio

api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"

client = TelegramClient("my_session", api_id, api_hash)
client.start()

app = Flask(__name__)

@app.route("/create_forum_group", methods=["POST"])
def create_forum_group():
    data = request.json
    title = data.get("title", "Новая форум-группа")
    users = data.get("users", [])        # список username или ID
    topics = data.get("topics", [])      # список названий топиков

    async def runner():
        # 1. создаём мегагруппу
        result = await client(CreateChannel(
            title=title,
            about="Группа с топиками",
            megagroup=True
        ))
        chat = result.chats[0]

        # 2. включаем форумный режим
        await client(ToggleForum(channel=chat, enabled=True))

        # 3. приглашаем пользователей
        if users:
            try:
                await client(InviteToChannel(
                    channel=chat,
                    users=users
                ))
            except Exception as e:
                print(f"Ошибка добавления юзеров: {e}")

        # 4. создаём топики
        created_topics = []
        for t in topics:
            try:
                topic = await client(CreateForumTopic(
                    channel=chat,
                    title=t
                ))
                created_topics.append(t)
            except Exception as e:
                print(f"Ошибка создания топика {t}: {e}")

        return {"chat_id": chat.id, "topics": created_topics}

    result = client.loop.run_until_complete(runner())
    return jsonify({"status": "ok", "result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


