import os
import telebot
from telebot import types

# Preia token-ul din variabilele de mediu (setate pe Render) sau introdu-l direct pentru teste
TOKEN = os.getenv('BOT_TOKEN', 'INTRODU_TOKEN_UL_AICI_DACA_TESTezi_LOCAL')
bot = telebot.TeleBot(TOKEN)

# Dicționar simplu pentru a salva utilizatorii înregistrați (în memorie)
registered_users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📝 Înregistrează-te anonim"))
    bot.send_message(
        message.chat.id, 
        "Salut! Acesta este un bot de discuții anonime. Apasă pe butonul de mai jos pentru a te înregistra.", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "📝 Înregistrează-te anonim")
def register_user(message):
    user_id = message.from_user.id
    registered_users[user_id] = {
        "username": message.from_user.username or "Anonim",
        "registered": True
    }
    bot.send_message(
        message.chat.id, 
        "✅ Te-ai înregistrat cu succes! Acum poți trimite orice mesaj, iar acesta va fi tratat anonim."
    )

@bot.message_handler(func=lambda message: True)
def handle_anonymous_message(message):
    user_id = message.from_user.id
    if user_id not in registered_users:
        bot.send_message(message.chat.id, "Te rog să te înregistrezi mai întâi folosind comanda /start.")
        return
    
    # Aici poți redirecționa mesajul către un grup de admini sau alt utilizator
    bot.send_message(message.chat.id, f"🥷 [Mesaj Anonim trimis]: {message.text}")

# Pornirea botului în modul Polling
if __name__ == "__main__":
    print("Botul a pornit...")
    bot.infinity_polling()
