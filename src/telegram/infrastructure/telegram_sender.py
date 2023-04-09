import os
import httpx
from dotenv import load_dotenv


load_dotenv()
URL = os.getenv('TELEGRAM_API_URL')
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')


class TelegramSender:

    def send_message(self, message):
        request = URL + TOKEN + '/sendMessage'
        data = {
            'chat_id': CHANNEL_ID,
            'text': message,
            'parse_mode': 'MarkdownV2'
        }
        response = httpx.post(request, data=data)
        self.__message_sent_log(response.status_code)

    def __message_sent_log(self, status_code):
        if 200 == status_code:
            print("Message sent succesfully")
        else:
            print("There was a problem sending this message")
