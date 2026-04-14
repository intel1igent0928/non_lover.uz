#!/bin/bash

# Запускаем бота в фоновом режиме
echo "Starting Telegram bot..."
python bot.py &

# Запускаем Django сайт (главный процесс)
echo "Starting Django (gunicorn)..."
exec gunicorn sourdough_site.wsgi:application --bind 0.0.0.0:$PORT
