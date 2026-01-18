import telebot
from telebot import types
from flask import Flask
import os
from threading import Thread

# Koyeb Environment Variables වලින් දත්ත ලබා ගැනීම (ආරක්ෂිත ක්‍රමය)
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '6810255100'))

bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Xiter Bot is Running on Koyeb!"

def run():
    app.run(host='0.0.0.0', port=8080)

# සරල දත්ත ගබඩාව
user_wallets = {} 
stock = {
    "hg_10": {"name": "HG 10 DAYS", "price": 1800, "keys": []},
    "hg_30": {"name": "HG 30 DAYS", "price": 3500, "keys": []},
    "drip_1": {"name": "DRIP 1 DAY", "price": 700, "keys": []}
}

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🎮 Shop Now", callback_data="shop"),
               types.InlineKeyboardButton("💰 Balance", callback_data="bal"))
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.chat.id
    if uid not in user_wallets: user_wallets[uid] = 0
    bot.send_message(uid, "🚀 **Xiter V2 Store Online**\nභාණ්ඩ මිලදී ගැනීමට පහත බටන් එක ඔබන්න.", 
                     reply_markup=main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    uid = call.message.chat.id
    if call.data == "shop":
        markup = types.InlineKeyboardMarkup()
        for k, v in stock.items():
            markup.add(types.InlineKeyboardButton(f"{v['name']} (Stock: {len(v['keys'])})", callback_data=f"buy_{k}"))
        bot.edit_message_text("🎮 භාණ්ඩයක් තෝරන්න:", uid, call.message.message_id, reply_markup=markup)
    elif call.data == "bal":
        bot.answer_callback_query(call.id, f"ඔබේ ශේෂය: රු. {user_wallets.get(uid, 0)}", show_alert=True)

# Admin Commands
@bot.message_handler(commands=['add'])
def add_bal(m):
    if m.chat.id == ADMIN_ID:
        try:
            p = m.text.split()
            user_wallets[int(p[1])] = user_wallets.get(int(p[1]), 0) + int(p[2])
            bot.reply_to(m, "✅ Balance Added!")
        except: bot.reply_to(m, "Use: /add [ID] [Amount]")

if __name__ == "__main__":
    # Flask සර්වර් එක Background එකේ පණ ගැන්වීම
    Thread(target=run).start()
    print("Bot is starting on Koyeb...")
    bot.infinity_polling()

