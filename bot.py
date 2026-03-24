import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import openai
from flask import Flask
import threading

# ================= CONFIG =================
BOT_TOKEN = "8600375363:AAGbDHQHvSX2ZTIwrk6XwZAhwcgZ9FI-2Po"
CHANNEL_USERNAME = "@team_dev1l_here"

GROUP_LINK = "https://t.me/+JfnzP14WwmE2MTA1"
YOUTUBE_LINK = "https://youtube.com/@devil_h4re"

openai.api_key = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# ================= FLASK (PORT FIX) =================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# ================= JOIN CHECK =================
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ================= FORCE JOIN =================
def send_join_msg(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Join Channel", url="https://t.me/team_dev1l_here")
    )
    markup.add(
        InlineKeyboardButton("✅ I Joined", callback_data="check_join")
    )
    bot.send_message(message.chat.id, "❌ पहले चैनल जॉइन करो!", reply_markup=markup)

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    if not is_joined(message.from_user.id):
        send_join_msg(message)
    else:
        send_main_menu(message)

# ================= MAIN MENU =================
def send_main_menu(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Channel", url="https://t.me/team_dev1l_here"),
        InlineKeyboardButton("🎬 YouTube", url=YOUTUBE_LINK)
    )
    markup.add(
        InlineKeyboardButton("💬 Support Group", url=GROUP_LINK)
    )

    bot.send_message(
        message.chat.id,
        "🔥 Devil AI Bot Ready!\n\nAsk anything 🤖",
        reply_markup=markup
    )

# ================= VERIFY BUTTON =================
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    if is_joined(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified!")
        send_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ अभी join नहीं किया!")

# ================= AI CHAT =================
@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    if not is_joined(message.from_user.id):
        send_join_msg(message)
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message.text}]
        )

        reply = response['choices'][0]['message']['content']
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, "⚠️ AI error ya API issue")

# ================= RUN =================
print("Bot running...")
bot.infinity_polling()
