import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import latest_status

async def status_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    s = await latest_status()
    if not s:
        await update.message.reply_text("هنوز وضعیتی ثبت نشده.")
        return
    await update.message.reply_text(format_status(s))

def format_status(s: dict) -> str:
    icon = {"closed":"🔴","likely":"🟡","open":"🟢"}.get(s["overall_status"],"⚪")
    cities = "، ".join(s["affected_cities"]) if s["affected_cities"] else "—"
    return (
        f"{icon} **وضعیت: {s['overall_status']}**\n"
        f"شهرها: {cities}\n"
        f"دلیل: {s['primary_reason']}\n"
        f"آخرین به‌روزرسانی: {s['created_at']}\n"
        f"منبع: @khozkhabar"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("USER_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("status", status_cmd))
    app.run_polling()