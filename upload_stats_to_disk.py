import pandas as pd
import yadisk
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_FILE = "data/user_stats.csv"
EXCEL_FILE = "data/user_actions.xlsx"
YANDEX_DISK_TOKEN = "y0__xDUoO2kqveAAhix6DYgv-LQ4RJwYCHBPi86vgAt6HGWVRogaPUTVQ"
REMOTE_DIR = "/bot_logs"
REMOTE_PATH = f"{REMOTE_DIR}/user_actions.xlsx"

def convert_csv_to_xlsx():
    """Конвертация CSV в XLSX"""
    try:
        print("📄 Чтение CSV:", CSV_FILE)
        print("📁 Существует ли CSV:", os.path.exists(CSV_FILE))
        
        df = pd.read_csv(CSV_FILE, header=None, names=["user_id", "timestamp", "action"])
        print("✅ CSV прочитан, сохраняем XLSX...")
        
        df.to_excel(EXCEL_FILE, index=False)
        logger.info("CSV успешно конвертирован в XLSX")
        return True
    except Exception as e:
        logger.error(f"Ошибка при конвертации: {e}")
        return False

def upload_to_yandex_disk():
    """Загрузка файла XLSX на Яндекс.Диск"""
    try:
        y = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)

        if not y.check_token():
            logger.error("Недействительный токен")
            return False

        if not os.path.exists(EXCEL_FILE):
            logger.error("Файл XLSX не найден")
            return False

        if not y.exists(REMOTE_DIR):
            y.mkdir(REMOTE_DIR)
            logger.info(f"Создана директория {REMOTE_DIR} на Яндекс.Диске")

        y.upload(EXCEL_FILE, REMOTE_PATH, overwrite=True)
        logger.info("Файл успешно загружен на Диск")
        return True

    except Exception as e:
        logger.error(f"Ошибка при загрузке: {e}")
        return False

def backup_and_upload():
    """Основной процесс"""
    logger.info("Запуск переноса статистики")
    if convert_csv_to_xlsx():
        return upload_to_yandex_disk()
    return False

if __name__ == "__main__":
    success = backup_and_upload()
    if success:
        logger.info("Процедура завершена успешно")
    else:
        logger.error("Процедура завершилась с ошибкой")
