import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BusinessMessage
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

answered = set()

@dp.business_message()
async def business_message_handler(message: BusinessMessage):
    chat_id = message.chat.id

    if chat_id in answered:
        return

    await bot.send_message(
        chat_id=chat_id,
        business_connection_id=message.business_connection_id,
        text="Иди нахуй! Сейчас занят, отвечу позже."
    )

    answered.add(chat_id)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
