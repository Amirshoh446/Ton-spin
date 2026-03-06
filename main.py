import os
import asyncio
import logging
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ==========================================
# ⚙️ ТАНЗИМОТИ АСОСӢ
# ==========================================
BOT_TOKEN = "7720127842:AAF6a0hU3Gmvgid7D635E1-gT4YCvvNT89c"
WEB_APP_URL = "https://spin-ton-rewards.lovable.app/"
CHANNEL_USERNAME = "@TonSpinEarn"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# 🌐 СЕРВЕРИ "БЕДОРКУНАК" (FLASK KEEP ALIVE)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive! 24/7"

def run_web_server():
    # Портро аз Render мегирем ё 8080 мемонем
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    # Серверро дар замина (background) ба кор медарорем
    t = threading.Thread(target=run_web_server)
    t.start()

# ==========================================
# 🛠 КЛАВИАТУРАИ АСОСӢ (Бо ҳифзи реферал)
# ==========================================
def get_main_keyboard(ref_id=None):
    """
    Агар одам бо ссылкаи рефералӣ омада бошад, мо ID-и даъваткунандаро 
    рост ба ссылкаи бозӣ мечаспонем.
    """
    url = WEB_APP_URL
    if ref_id:
        url = f"{WEB_APP_URL}?start_param={ref_id}"
        
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 ИГРАТЬ", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text="📢 Наш Канал", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]
    ])

# ==========================================
# 🚀 ФАРМОНИ /start
# ==========================================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    username = message.from_user.username or message.from_user.first_name or "Без имени"
    
    # Гирифтани ID-и реферал аз фармон (масалан: /start 123456789)
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    
    # Рост ба бозӣ даъват мекунем
    await message.answer(
        f"🎰 Добро пожаловать в **TON SPIN**, {username}!\n\n"
        f"Твоя цель — крутить рулетку, выполнять задания и зарабатывать криптовалюту TON.\n\n"
        f"Жми кнопку «ИГРАТЬ» ниже и забирай свой профит! 🚀",
        reply_markup=get_main_keyboard(ref_id),
        parse_mode="Markdown"
    )

# ==========================================
# ⚙️ АСОСӢ (АСИНХРОНӢ)
# ==========================================
async def main():
    # 1. Сервери бедоркунакро ба кор медарорем
    keep_alive()
    print("✅ БОТ ВА СЕРВЕР ОҒОЗ ШУДАНД!")
    
    # 2. Боти Телеграмро ба кор медарорем
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
