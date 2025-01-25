7576609431:AAFHevv9TqZz48LCRV84eHYI3FkmDLepMfwimport telebot
import pandas as pd
import os

# Βάλε εδώ το token του bot
TOKEN = "TO_TOKEN_SOY"
bot = telebot.TeleBot(TOKEN)

# Λίστα προϊόντων (αυτή μπορεί να φορτωθεί από αρχείο στο μέλλον)
products = {
    "Σπίρτα": "001",
    "Γάλα": "002",
    "Νερό": "003"
}

orders = []  # Προσωρινή αποθήκευση παραγγελιών

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Γεια! Στείλε την παραγγελία σου σε μορφή 'Προϊόν Ποσότητα' ή 'Ποσότητα Προϊόν'.")

@bot.message_handler(func=lambda message: True)
def process_order(message):
    global orders
    text = message.text.strip()
    words = text.split()

    if len(words) == 2:
        # Αν είναι σε μορφή "Προϊόν Ποσότητα" ή "Ποσότητα Προϊόν"
        if words[0].isdigit():  # Αν το πρώτο είναι αριθμός
            quantity, product = int(words[0]), words[1]
        else:  # Αν το δεύτερο είναι αριθμός
            product, quantity = words[0], int(words[1])

        if product in products:
            orders.append({"Κωδικός": products[product], "Προϊόν": product, "Ποσότητα": quantity})
            bot.reply_to(message, f"Προστέθηκε: {product} - {quantity} τεμάχια.")
        else:
            bot.reply_to(message, "Άγνωστο προϊόν! Δοκίμασε ξανά.")

    elif text.lower() == "ολοκλήρωση":
        if orders:
            save_to_excel(orders, message.chat.id)
            orders = []  # Καθαρισμός λίστας
        else:
            bot.reply_to(message, "Δεν έχεις καταχωρημένες παραγγελίες.")

def save_to_excel(orders, chat_id):
    df = pd.DataFrame(orders)
    filename = f"order_{chat_id}.xlsx"
    df.to_excel(filename, index=False)

    with open(filename, "rb") as file:
        bot.send_document(chat_id, file)

    os.remove(filename)  # Διαγραφή αρχείου μετά την αποστολή

bot.polling()
