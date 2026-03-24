import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8600375363:AAGbDHQHvSX2ZTIwrk6XwZAhwcgZ9FI-2Po"
CHANNEL_USERNAME = "@team_dev1l_here"

bot = telebot.TeleBot(TOKEN)

# JOIN CHECK
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# START
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if not is_joined(user_id):
        send_join_msg(message)
    else:
        send_main_menu(message)

# JOIN MESSAGE
def send_join_msg(message):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("📢 Join Channel", url="https://t.me/team_dev1l_here")
    )
    markup.add(
        InlineKeyboardButton("▶️ Subscribe YouTube", url="https://youtube.com/@devil_h4re?si=cqVTxZXLb0YcUmLw")
    )
    markup.add(
        InlineKeyboardButton("✅ I Joined", callback_data="check_join")
    )

    bot.send_message(
        message.chat.id,
        """🚫 ACCESS DENIED

👉 Bot use karne ke liye:

📢 Channel join karo  
▶️ YouTube subscribe karo  

⚠️ Fir "I Joined" dabao""",
        reply_markup=markup
    )

# VERIFY BUTTON
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    user_id = call.from_user.id

    if is_joined(user_id):
        bot.answer_callback_query(call.id, "✅ Verified")
        send_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Join first!")

# MAIN MENU
def send_main_menu(message):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton("📢 Deals", callback_data="deals"),
        InlineKeyboardButton("💰 Middleman", callback_data="middleman"),
        InlineKeyboardButton("🆘 Support", callback_data="support")
    )

    bot.send_message(
        message.chat.id,
        f"🔥 Welcome {message.from_user.first_name}\n\nBot Activated ✅",
        reply_markup=markup
    )

# BUTTON HANDLER
@bot.callback_query_handler(func=lambda call: True)
def buttons(call):

    if call.data == "deals":
        bot.send_message(call.message.chat.id, "📢 Deals section open")

    elif call.data == "middleman":
        bot.send_message(call.message.chat.id, "💰 Use middleman for safe deals")

    elif call.data == "support":
        bot.send_message(call.message.chat.id, "🆘 Contact: @Dev1l_h4re")

print("BOT RUNNING...")
bot.polling()
