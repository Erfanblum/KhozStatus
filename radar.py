import asyncio, os, logging
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

from models import FinalStatus
from agents import news_agent, decision_agent
from weather import fetch_all
from news import client, get_new_messages
from db import init_db, save_status, load_last_id, save_last_id

load_dotenv()
logging.basicConfig(level=logging.INFO)

# --- Health Check برای Koyeb و UptimeRobot ---
app = Flask(__name__)

@app.route("/health")
def health():
    return "ok", 200

def run_health():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

# --- حلقه رادار ---
async def radar_loop():
    await init_db()
    await client.start()
    while True:
        try:
            weather = await fetch_all()
            last_id = await load_last_id()
            msgs = await get_new_messages(last_id)
            new_last = last_id
            for m in msgs:
                if not m.text:
                    continue
                news = await news_agent.run(m.text)
                final = await decision_agent.run(
                    f"خبر: {news.data.model_dump_json()}\nهوا: {weather}"
                )
                await save_status(final.data)
                new_last = max(new_last, m.id)
                logging.info("Saved: %s", final.data.overall_status)
            await save_last_id(new_last)
        except Exception as e:
            logging.exception("Radar cycle failed: %s", e)
        await asyncio.sleep(600)  # 10 دقیقه

if __name__ == "__main__":
    Thread(target=run_health, daemon=True).start()
    asyncio.run(radar_loop())