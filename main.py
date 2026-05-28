python
import os
import requests
import telebot

TOKEN = os.getenv("8847386138:AAFAIbtJIFtAvrocKPi7vRDqIWDBti0RX2o")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send UID (Example: 123456789)")

@bot.message_handler(func=lambda m: True)
def check(message):

    uid = message.text.strip()

    # Demo API (မင်းနောက်မှပြောင်း)
    url = f"https://your-api.com/player?uid={uid}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            bot.reply_to(message, "Player not found")
            return

        data = r.json()

        name = data.get("name", "Unknown")
        region = data.get("region", "Unknown")

        bot.reply_to(
            message,
            f"Name: {name}\nRegion: {region}\nUID: {uid}"
        )

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

print("Bot Running...")
bot.infinity_polling()

