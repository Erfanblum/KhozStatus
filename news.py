import os
from telethon import TelegramClient
from telethon.sessions import StringSession

client = TelegramClient(
    StringSession(os.getenv("TELEGRAM_SESSION_STRING")),
    int(os.getenv("TELEGRAM_API_ID")),
    os.getenv("TELEGRAM_API_HASH"),
)

async def get_new_messages(last_id: int, channel: str = "@khozkhabar"):
    msgs = await client.get_messages(channel, min_id=last_id, limit=20)
    # min_id: فقط پیام‌هایی با ID بزرگ‌تر از last_id را برمی‌گرداند
    return msgs