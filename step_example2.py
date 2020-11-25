import config
import telebot
from telebot import types
import time
from datetime import datetime
from dbags import DBAgs
import traceback

host = config.host
dbname = config.dbname
user = config.user
password = config.password
db = DBAgs(host, dbname, user, password)

TOKEN = config.token
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start'])
def welcome(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  item1 = types.KeyboardButton("clima")
  item2 = types.KeyboardButton("Meu criador")
  item3 = types.KeyboardButton("Lições")
  item4 = types.KeyboardButton("Ligações")
  item5 = types.KeyboardButton("Menu")
  markup.add(item1, item2, item3, item4, item5)
  bot.send_message(message.chat.id, "Olá",reply_markup=markup)
  bot.register_next_step_handler(message, testfunction)

def testfunction(message):
    if message.text == 'Meu criador':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Vkontakte")
        item2 = types.KeyboardButton("Telegram")
        item3 = types.KeyboardButton("Menu")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Escolha VKontakte ou Telegram', reply_markup=markup)
    elif message.text == 'Menu':
    	bot.register_next_step_handler(message, welcome)


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()