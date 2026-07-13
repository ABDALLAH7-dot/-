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
