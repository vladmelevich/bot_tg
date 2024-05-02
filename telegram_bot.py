import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('')
us_name = None
two_name = None

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('vladgih.db')
    cur = conn.cursor()
    zap1 = """CREATE TABLE IF NOT EXISTS VLADGH(name TEXT, surname TEXT,kod_slovo TEXT)"""
    cur.execute(zap1)
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('зарегистрироваться 1',callback_data='рег')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('авторезироваться 2', callback_data='авт')
    markup.row(btn2)
    bot.send_message(message.chat.id,'Привет этот бот может считать количество букв в слове которое ты введешь и может считать факториал числа которое ты введешь но что бы это все делать ты должен зарегистрироваться кнопка(1) либо авторезироваться кнопка(2)',reply_markup=markup)


@bot.callback_query_handler(func=lambda callback:True)
def callback_db(callback):
    if callback.data == 'рег':
        bot.send_message(callback.message.chat.id, 'введите имя')
        bot.register_next_step_handler(callback.message,user_name)
    elif callback.data =='авт':
        bot.send_message(callback.message.chat.id,'введите кодовое слово которое вы вводили при регистрации')
        bot.register_next_step_handler(callback.message,sign_up)
    if callback.data == 'сумм':
        bot.send_message(callback.message.chat.id, 'введите слово')
        bot.register_next_step_handler(callback.message, podchet)
    elif callback.data == 'фактор':
        bot.send_message(callback.message.chat.id, 'введите цифру для подсчета факториала')
        bot.register_next_step_handler(callback.message,factor)

def user_name(message):
    global us_name
    us_name = message.text
    bot.send_message(message.chat.id, 'введите фамилию')
    bot.register_next_step_handler(message, sur_user_name)

def sur_user_name(message):
    global two_name
    two_name = message.text
    bot.send_message(message.chat.id, 'введите кодовое слово')
    bot.register_next_step_handler(message, kod_slovo)

def kod_slovo(message):
    kod_text = message.text
    conn = sqlite3.connect('vladgih.db')
    cur = conn.cursor()
    zap2 = f"""INSERT INTO VLADGH(name,surname,kod_slovo) VALUES('{us_name}','{two_name}','{kod_text}')"""
    cur.execute(zap2)
    conn.commit()
    cur.close()
    conn.close()
    bot_mosz(message)


def sign_up(message):
    kod_slov_up = message.text
    list = []
    list.append(kod_slov_up)
    conn = sqlite3.connect('vladgih.db')
    cur = conn.cursor()
    zap2 = """SELECT * FROM VLADGH WHERE kod_slovo=(?)"""
    cur.execute(zap2,list)
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        bot.send_message(message.chat.id, 'вы авторизованы')
        bot_mosz(message)
    else:
        bot.send_message(message.chat.id, 'вы не авторизованы не вверное кодовое слово')

def bot_mosz(message):
    markup = types.InlineKeyboardMarkup()
    b = types.InlineKeyboardButton('сумма',callback_data='сумм')
    markup.row(b)
    b2 = types.InlineKeyboardButton('факториал',callback_data='фактор')
    markup.row(b2)
    bot.send_message(message.chat.id,'после того как вы авторезировались этот бот может либо посчитать сумму количества всех символов слова которого вы введети(1) либо факториал число которое вы введете(2) это вы хотите 1 то нажмите на кнопку сумма если хотите 2 нажмите на кнопку факториал',reply_markup=markup)


def podchet(message):
    slovo = message.text
    summ = 0
    for i in range(len(slovo)):
        summ +=i
    bot.send_message(message.chat.id,f'сумма количества элементов слова равна, {summ}')

def factor(message):
    factorial = int(message.text)
    f = 1
    for i in range(1,factorial+1):
        f= f*i
    bot.send_message(message.chat.id, f'факториал данного числа равен,{f}')



bot.polling(none_stop=True)



