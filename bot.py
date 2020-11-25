#!/usr/bin/env python3
import config
import telebot
from telebot import types
from telebot import util
import time
from datetime import datetime
from dbags import DBAgs
import traceback


print(str(datetime.now()) + " --> Bot Iniciado!")


host = config.host
dbname = config.dbname
user = config.user
password = config.password
db = DBAgs(host, dbname, user, password)

TOKEN = config.token
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help','Voltar'])
def handle_start_help(message):
    usuario = message.from_user.first_name
    time = datetime.now()
    func = who_am_i()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    """bot.reply_to(message,Olá esse é o Bot da AGS Representantes Comerciais LTDA \
        \n \
        \n Use os um dos comandos abaixo: \n /start | /help  - Para iniciar ou mostrar comandos do ChatBot \
        \n /Financeiro - Para listar Títulos a Pagar X Receber \
        \n /PrecoItem - Para Consultar Produto por Ref. do Fabricante \
        \n /photo - Para ver uma voto legal!!!)
    """
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btnFinanceiro = types.KeyboardButton('/Financeiro')
    btnPrecoItem = types.KeyboardButton('/PrecoItem')
    btnPhoto = types.KeyboardButton('/photo')
    btnVoltar = types.KeyboardButton('/Voltar')
    markup.add(btnFinanceiro, btnPrecoItem, btnPhoto,btnVoltar) #btncReceber, btncPagar, )
    #markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Menu Principal: \nEscolha um comando:", reply_markup=markup)

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

@bot.message_handler(commands=['Financeiro'])
def financeiro(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btncReceber = types.KeyboardButton('/Contas Receber')
    btncPagar = types.KeyboardButton('/Contas Pagar')
    btnVoltar = types.KeyboardButton('/Voltar')
    markup.add(btncReceber, btncPagar,btnVoltar)
    
    msg = bot.reply_to(message, "Selecione a consulta:", reply_markup=markup)
    func = who_am_i()
    usuario = message.from_user.first_name
    time = datetime.now()
    
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))  
    bot.register_next_step_handler(msg, consulta_Financeiro)
    
#@bot.message_handler(commands=['ConsultarFinanceiro'])
def consulta_Financeiro(message):
    msg = ""
    #print(message)
    if message.text == '/Contas Receber' :
        result = db.get_Contas_Receber()
        #print(result)
        if not result:
            msg = "Não encontrado valores na consulta!!!"
        else:
            for row in result:
                msg += "Nome.: " + row[1] + "\n"
                msg +="Título: " + str(row[2]) + "\n" 
                msg +="Parcela: " + str(row[3]) + "\n"
                msg +="Data Emissão: " + str(row[4]) + "\n" 
                msg +="Data Vencimento: " + str(row[5]) + "\n"
                msg +="Valor Título...: " + str(row[6]) + "\n"
                msg +="Saldo Aberto...: " + str(row[7]) + "\n"
                msg +="---------------------------------------------------- \n"
            func = who_am_i()
            usuario = message.from_user.first_name
            time = datetime.now()
            print('{} - Bot acionado pelo Usuário: {} - Função: {}  - Digitado: {}'.format(time, usuario, func, message.text))
            #print(message)
            #print(msg)
            splitted_msg = util.split_string(msg, 3000)
            for text in splitted_msg:
	            #tb.send_message(chat_id, text)
                bot.reply_to(message, text)
        
        msg = bot.reply_to(message, """ Clique em /Voltar ou Digite: /Voltar """)
        bot.register_next_step_handler(message, handle_start_help)
        
    else:
        if message.text == '/Contas Pagar' :
                result = db.get_Contas_Pagar()
                #print(result)
                if not result:
                    msg = "Não encontrado valores na consulta!!!"
                else:
                    for row in result:
                        msg += "Nome.: " + row[1] + "\n"
                        msg +="Título: " + str(row[2]) + "\n" 
                        msg +="Parcela: " + str(row[3]) + "\n"
                        msg +="Data Emissão: " + str(row[4]) + "\n" 
                        msg +="Data Vencimento: " + str(row[5]) + "\n"
                        msg +="Valor Título...: " + str(row[6]) + "\n"
                        msg +="Saldo Aberto...: " + str(row[7]) + "\n"
                        msg +="---------------------------------------------------- \n"
                    func = who_am_i()
                    usuario = message.from_user.first_name
                    time = datetime.now()
                    print('{} - Bot acionado pelo Usuário: {} - Função: {}  - Digitado: {}'.format(time, usuario, func, message.text))
                    #print(message)
                    #print(msg)
                    splitted_msg = util.split_string(msg, 3000)
                    for text in splitted_msg:
                        #tb.send_message(chat_id, text)
                        bot.reply_to(message, text)
                
                msg = bot.reply_to(message, """ Clique em /Voltar ou Digite: /Voltar """)
                bot.register_next_step_handler(message, handle_start_help)
                    
@bot.message_handler(commands=['PrecoItem'])
def send_precoitem(message):
    usuario = message.from_user.first_name
    time = datetime.now()
    func = who_am_i()
    print('{} - Bot acionado pelo Usuário: {} - Função: {}'.format(time, usuario, func))
    
    msg = bot.reply_to(message, """ Informe o código/Referencia a ser pesquisado: """)
    if msg =="/Voltar":
        bot.register_next_step_handler(message, handle_start_help)
    else:
        bot.register_next_step_handler(message, consultar_item)
    
def consultar_item(message):
    if message.text == "/Voltar":
        bot.register_next_step_handler(message, handle_start_help)
    else:
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
        
        bot.reply_to(message, msg)
        
        msg = bot.reply_to(message, "Digite Novo Código para pesquisar? \n /Voltar = sair")
        if msg.text == "/Voltar":
            #print("entrei na linha 121")
            bot.register_next_step_handler(message, handle_start_help)
        else:
            bot.register_next_step_handler(message, consultar_item)


def who_am_i():
   stack = traceback.extract_stack()
   filename, codeline, funcName, text = stack[-2]
   return funcName


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
#bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
#bot.load_next_step_handlers()

bot.polling()
while True:
    time.sleep(0)
