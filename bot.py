import telebot
import os
from dotenv import load_dotenv

# Φόρτωση του token από το αρχείο .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Μήνυμα καλωσορίσματος
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Γειά! Είμαι το bot για παραγγελίες.")

# Επεξεργασία παραγγελίας
@bot.message_handler(func=lambda message: True)
def process_order(message):
    bot.reply_to(message, f"Έλαβα: {message.text}")

# Τρέξε το bot
bot.polling()
