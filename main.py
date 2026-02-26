import asyncio
import logging
import threading
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from supabase import create_client, Client
from flask import Flask
import os

# ==========================================
# ⚙️ ТАНЗИМОТ
# ==========================================
BOT_TOKEN = "7720127842:AAF6a0hU3Gmvgid7D635E1-gT4YCvvNT89c" 
WEB_APP_URL = "https://beautiful-kheer-77f324.netlify.app/"
SUPABASE_URL = "https://uzibbrtbyqklwfgjzhmz.supabase.co"
SUPABASE_KEY = "sb_publishable_PJC0qmQO0IfrNZSgUEfWSA_VuhcKRyI"
CHANNEL_URL = "https://t.me/TonSpinEarn" 

# ==========================================
# 🌐 СЕРВЕРИ "БЕДОРКУНАК" (FLASK KEEP ALIVE)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive! 24/7"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run_web_server)
    t.start()

# ==========================================
# 🤖 БОТИ TELEGRAM
# ==========================================
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message, command: CommandObject):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    referrer_id = command.args 

    try:
        user_response = supabase.table('users').select('*').eq('id', user_id).execute()
        
        if not user_response.data:
            data = {'id': user_id, 'balance': 0, 'spins': 10}
            if referrer_id and referrer_id != user_id:
                data['referred_by'] = referrer_id
            supabase.table('users').insert(data).execute()
            welcome_msg = f"🎉 <b>Welcome, {first_name}!</b>\nYou have received <b>10 Free Spins</b>."
        else:
            welcome_msg = f"👋 <b>Welcome back, {first_name}!</b>"

    except Exception as e:
        print(f"Error: {e}")
        welcome_msg = f"👋 <b>Welcome, {first_name}!</b>"

    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Play TON SPIN", web_app=WebAppInfo(url=WEB_APP_URL))
    builder.button(text="👥 Invite Friends", callback_data="invite")
    builder.button(text="📢 Official Channel", url=CHANNEL_URL)
    builder.adjust(1)

    await message.answer(
        f"{welcome_msg}\n\n"
        f"🎰 <b>TON SPIN - Play to Earn</b>\n"
        f"💎 Spin, complete tasks, and withdraw TON!\n\n"
        f"👇 <b>Main Menu:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "invite")
async def callback_invite(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ref_link = f"https://t.me/TonSpinEarn_bot?start={user_id}"
    await callback.message.answer(
        f"👥 <b>Invite & Earn!</b>\n\nLink: <code>{ref_link}</code>", 
        parse_mode="HTML"
    )
    await callback.answer()

async def main():
    # Аввал сервери бедоркунакро меёзонем
    keep_alive()
    print("✅ БОТ + СЕРВЕР ОҒОЗ ШУД!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
