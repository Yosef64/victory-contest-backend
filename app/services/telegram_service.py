import json
import os
import requests

from app.repositories.student_repo import StudentRepository

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


class TelegramBot:
    @staticmethod
    def send_message(chat_id: str,contest):
        """Sends a message with an inline button to a user."""
        data = {
            "chat_id": chat_id,
            "text": "Click the button below:",
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": "Join", "url": "https://example.com"}]
                ]
            })
        }
        response = requests.post(BASE_URL, data=data)
        return response.json()

    @staticmethod
    def send_message_to_all(contest):
        """Fetches all student telegram IDs and sends a message to each."""
        students = StudentRepository.get_students()
        for st in students:
            TelegramBot.send_message(st.telegram_id,contest)
           