import json
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from schema.user import TgIdUserSchema


load_dotenv()

router = APIRouter(
    tags=['bot'],
    prefix="/bot"
)

@router.post("/{tg_id}")
async def send_message(tg_id: int):
    bot_token = os.getenv("BOT_TOKEN")
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    message_text = "Поздравляю!\nВы выиграли в розыгрыше, просим вас подойти к сцене!"
    payload = {
        'chat_id': tg_id,
        'text': message_text
    }
    response = requests.post(url=send_message_url, data=payload)
    return json.loads(response.text)
