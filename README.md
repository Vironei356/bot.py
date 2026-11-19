import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍕 Скидки на еду", callback_data="food")],
        [InlineKeyboardButton(text="🔥 Скидки WB и OZON", callback_data="market")]
    ])
    await message.answer("👋 Привет! Я нахожу лучшие скидки и промокоды.\nВыбирай категорию:", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "food")
async def promo_food(callback: types.CallbackQuery):
    await callback.message.answer("🍔 Промокод Купер на 500 ₽: `EDA500`\nСамокат на 300 ₽: `EDA300`", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "market")
async def promo_market(callback: types.CallbackQuery):
    await callback.message.answer("🔥 Наушники с WB за 390 ₽ вместо 1800 ₽: https://ya.cc")
    await callback.answer()

# Микро-сервер для бесплатного тарифа Render
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
