import json
import os
import requests

from app.repositories.student_repo import StudentRepository
from app.repositories.image_repo import Image
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
CONTEST_URL = os.getenv("CONTEST_URL")

class TelegramBot:
    @staticmethod
    def send_message(chat_id: str,contest,data):
        """Sends a message with an inline button to a user."""

        data = {
            "chat_id": chat_id,
            "parse_mode": "Markdown", 
            "photo":data["imgurl"],
            "caption":f"{data["message"]}",
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": "🔥 Join 🔥", "web_app":{"url": f"{CONTEST_URL}/{contest["id"]}?tele_id={chat_id}"}}]
                ]
            })
        }
        
        response = requests.post(BASE_URL, data=data)
        return response.json()

    @staticmethod
    def send_message_to_all(contest,message,file):
        """Fetches all student telegram IDs and sends a message to each."""
        students = StudentRepository.get_students()
        upload_option = {"public_id":contest["id"]}
        uploadedData = Image.upload_image(file=file,upload_options=upload_option)
        for st in students:
            tele_id = st["telegram_id"] if "telegram_id" in st else "1656463485"
            data = {"imgurl":uploadedData["secure_url"],"message":message}
            TelegramBot.send_message(tele_id,contest,data=data)
           