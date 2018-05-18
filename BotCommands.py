#bot_token = '523936015:AAEJ8-P5DdHSDXAsv8CBTsqv_I9umrlqjIs'
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
#https://python-telegram-bot.readthedocs.io/en/stable/

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters
import logging, sys, time, os
from ConexaoDB import Mongo_DB

#Banco de dados
banco = Mongo_DB()

#Bot Token
bot_token = '523936015:AAEJ8-P5DdHSDXAsv8CBTsqv_I9umrlqjIs'
updater = Updater(token=bot_token)

#Cria os handle's (comandos)
dispatcher = updater.dispatcher

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Inicia o bot
def start(bot, update):
    try:
        #keyboard = [[InlineKeyboardButton("Add note", callback_data='add'),
        #         InlineKeyboardButton("Remove note", callback_data='remove')],
        #        [InlineKeyboardButton("Edit note", callback_data='edit'),
        #        InlineKeyboardButton("Delete note", callback_data='delete')],
        #        [InlineKeyboardButton("See note", callback_data='see_one'),
        #        InlineKeyboardButton("See all notes", callback_data='see_all')]]

        #reply_markup = InlineKeyboardMarkup(keyboard)

        #update.message.reply_text("Hello, I'm {}! Please choose".format(bot.name), reply_markup=reply_markup)
        
        msg = "Hello, I'm {}. Please talk to me!".format(bot.name)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)
    except Exception as ex:
        msg = 'Error: {}'.format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)

#Encerra o bot
def stop(bot, update):
    try:
        msg = "I'm going... bye"
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)
    except Exception as ex:
        print(ex)

#Comandos disponíveis
def help(bot, update):
    try:
        msg = "/start - Begin a conversation\n{} {}".format("/stop - End's a conversation \n", 
        "/help - Show the commands")
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)
    except Exception as ex:
        print(ex)

#Adicionando uma nota
def add(bot, update, args):
    try:
        is_body = False
        title = ''
        body = ''

        for text in args:
            if text == ':':
                is_body = True
            else:
                if is_body == False:
                    title += "{} ".format(text)
                elif is_body == True:
                    body += "{} ".format(text)

        member = update.message.from_user.first_name
        note = {"titulo" : title,
                "anotacao": body,
                "autor": member}

        msg = "Added note... \n\n Titulo : {} \nAnotação : {} \nAutor : {}".format(
            note["titulo"], note["anotacao"], note["autor"])

        banco.insert(note)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)
    except Exception as ex:
        msg = 'Error: {}'.format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)

#Localizar uma nota
def find(bot, update, args):
    try:
        titulo = ''
        for text in args:
            titulo += '{} '.format(text)
        
        note = banco.consulta(titulo)
        msg = "Titulo : {} \nAnotação : {} \nAutor : {}".format(
            note["titulo"], note["anotacao"], note["autor"])

        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)
    except Exception as ex:
        msg = 'Error: {}'.format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)

def all_notes(bot, update):
    try:
        notes = banco.all_notes()

        for note in notes:
            msg = "Titulo : {} \nAnotação : {} \nAutor : {}".format(
            note["titulo"], note["anotacao"], note["autor"])

            bot.send_message(chat_id=update.message.chat_id, text=msg)
            print(msg)
            print()
    except Exception as ex:
        msg = 'Error: {}'.format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)

def delete_note(bot, update, args):
    try:
        titulo = ''
        for text in args:
            titulo += '{} '.format(text)

        retorno = banco.delete(titulo)
        bot.send_message(chat_id=update.message.chat_id, text=retorno)
        print(retorno)
    except Exception as ex:
        msg = 'Error: {}'.format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)

#Retorna a msg ao escolher o botão    
def action(bot, update):
    msg = str
    try:
        query = update.callback_query
        msg = "Selected option: {}".format(query.data)
        bot.edit_message_text(text=msg,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)
    except Exception as ex:
        msg = 'An error has occurred: {}'.format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)
        print(msg)
    
def test(bot, update, args):
    try:
        if list.count(args) > 0:
            for text in args:
                msg = ('You write: {}').format(text)
                bot.send_message(chat_id=update.message.chat_id, text=msg)
                print(msg)
        else:
           msg = ('Please enter at least one parameter.. ')
        bot.send_message(chat_id=update.message.chat_id, text=msg) 
    except Exception as ex:
        msg = ('Error: {}').format(ex)
        bot.send_message(chat_id=update.message.chat_id, text=msg)

#Comando não conhecido
def unknown(bot, update):
    msg="Sorry, I didn't understand that command."
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    print(msg)

#Define os comandos
start_handle = CommandHandler('start', start)
dispatcher.add_handler(start_handle)

stop_handle = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handle)

help_handle = CommandHandler('help', help)
dispatcher.add_handler(help_handle)

add_handle = CommandHandler('add', add, pass_args=True)
dispatcher.add_handler(add_handle)

find_handle = CommandHandler('find', find, pass_args=True)
dispatcher.add_handler(find_handle)

all_notes_handle = CommandHandler('all', all_notes)
dispatcher.add_handler(all_notes_handle)

delete_handle = CommandHandler('delete', delete_note, pass_args=True)
dispatcher.add_handler(delete_handle)

test_handle = CommandHandler('test', test, pass_args=True)
dispatcher.add_handler(test_handle)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

do_action = CallbackQueryHandler(action)
dispatcher.add_handler(do_action)

#Inicia o bot
updater.start_polling()

banco.altera_banco('DbPython', 'Teste')
      
#Mantem o programa sendo executado
while(False != True):
    print("Aguardando um comando...")
    time.sleep(5)
    

#os.startfile('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe')