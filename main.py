import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# === ⚙️ ТАНЗИМОТИ АСОСӢ ===
BOT_TOKEN = "7720127842:AAF6a0hU3Gmvgid7D635E1-gT4YCvvNT89c"
WEB_APP_URL = "https://spin-ton-rewards.lovable.app/"
CHANNEL_USERNAME = "@TonSpinEarn"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === 🛠 КЛАВИАТУРАИ АСОСӢ (Бо ҳифзи реферал) ===
def get_main_keyboard(ref_id=None):
    """
    Агар одам бо ссылкаи рефералӣ омада бошад, мо ID-и даъваткунандаро 
    рост ба ссылкаи бозӣ мечаспонем, то ки Lovable онро хонда тавонад.
    """
    url = WEB_APP_URL
    if ref_id:
        url = f"{WEB_APP_URL}?start_param={ref_id}"
        
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 ИГРАТЬ", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text="📢 Наш Канал", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]
    ])

# === 🚀 ФАРМОНИ /start ===
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    username = message.from_user.username or message.from_user.first_name or "Без имени"
    
    # Гирифтани ID-и реферал аз фармон (масалан: /start 123456789)
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    
    # Рост ба бозӣ даъват мекунем (бе ягон проверки подписка)
    await message.answer(
        f"🎰 Добро пожаловать в **TON SPIN**, {username}!\n\n"
        f"Твоя цель — крутить рулетку, выполнять задания и зарабатывать криптовалюту TON.\n\n"
        f"Жми кнопку «ИГРАТЬ» ниже и забирай свой профит! 🚀",
        reply_markup=get_main_keyboard(ref_id),
        parse_mode="Markdown"
    )

# === 🌐 ВЕБ-СЕРВЕР БАРОИ RENDER (Ки бот хоб наравад) ===
async def handle_ping(request):
    return web.Response(text="TON SPIN Bot is running smoothly! 🚀")

async def main():
    # Сохтани сервери хурд барои банд кардани Порт дар Render
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Веб-сервер дар порти {port} ба кор даромад.")

    # Ба кор даровардани худи Бот
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

