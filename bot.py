import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопки внизу экрана
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Старт"), KeyboardButton(text="🔵 Скидки OZON")],
        [KeyboardButton(text="🎁 Халява"), KeyboardButton(text="📢 Наш канал")]
    ],
    resize_keyboard=True
)

# Команда /start и кнопка "🚀 Старт"
@dp.message(Command("start"))
@dp.message(F.text == "🚀 Старт")
async def start_handler(message: types.Message):
    text = (
        "👋 <b>Добро пожаловать в бота со скидками и халявой!</b>\n\n"
        "Выбирай нужный раздел кнопками ниже:\n"
        "• <b>«🔵 Скидки OZON»</b> — секретные артикулы товаров по низким ценам\n"
        "• <b>«🎁 Халява»</b> — промокоды на доставку еды и продуктов\n"
        "• <b>«📢 Наш канал»</b> — переход в наш канал со скидками"
    )
    await message.answer(text, reply_markup=main_keyboard, parse_mode="HTML")

# Раздел "Скидки OZON"
@dp.message(F.text == "🔵 Скидки OZON")
async def ozon_items_handler(message: types.Message):
    text = (
        "🔥 <b>ТОП ТОВАРЫ С OZON ПО АКЦИИ</b> 🔥\n\n"
        "<i>(Нажми на артикул, чтобы моментально скопировать его)</i>\n\n"
        "🎧 <b>1. Беспроводные наушники</b>\n"
        "💰 Цена: <s>1800 ₽</s> ➡️ <b>200 ₽</b>\n"
        "📦 Артикул: <code>3599088362</code>\n\n"
        "💨 <b>2. Воздуходувка (турбо-вентилятор)</b>\n"
        "💰 Цена: <s>3500 ₽</s> ➡️ <b>1300 ₽</b>\n"
        "📦 Артикул: <code>6230129353</code>\n\n"
        "👇 <i>Или нажми на кнопку ниже, чтобы открыть сразу на OZON:</i>"
    )
    
    ozon_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎧 Наушники за 200 ₽", url="https://www.ozon.ru/product/3599088362")],
        [InlineKeyboardButton(text="💨 Воздуходувка за 1300 ₽", url="https://www.ozon.ru/product/6230129353")]
    ])
    
    await message.answer(
        text,
        reply_markup=ozon_inline_kb,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# Раздел "Халява" (Пятёрочка)
@dp.message(F.text == "🎁 Халява")
async def halyava_handler(message: types.Message):
    text = (
        "🛒 <b>ХАЛЯВА В ДОСТАВКЕ «ПЯТЁРОЧКА»</b> 🛒\n\n"
        "<i>(Нажми на промокод, чтобы быстро его скопировать!)</i>\n\n"
        "1️⃣ <b>Скидка 750 ₽</b> в Пятёрочке\n"
        "🔑 Промокод: <code>pyyccmwhkr</code>\n\n"
        "2️⃣ <b>Скидка 400 ₽</b> на заказ в Пятёрочке\n"
        "🔑 Промокод: <code>psn2tjh6xx6</code>\n\n"
        "👇 <i>Нажимай на кнопки ниже, чтобы открыть приложение Доставки:</i>"
    )
    
    pyaterochka_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Скидка 750 ₽ (Пятёрочка)", url="https://5dostavka.ru")],
        [InlineKeyboardButton(text="📦 Скидка 400 ₽ (Пятёрочка)", url="https://5dostavka.ru")]
    ])
    
    await message.answer(
        text,
        reply_markup=pyaterochka_kb,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# Раздел "Наш канал"
@dp.message(F.text == "📢 Наш канал")
async def channel_handler(message: types.Message):
    channel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 Открыть канал @productdiscounts2", url="https://t.me/productdiscounts2")]
    ])
    await message.answer(
        "📢 <b>Подписывайся на наш официальный канал @productdiscounts2!</b>\n\n"
        "Там самые горячие скидки, ошибки цен и эксклюзивные промокоды выходят каждый день 🔥\n\n"
        "Нажми кнопку ниже, чтобы перейти в канал 👇",
        reply_markup=channel_kb,
        parse_mode="HTML"
    )

# Фоновый веб-сервер для бесплатного тарифа Render
async def run_dummy_server():
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is running!"))
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
