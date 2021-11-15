'''
telegram bot
команды:
/start, /help
/readme имя   - регистрация пользователя
/print	- характеристики пользователей
/time - текущее дата время
/ - помощь
'''

import telebot
import pprint
from bot_handler import BotHandler
import datetime

def is_registration( bot : telebot.TeleBot, message : telebot.types.Message):
	text = message.text
	id_user = message.chat.id
	user = bot_handler.get_name_user(id_user)
	if user == '?':
		bot.reply_to( message, "Я с Вами не знаком. Представьтесь, пожалуста!\n(команда: /readme ВашеИмя)" )
		return False
	else:
		return True
bot_handler = BotHandler()

TOKEN = '*'

# экземпляр класса Telebot
bot = telebot.TeleBot( TOKEN, parse_mode=None )

# обработчики сообщений ( фильтр )
@bot.message_handler(commands=['start','help'])
def send_welcome( message ):
	bot.reply_to(message, "Вы находитесь в боте занятий по Python!")
	if is_registration( bot, message ):
		id_user = message.chat.id
		user = bot_handler.get_name_user(id_user)
		bot.reply_to( message, f'Приветствую,{user}!' )

@bot.message_handler(commands=['print'])
def user_print( message ):
	if is_registration(bot, message):
		bot.reply_to( message, str( bot_handler ) )

	bot_handler.calc_chat( message.chat.id )

@bot.message_handler(commands=['time'])
def my_command( message ):
	today = datetime.datetime.today()
	d1 = today.strftime("%d-%m-%Y")  # 2017-04-05-00.18.00
	d2 = today.strftime("%H:%M:%S")
	bot.reply_to( message, f'Сегодня: {d1}, время: {d2}' )
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler( commands=['readme'] )
def my_read( message ):
	lst = message.text.split(' ')[1:]
	text = ' '.join(lst)

	bot_handler.set_name_user( message.chat.id, text)
	bot_handler.calc_chat( message.chat.id )

	today = datetime.datetime.today()
	d = today.strftime("%d-%m-%Y %H:%M:%S")  # 2017-04-05-00.18.00
	bot_handler.set_beg_time( message.chat.id, d )

	bot.reply_to( message, f"Я Вас запомнил! Приветствую,{text}!")
	bot_handler.calc_chat(message.chat.id)

@bot.message_handler( content_types=['text'] )
def my_text( message ):
	#print('content_types1',bot_handler)
	if is_registration( bot, message ):
		text = message.text
		id_user = message.chat.id
		user = bot_handler.get_name_user(id_user)

		bot.reply_to(message, f"Приветствую,{user}! Вы сказали:\'{text}\', а я повторил!")

	bot_handler.calc_chat(message.chat.id)
	#print('text',bot_handler)

bot.polling()


