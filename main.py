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
