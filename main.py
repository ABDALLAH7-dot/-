import json
import requests
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, CITY, COUNTRY

USERS_FILE = "users.json"
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users = load_users()

    if chat_id not in users:
        users.append(chat_id)
        save_users(users)

    await update.message.reply_text(
        "✅ تم الاشتراك بنجاح.\n"
        "سيتم إرسال تذكير عند كل أذان لمدينة هيت."
    )
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    users = load_users()

    if chat_id in users:
        users.remove(chat_id)
        save_users(users)

    await update.message.reply_text(
        "❌ تم إلغاء الاشتراك.\nلن تصلك إشعارات الصلاة بعد الآن."
    )


def get_prayer_times():
    url = (
        f"https://api.aladhan.com/v1/timingsByCity"
        f"?city={CITY}&country={COUNTRY}&method=4"
    )

    response = requests.get(url, timeout=10).json()

    return response["data"]["timings"]


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    timings = get_prayer_times()

    text = (
        f"🕌 مواقيت الصلاة في {CITY}\n\n"
        f"الفجر: {timings['Fajr']}\n"
        f"الظهر: {timings['Dhuhr']}\n"
        f"العصر: {timings['Asr']}\n"
        f"المغرب: {timings['Maghrib']}\n"
        f"العشاء: {timings['Isha']}"
    )

    await update.message.reply_text(text)
async def next_prayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    timings = get_prayer_times()

    now = datetime.now()

    prayers = [
        ("الفجر", timings["Fajr"]),
        ("الظهر", timings["Dhuhr"]),
        ("العصر", timings["Asr"]),
        ("المغرب", timings["Maghrib"]),
        ("العشاء", timings["Isha"]),
    ]

    for name, time_str in prayers:
        prayer_time = datetime.strptime(time_str, "%H:%M").replace(
            year=now.year,
            month=now.month,
            day=now.day,
        )

        if prayer_time > now:
            await update.message.reply_text(
                f"🕌 الصلاة القادمة: {name}\n⏰ الوقت: {time_str}"
            )
            return

 await update.message.reply_text("انتهت صلوات اليوم.")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("next", next_prayer))

print("Bot Started...")

app.run_polling()
