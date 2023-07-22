from logging import getLogger, StreamHandler
from db_manager import SQLiteClient
from telegram_client import TelegramClient
from reminder import Reminder
import datetime
import time

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
TOKEN = ''
FROM_TIME = "10:00"
TO_TIME = "23:59"


database_client = SQLiteClient("users.db")
telegram_client = TelegramClient(token=TOKEN,
                                 base_url="https://api.telegram.org")
reminder = Reminder(database_client=database_client, telegram_client=telegram_client)
reminder.setup()

start_time = datetime.datetime.strptime(FROM_TIME, '%H:%M').time()
end_time = datetime.datetime.strptime(TO_TIME, '%H:%M').time()
while True:
    now_time = datetime.datetime.now().time()
    if start_time <= now_time <= end_time:
        reminder()
        time.sleep(30)
    else:
        time.sleep(3600)