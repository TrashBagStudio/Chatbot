import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

answered = set()

def system_status():
    # тут можно расширять проверки: БД, API, файлы и т.д.
    if not TOKEN:
        return "⚠️ BOT_TOKEN не задан"
    return "✅ Всё штатно. Система работает нормально."

@dp.message(F.business_connection_id.is_not(None))
async def business_message_handler(message: Message):
    chat_id = message.chat.id

    if chat_id in answered:
        return

    await bot.send_message(
        chat_id=chat_id,
        business_connection_id=message.business_connection_id,
        text="Привет! Сейчас занят, отвечу позже."
    )

    answered.add(chat_id)


# 👇 НОВОЕ: обычные сообщения в личке с ботом
@dp.message(F.business_connection_id.is_(None))
async def normal_message_handler(message: Message):
    # можно ограничить только личные чаты:
    if message.chat.type != "private":
        return

    status = system_status()

    await message.answer(
        f"📊 Статус системы:\n{status}"
    )


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
