from db_manager import SQLiteClient, UserActioner
from telegram_client import TelegramClient
from logging import getLogger, StreamHandler


logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
TOKEN = ''


class Reminder:
    GET_TASK = """
    SELECT chat_id FROM users WHERE last_update_date IS NULL OR last_update_date < date('now');
    """
    def __init__(self, telegram_client: TelegramClient, database_client: SQLiteClient):
        self.telegram_client = telegram_client
        self.database_client = database_client
        self.setted_up = False
        self.user_actioner = UserActioner(database_client)

    def setup(self):
        self.database_client.create_conn()
        self.setted_up = True

    def shutdown(self):
        self.database_client.create_conn()

    def notify(self, chat_ids: list):
        for chat_id in chat_ids:
            if len(self.user_actioner.get_user(chat_id))!=0:
                data = self.user_actioner.get_user(chat_id)
                res = self.telegram_client.post(method="sendMessage", params={
                    "text": f"эй, да, это спам, как насчет аникдота {data[1]}?",
                    "chat_id": chat_id
                })
            else:
                res = self.telegram_client.post(method="sendMessage", params={
                    "text": f"эй, да, это спам, как насчет аникдота?",
                    "chat_id": chat_id
                })
            logger.info(res)

    def execute(self):
        chat_ids = self.database_client.execute_select_command(self.GET_TASK)
        if chat_ids:
            self.notify(chat_ids=[tuple_from_database[0] for tuple_from_database in chat_ids])

    def __call__(self, *args, **kwargs):
        if not self.setted_up:
            logger.error("Resources in worker has not been setted up!")
            return
        self.execute()

if __name__ == "__main__":
    database_client = SQLiteClient("/telegram_bot/users.db")
    telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")

    reminder = Reminder(database_client=database_client, telegram_client=telegram_client)
    reminder.setup()
    reminder()


