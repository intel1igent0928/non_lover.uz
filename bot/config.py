# bot/config.py

import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", 0))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
CARD_NUMBER = os.getenv("CARD_NUMBER", "8600 0000 0000 0000")
