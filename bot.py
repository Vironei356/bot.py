import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню с кнопками внизу экрана
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
        "Нажимай на кнопку **«🔵 Скидки OZON»**, чтобы забрать секретные артикулы товаров по низким ценам!\n"
        "И обязательно подпишись на наш канал через кнопку **«📢 Наш канал»**.",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

# Раздел "Скидки OZON" с артикулами и ссылками
@dp.message(F.text == "🔵 Скидки OZON")
async def ozon_items_handler(message: types.Message):
    text = (
        "🔥 **ТОП ТОВАРЫ С OZON ПО АКЦИИ** 🔥\n\n"
        "*(Нажми на артикул, чтобы моментально скопировать его)*\n\n"
        "🎧 **1. Беспроводные наушники**\n"
        "💰 Цена: ~~1800 ₽~~ ➡️ **200 ₽**\n"
        "📦 Артикул: `3599088362`\n\n"
        "💨 **2. Воздуходувка (турбо-вентилятор)**\n"
        "💰 Цена: ~~3500 ₽~~ ➡️ **1300 ₽**\n"
        "📦 Артикул: `6230129353`\n\n"
        "👇 *Либо нажми на кнопку ниже, чтобы открыть сразу на OZON:*"
    )
    
    ozon_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎧 Наушники за 200 ₽", url="https://www.ozon.ru/product/3599088362")],
        [InlineKeyboardButton(text="💨 Воздуходувка за 1300 ₽", url="https://www.ozon.ru/product/6230129353")]
    ])
    
    await message.answer(
        text,
        reply_markup=ozon_inline_kb,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# Раздел "Халява"
@dp.message(F.text == "🎁 Халява")
async def halyava_handler(message: types.Message):
    await message.answer(
        "🎁 **Промокоды на доставку еды:**\n\n"
        "🍕 **Купер**: скидка 500 ₽ от 1500 ₽ по промокоду `EDA500`\n"
        "🛴 **Самокат**: скидка 300 ₽ по промокоду `EDA300`",
        parse_mode="Markdown"
    )

# Раздел "Наш канал" с прямым переходом на @productdiscounts2
@dp.message(F.text == "📢 Наш канал")
async def channel_handler(message: types.Message):
    channel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 Открыть канал @productdiscounts2", url="https://t.me/productdiscounts2")]
    ])
    await message.answer(
        "📢 **Подписывайся на наш официальный канал @productdiscounts2!**\n\n"
        "Там самые горячие скидки, ошибки цен и эксклюзивные промокоды выходят каждый день 🔥\n\n"
        "Нажми кнопку ниже, чтобы перейти в канал 👇",
        reply_markup=channel_kb,
        parse_mode="Markdown"
    )

# Сервер для круглосуточной работы Render
async def run_dummy_server():
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is alive!"))
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await run_dummy_server()
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
