import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍕 Скидки на еду", callback_data="food")],
        [InlineKeyboardButton(text="🔥 Скидки WB и OZON", callback_data="market")],
        [InlineKeyboardButton(text="📢 Канал со скидками", url="https://t.me/твой_канал")]
    ])
    await message.answer(
        "👋 Привет! Я нахожу горящие скидки и промокоды.\nВыбирай категорию ниже:",
        reply_markup=kb
    )

@dp.callback_query(lambda c: c.data == "food")
async def promo_food(callback: types.CallbackQuery):
    text = (
        "🍔 Промокоды на доставку:\n\n"
        "1. Купер: скидка 500 ₽ на заказ от 1500 ₽\n"
        "Промокод: ПРОМОКОД1\n\n"
        "2. Самокат: скидка 300 ₽ на первый заказ\n"
        "Промокод: ПРОМОКОД2"
    )
    await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "market")
async def promo_market(callback: types.CallbackQuery):
    text = (
        "🔥 Топ скидок:\n\n"
        "• Наушники: 390 ₽ вместо 1800 ₽\n"
        "• Смарт-часы: 690 ₽ вместо 2500 ₽"
    )
    await callback.message.answer(text)
    await callback.answer()

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
