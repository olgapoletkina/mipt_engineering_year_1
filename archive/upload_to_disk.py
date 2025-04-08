import yadisk
import pandas as pd
from datetime import datetime
import os

OAUTH_TOKEN = "y0__xDUoO2kqveAAhju3TYg-d2L3hLmlqs1lUtFJ6Mh3zc3cXnUZn1mhQ"
CSV_PATH = "/home/poletkinaov/bot_yandexgpt/data/user_stats.csv"
XLSX_PATH = "/home/poletkinaov/bot_yandexgpt/data/user_stats.xlsx"
DISK_DIR = "/telegram_stats"
DISK_DEST = f"{DISK_DIR}/user_stats_{datetime.now().date()}.xlsx"


if not os.path.exists(CSV_PATH):
    print(f" Файл не найден: {CSV_PATH}")
    exit()

df = pd.read_csv(CSV_PATH, header=None)
df.columns = ["user_id", "timestamp", "action"]
df.to_excel(XLSX_PATH, index=False)
print("Конвертация завершена.")

y = yadisk.YaDisk(token=OAUTH_TOKEN)

if not y.check_token():
    print("Ошибка: недействительный токен")
    exit()
else:
    print("Успешная авторизация")

if not y.exists(DISK_DIR):
    y.mkdir(DISK_DIR)
    print(f"Папка создана: {DISK_DIR}")

y.upload(XLSX_PATH, DISK_DEST, overwrite=True)
print(f"Файл успешно загружен на Яндекс Диск: {DISK_DEST}")
