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
