import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6249438349

bot = Bot(token=TOKEN)
dp = Dispatcher()

sent_products = set()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Старт"), KeyboardButton(text="🔵 Скидки OZON")],
        [KeyboardButton(text="🎁 Халява"), KeyboardButton(text="📢 Наш канал")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
@dp.message(F.text == "🚀 Старт")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 <b>Бот скидок активен!</b>\n\nЯ ищу скидки на WB от 40% до 95% и присылаю их админу.",
        reply_markup=main_keyboard,
        parse_mode="HTML"
    )

@dp.message(F.text == "🔵 Скидки OZON")
async def ozon_items_handler(message: types.Message):
    text = (
        "🔥 <b>ТОП ТОВАРЫ С OZON</b> 🔥\n\n"
        "🎧 <b>Наушники:</b> <s>1800 ₽</s> ➡️ <b>200 ₽</b> | Арт: <code>3599088362</code>\n"
        "💨 <b>Воздуходувка:</b> <s>3500 ₽</s> ➡️ <b>1300 ₽</b> | Арт: <code>6230129353</code>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎧 Наушники 200 ₽", url="https://www.ozon.ru/product/3599088362")],
        [InlineKeyboardButton(text="💨 Воздуходувка 1300 ₽", url="https://www.ozon.ru/product/6230129353")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@dp.message(F.text == "🎁 Халява")
async def halyava_handler(message: types.Message):
    text = (
        "🛒 <b>ПЯТЁРОЧКА ДОСТАВКА</b>\n\n"
        "1️⃣ Скидка 750 ₽: <code>pyyccmwhkr</code>\n"
        "2️⃣ Скидка 400 ₽: <code>psn2tjh6xx6</code>"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text == "📢 Наш канал")
async def channel_handler(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 Перейти в @productdiscounts2", url="https://t.me/productdiscounts2")]
    ])
    await message.answer("📢 Наш канал:", reply_markup=kb, parse_mode="HTML")

# Популярные запросы по одежде и товарам для дома
SEARCH_QUERIES = [
    "худи оверсайз",
    "плед пушистый",
    "футболка оверсайз",
    "увлажнитель воздуха",
    "постельное белье сатин",
    "куртка демисезонная",
    "ночник светильник",
    "органайзер для дома"
]

async def fetch_wb_discounts(query: str):
    url = (
        f"https://search.wb.ru/exactmatch/ru/common/v5/search?"
        f"appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog&sort=discount&spp=30"
    )
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    found = []
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    products = data.get("data", {}).get("products", [])
                    for prod in products[:20]:
                        art = prod.get("id")
                        name = prod.get("name", "Товар")
                        sizes = prod.get("sizes", [])
                        if not sizes:
                            continue
                        p_info = sizes[0].get("price", {})
                        cur_p = p_info.get("total", 0) // 100
                        old_p = p_info.get("basic", 0) // 100
                        
                        if old_p > cur_p and cur_p > 0:
                            disc = int(((old_p - cur_p) / old_p) * 100)
                            
                            # ФИЛЬТР: ТОЛЬКО СКИДКИ ОТ 40% ДО 95%
                            if 40 <= disc <= 95 and art not in sent_products:
                                found.append({
                                    "art": art,
                                    "name": name,
                                    "cur_p": cur_p,
                                    "old_p": old_p,
                                    "disc": disc
                                })
    except Exception as e:
        print(f"Ошибка WB {query}: {e}")
    return found

async def auto_radar_loop():
    # Первое тестовое сообщение через 10 секунд
    await asyncio.sleep(10)
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text="📡 <b>Радар WB активен!</b>\nИщу товары со скидками <b>от 40% до 95%</b> в категориях «Одежда» и «Дом»...",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")

    while True:
        for q in SEARCH_QUERIES:
            items = await fetch_wb_discounts(q)
            for item in items:
                sent_products.add(item["art"])
                msg = (
                    f"🔥 <b>НАХОДКА С WB | СКИДКА -{item['disc']}%</b> 🔥\n\n"
                    f"📦 <b>{item['name']}</b>\n\n"
                    f"💰 Цена: <s>{item['old_p']} ₽</s> ➡️ <b>{item['cur_p']} ₽</b>\n"
                    f"📦 Артикул: <code>{item['art']}</code> <i>(нажми, чтобы скопировать)</i>\n\n"
                    f"👉 https://www.wildberries.ru/catalog/{item['art']}/detail.aspx\n\n"
                    "📢 @productdiscounts2"
                )
                try:
                    await bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="HTML")
                except Exception as err:
                    print(f"Ошибка отправки поста: {err}")
                
                await asyncio.sleep(15)  # интервал 15 секунд между сообщениями
            await asyncio.sleep(10)

        await asyncio.sleep(600)  # сканирование каждые 10 минут

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
    asyncio.create_task(auto_radar_loop())
    print("Бот работает!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
