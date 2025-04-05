import requests
import os
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ✅ Replace with your actual tokens (already in use here)
TELEGRAM_BOT_TOKEN = "7908556401:AAHUjWAGSy72YmqARssxrfrLsP5NcBM1UkI"
OAUTH_TOKEN = "y0__xDUoO2kqveAAhjB3RMgzce-2xJywB-QwLpqs67Pg-LUauO_dMaZOQ"
FOLDER_ID = "b1g7d34r5kdavqia9fed"

# 📦 Logging user actions
def log_user_action(user_id, action):
    log_path = "data/user_stats.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, datetime.now().isoformat(), action])

# 🔐 Getting token
def get_iam_token():
    response = requests.post(
        'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        json={'yandexPassportOauthToken': OAUTH_TOKEN}
    )
    response.raise_for_status()
    return response.json()['iamToken']

# 🚀 Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    log_user_action(user_id, "/start")
    await update.message.reply_text("Привет! Я — Telegram-бот с YandexGPT!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    log_user_action(user_id, "/help")
    await update.message.reply_text("Просто напиши мне сообщение, и я постараюсь ответить 🤖")

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    log_user_action(user_id, "message")

    user_text = update.message.text
    iam_token = get_iam_token()

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
        "completionOptions": {
            "temperature": 0.3,
            "maxTokens": 1000
        },
        "messages": [{"role": "user", "text": user_text}]
    }

    URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    response = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {iam_token}",
            "Content-Type": "application/json"
        },
        json=data
    ).json()

    answer = response.get('result', {}) \
                     .get('alternatives', [{}])[0] \
                     .get('message', {}) \
                     .get('text', "🤖 Извините, я не смог сгенерировать ответ.")
    
    await update.message.reply_text(answer)

# 🧠 Entry point
def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
