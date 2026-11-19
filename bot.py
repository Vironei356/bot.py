import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")

# Твой проверенный ID для личных уведомлений:
ADMIN_ID = 6249438349

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище уже отправленных товаров, чтобы не повторяться
sent_products = set()

# Кнопки внизу экрана
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
    text = (
        "👋 <b>Добро пожаловать в бота скидок и халявы!</b>\n\n"
        "Нажимай на кнопки ниже:\n"
        "• <b>«🔵 Скидки OZON»</b> — горячие товары с артикулами\n"
        "• <b>«🎁 Халява»</b> — промокоды на продукты и доставку\n"
        "• <b>«📢 Наш канал»</b> — подписка на @productdiscounts2"
    )
    await message.answer(text, reply_markup=main_keyboard, parse_mode="HTML")

@dp.message(F.text == "🔵 Скидки OZON")
async def ozon_items_handler(message: types.Message):
    text = (
        "🔥 <b>ТОП ТОВАРЫ С OZON ПО АКЦИИ</b> 🔥\n\n"
        "<i>(Нажми на артикул, чтобы скопировать)</i>\n\n"
        "🎧 <b>1. Беспроводные наушники</b>\n"
        "💰 Цена: <s>1800 ₽</s> ➡️ <b>200 ₽</b>\n"
        "📦 Артикул: <code>3599088362</code>\n\n"
        "💨 <b>2. Воздуходувка (турбо-вентилятор)</b>\n"
        "💰 Цена: <s>3500 ₽</s> ➡️ <b>1300 ₽</b>\n"
        "📦 Артикул: <code>6230129353</code>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎧 Наушники за 200 ₽", url="https://www.ozon.ru/product/3599088362")],
        [InlineKeyboardButton(text="💨 Воздуходувка за 1300 ₽", url="https://www.ozon.ru/product/6230129353")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="HTML", disable_web_page_preview=True)

@dp.message(F.text == "🎁 Халява")
async def halyava_handler(message: types.Message):
    text = (
        "🛒 <b>ХАЛЯВА В «ПЯТЁРОЧКЕ»</b> 🛒\n\n"
        "1️⃣ Скидка 750 ₽: <code>pyyccmwhkr</code>\n"
        "2️⃣ Скидка 400 ₽: <code>psn2tjh6xx6</code>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Скидка 750 ₽", url="https://5dostavka.ru")],
        [InlineKeyboardButton(text="📦 Скидка 400 ₽", url="https://5dostavka.ru")]
    ])
    await message.answer(text, reply_markup=kb, parse_mode="HTML", disable_web_page_preview=True)

@dp.message(F.text == "📢 Наш канал")
async def channel_handler(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 Перейти в @productdiscounts2", url="https://t.me/productdiscounts2")]
    ])
    await message.answer("📢 Наш канал со скидками: @productdiscounts2", reply_markup=kb, parse_mode="HTML")

# Поисковые запросы авто-радара для категорий «Одежда» и «Товары для дома»
SEARCH_QUERIES = [
    "худи оверсайз",
    "футболка оверсайз",
    "плед пушистый",
    "постельное белье сатин",
    "ночник светильник",
    "органайзер для дома",
    "куртка демисезонная",
    "увлажнитель воздуха"
]

# Функция поиска больших скидок на Wildberries
async def fetch_wb_discounts(query: str):
    url = (
        f"https://search.wb.ru/exactmatch/ru/common/v5/search?"
        f"appType=1&curr=rub&dest=-1257786&query={query}&resultset=catalog&sort=discount&spp=30"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    found_items = []
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=12) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    products = data.get("data", {}).get("products", [])
                    for prod in products[:15]:
                        article = prod.get("id")
                        name = prod.get("name", "Товар")
                        
                        sizes = prod.get("sizes", [])
                        if not sizes:
                            continue
                            
                        price_info = sizes[0].get("price", {})
                        current_price = price_info.get("total", 0) // 100
                        old_price = price_info.get("basic", 0) // 100
                        
                        if old_price > current_price and current_price > 0:
                            discount = int(((old_price - current_price) / old_price) * 100)
                            # Фильтр: скидка от 60% до 95%
                            if 60 <= discount <= 95 and article not in sent_products:
                                found_items.append({
                                    "article": article,
                                    "name": name,
                                    "current_price": current_price,
                                    "old_price": old_price,
                                    "discount": discount
                                })
    except Exception as e:
        print(f"Ошибка поиска по '{query}': {e}")
        
    return found_items

# Автоматический радар: ищет товары и присылает тебе готовый пост
async def auto_radar_loop():
    await asyncio.sleep(10)
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text="📡 <b>Радар скидок WB активирован!</b>\n\nКатегории: <b>Одежда и Товары для дома</b>.\nБот сам ищет скидки от 60% до 95% и будет присылать готовые посты прямо сюда!",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка отправки подтверждения: {e}")

    while True:
        for q in SEARCH_QUERIES:
            items = await fetch_wb_discounts(q)
            for item in items:
                sent_products.add(item["article"])
                
                post_text = (
                    f"🔥 <b>НАХОДКА НА WILDBERRIES | СКИДКА -{item['discount']}%</b> 🔥\n\n"
                    f"📦 <b>{item['name']}</b>\n\n"
                    f"💰 Цена: <s>{item['old_price']} ₽</s> ➡️ <b>{item['current_price']} ₽</b>\n"
                    f"📦 Артикул: <code>{item['article']}</code> <i>(нажми, чтобы скопировать)</i>\n\n"
                    f"👉 <a href='https://www.wildberries.ru/catalog/{item['article']}/detail.aspx'>Открыть товар на WB</a>\n\n"
                    "📢 @productdiscounts2"
                )
                
                try:
                    await bot.send_message(
                        chat_id=ADMIN_ID,
                        text=post_text,
                        parse_mode="HTML",
                        disable_web_page_preview=False
                    )
                except Exception as err:
                    print(f"Ошибка отправки находки: {err}")
                
                await asyncio.sleep(25)
                
            await asyncio.sleep(15)

        await asyncio.sleep(1200)

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
    print("Бот и Авто-радар запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

