import os
import asyncio
import threading
from flask import Flask

from radar import radar_loop
from userbot import build_application  # تابعی که Application را می‌سازد و برمی‌گرداند

app = Flask(__name__)

@app.route("/health")
def health():
    return "ok", 200

def run_health():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

async def run_userbot():
    application = build_application()
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    # تا ابد منتظر بمان تا polling متوقف نشود
    await asyncio.Event().wait()

async def run_all():
    await asyncio.gather(
        radar_loop(),
        run_userbot(),
    )

if __name__ == "__main__":
    threading.Thread(target=run_health, daemon=True).start()
    asyncio.run(run_all())