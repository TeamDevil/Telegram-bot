import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
import os
from flask import Flask
import threading

# ================= CONFIG =================
TOKEN = "8600375363:AAGbDHQHvSX2ZTIwrk6XwZAhwcgZ9FI-2Po"
CHANNEL_USERNAME = "@team_dev1l_here"
YOUTUBE_LINK = "https://youtube.com/@yourchannel"
GROUP_LINK = "https://t.me/+JfnzP14WwmE2MTA1"

openai.api_key = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)

# ================= DATABASE =================
warns = {}

# ================= FLASK =================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ================= JOIN CHECK =================
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

def join_msg(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")
    )
    bot.reply_to(message, "❌ पहले चैनल जॉइन करो!", reply_markup=markup)

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    if not is_joined(message.from_user.id):
        return join_msg(message)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"),
        InlineKeyboardButton("🎥 YouTube", url=YOUTUBE_LINK)
    )
    markup.add(
        InlineKeyboardButton("💬 Support Group", url=GROUP_LINK)
    )

    bot.reply_to(message, "🔥 Devil AI Bot Ready!\n\nAsk anything 🤖", reply_markup=markup)

# ================= HELP =================
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, """
📌 Commands:
/start /help /id

⚠️ Admin:
/warn /ban /unban /mute /unmute
""")

# ================= ID =================
@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(message, f"🆔 {message.from_user.id}")

# ================= ADMIN CHECK =================
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# ================= WARN =================
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if not message.reply_to_message:
        return bot.reply_to(message, "Reply to user")

    user_id = message.reply_to_message.from_user.id
    warns[user_id] = warns.get(user_id, 0) + 1

    bot.reply_to(message, f"⚠️ Warn {warns[user_id]}/3")

    if warns[user_id] >= 3:
        bot.kick_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "🚫 User banned (3 warns)")

# ================= BAN =================
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "🚫 Banned")

# ================= UNBAN =================
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "✅ Unbanned")

# ================= MUTE =================
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
        bot.reply_to(message, "🔇 Muted")

# ================= UNMUTE =================
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True)
        bot.reply_to(message, "🔊 Unmuted")

# ================= AI =================
@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    if not is_joined(message.from_user.id):
        return join_msg(message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )

        reply = response['choices'][0]['message']['content']
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"❌ {e}")

# ================= RUN =================
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_flask()
