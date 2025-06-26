import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from registration.router import router
load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


dp = Dispatcher()
dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())