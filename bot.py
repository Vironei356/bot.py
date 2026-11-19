import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню внизу экрана
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Старт"), KeyboardButton(text="🔵 Скидки OZON")],
        [KeyboardButton(text="🎁 Халява"), KeyboardButton(text="📢 Наш канал")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
@dp.message(F.text == "🚀 Старт")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 **Добро пожаловать в бота со скидками и халявой!**\n\n"
        "Выбирай нужный раздел кнопками ниже:\n"
        "• **«🔵 Скидки OZON»** — секретные артикулы товаров по низким ценам\n"
        "• **«🎁 Халява»** — промокоды на доставку еды и продуктов\n"
        "• **«📢 Наш канал»** — перех
