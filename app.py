import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from aiogram import Bot, Dispatcher, types
from groq import Groq
from duckduckgo_search import DDGS

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()
client = Groq(api_key=GROQ_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def search_web(query: str) -> str:
    try:
        results = DDGS().text(query, max_results=4)
        if not results:
            return ""
        return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception:
        return ""

def ask_omnai(user_text: str) -> str:
    web_context = search_web(user_text)
    system_prompt = (
        "Ты — Omnai, продвинутый суперассистент нового поколения. "
        "Отвечай чётко, умно и по делу. Используй свежие данные из поиска ниже, если они подходят к вопросу.\n\n"
        f"Актуальные данные из интернета:\n{web_context}"
    )
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        temperature=0.7,
        max_tokens=2048
    )
    return completion.choices[0].message.content

@dp.message()
async def handle_tg_message(message: types.Message):
    if not message.text:
        return
    await bot.send_chat_action(message.chat.id, "typing")
    reply = await asyncio.to_thread(ask_omnai, message.text)
    await message.answer(reply)

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(dp.start_polling(bot))

@app.post("/api/chat")
async def web_chat(request: Request):
    data = await request.json()
    reply = await asyncio.to_thread(ask_omnai, data.get("message", ""))
    return JSONResponse({"reply": reply})

@app.get("/manifest.json")
async def manifest():
    return JSONResponse({
        "name": "Omnai AI",
        "short_name": "Omnai",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#0f172a"
    })

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Omnai — Суперассистент</title>
        <link rel="manifest" href="/manifest.json">
        <style>
            body { margin: 0; font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; display: flex; flex-direction: column; height: 100vh; }
            header { padding: 16px; text-align: center; font-size: 20px; font-weight: bold; background: #1e293b; border-bottom: 1px solid #334155; }
            #chat { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
            .msg { max-width: 80%; padding: 12px 16px; border-radius: 16px; line-height: 1.5; white-space: pre-wrap; }
            .user { align-self: flex-end; background: #3b82f6; color: white; }
            .bot { align-self: flex-start; background: #1e293b; border: 1px solid #334155; }
            form { display: flex; padding: 12px; background: #1e293b; gap: 8px; }
            input { flex: 1; padding: 12px; border-radius: 12px; border: 1px solid #334155; background: #0f172a; color: white; font-size: 16px; }
            button { padding: 12px 20px; border-radius: 12px; border: none; background: #3b82f6; color: white; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <header>✨ Omnai AI (Web + App)</header>
        <div id="chat"><div class="msg bot">Привет! Я Omnai с доступом в реальный интернет. Спрашивай что угодно!</div></div>
[21.11.2026 01:16] Саша: <form id="form">
            <input id="input" placeholder="Напиши запрос..." autocomplete="off" required />
            <button type="submit">Отправить</button>
        </form>
        <script>
            const form = document.getElementById('form'), input = document.getElementById('input'), chat = document.getElementById('chat');
            form.onsubmit = async (e) => {
                e.preventDefault();
                const text = input.value; input.value = '';
                chat.innerHTML += <div class="msg user">${text}</div>;
                const botDiv = document.createElement('div'); botDiv.className = 'msg bot'; botDiv.textContent = 'Ищу в интернете и думаю...';
                chat.appendChild(botDiv); chat.scrollTop = chat.scrollHeight;
                const res = await fetch('/api/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: text}) });
                const data = await res.json();
                botDiv.textContent = data.reply; chat.scrollTop = chat.scrollHeight;
            };
        </script>
    </body>
    </html>
    """
