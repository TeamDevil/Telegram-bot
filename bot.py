import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os

# ====== CONFIG ======
TOKEN = "8600375363:AAGbDHQHvSX2ZTIwrk6XwZAhwcgZ9FI-2Po"
CHANNEL = "@CHANNEL = "@team_dev1l_here""   # apna channel username

bot = telebot.TeleBot(TOKEN)

# ====== FLASK (Render fix) ======
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# ====== JOIN CHECK ======
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ====== JOIN BUTTON ======
def join_msg(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL.replace('@','')}"),
        InlineKeyboardButton("✅ Joined", callback_data="check")
    )
    bot.send_message(message.chat.id, "पहले चैनल जॉइन करो!", reply_markup=markup)

# ====== START ======
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if not is_joined(user_id):
        join_msg(message)
        return

    bot.reply_to(message, "👋 Hello!\nMain AI Bot hu 🤖\nMujhse kuch bhi pucho!")

# ====== CALLBACK ======
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "check":
        if is_joined(call.from_user.id):
            bot.answer_callback_query(call.id, "Verified ✅")
            bot.send_message(call.message.chat.id, "अब use karo bot 😎")
        else:
            bot.answer_callback_query(call.id, "❌ Join nahi kiya")

# ====== SIMPLE AI CHAT ======
def ai_reply(text):
    text = text.lower()

    if "hello" in text or "hi" in text:
        return "Hello 👋 kaise ho?"
    elif "kaun ho" in text:
        return "Main AI Telegram Bot hu 🤖"
    elif "love" in text:
        return "Love is complicated bro ❤️🙂"
    elif "time" in text:
        import datetime
        return str(datetime.datetime.now())
    else:
        return "Samajh nahi aaya 😅\nThoda aur clear bolo"

# ====== GROUP + PRIVATE CHAT ======
@bot.message_handler(func=lambda message: True)
def chat(message):
    user_id = message.from_user.id

    if not is_joined(user_id):
        return

    reply = ai_reply(message.text)
    bot.reply_to(message, reply)

# ====== RUN ======
keep_alive()
bot.infinity_polling()
