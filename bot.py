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

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    usuario = message.from_user.first_name
    time = datetime.now()
    func = who_am_i()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    bot.reply_to(message,"""Olá esse é o Bot da AGS Representantes Comerciais LTDA \
        \n \
        \n Use os um dos comandos abaixo: \n /start - Para iniciar o ChatBot \
        \n /help - Para mostrar Comandos \
        \n /ContasReceber - Para listar Títulos a Receber X Cliente \
        \n /PrecoItem - Para Consultar Produto por Ref. do Fabricante \
        \n /photo - Para ver uma voto legal!!!""")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btncReceber = types.KeyboardButton('/ContasReceber')
    btncPagar = types.KeyboardButton('/ContasPagar')
    btnPrecoItem = types.KeyboardButton('/PrecoItem')
    btnPhoto = types.KeyboardButton('/photo')
    markup.add(btncReceber, btncPagar, btnPrecoItem, btnPhoto)
    #markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Escolha um comando:", reply_markup=markup)

@bot.message_handler(commands=['photo'])
def send_photo(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    func = who_am_i()
    usuario = message.from_user.first_name
    time = datetime.now()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    img = open('_MG_1063.jpg', 'rb')
    bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()

@bot.message_handler(commands=['ContasReceber'])
def send_creceber(message):
    result = db.get_Contas_Receber()
    func = who_am_i()
    usuario = message.from_user.first_name
    time = datetime.now()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    bot.reply_to(message,result)

@bot.message_handler(commands=['ContasPagar'])
def send_cpagar(message):
    result = db.get_Contas_Receber()
    func = who_am_i()
    usuario = message.from_user.first_name
    time = datetime.now()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    bot.reply_to(message,result)

@bot.message_handler(commands=['PrecoItem'])
def send_precoitem(message):
    usuario = message.from_user.first_name
    time = datetime.now()
    func = who_am_i()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    
    msg = bot.reply_to(message, """ Informe o código/Referencia a ser pesquisado: """)
    bot.register_next_step_handler(msg, consultar_item)
            
def consultar_item(message):
    chat_id = message.chat.id
    codigo = message.text
    print("Produto a ser pesquisado:{}".format(codigo))
    result = db.get_Preço_Item(codigo)
    if not result:
        msg = str(codigo) + " - Referencia não localizada, tende outro Código!!!"
    else:
        msg = "Ref....: " + result[0][0] + "\n"
        msg +="Codigo.: " + result[0][1] + "\n"
        msg +="Desc...: " + result[0][2] + "\n" 
        msg +="Estoque: " + str(result[0][5]) + "\n \n"
        msg +="Preços.: " + "\n"
    for row in result:
        msg += str(row[3]) + " --> " + str(row[4]) + "\n"
    
    bot.send_message(chat_id, msg)

def who_am_i():
   stack = traceback.extract_stack()
   filename, codeline, funcName, text = stack[-2]
   return funcName


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
while True:
    time.sleep(0)