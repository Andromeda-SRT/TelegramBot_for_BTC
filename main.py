import json
import telebot
import requests
import time
import tcn

from telebot import types


bot = telebot.TeleBot(tcn.TOKEN)
url = 'https://blockchain.info/ru/ticker'

def putData():
    return requests.get(url).text
data_c = json.loads(putData())


keyboard_txt = types.ReplyKeyboardMarkup(resize_keyboard=True) # объявление клавиатуры для кнопок под полем ввода сообщения
btn1 = types.KeyboardButton('Курс BTC')
btn2 = types.KeyboardButton('Помощь')
keyboard_txt.add(btn1, btn2) # добавление кнопок в клавиатуру

i = 1
keyboard_message = types.InlineKeyboardMarkup(row_width = 4) # объявление клавиатуры в сообщении
for key, value in data_c.items():
    # Currency = types.InlineKeyboardButton(text=key, callback_data=key)
    globals()['x' + str(i)] = types.InlineKeyboardButton(text=key, callback_data=key)
    i += 1
    if (i == 24): #Самый большой КОСТЫЛЬ в мире
        keyboard_message.add(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет {0.first_name}! \nЯ, {1.first_name} - бот способный выводить курс BTC по отношению к выбранной валюте.\n Для получения инструкции введи /help или нажми на кнопку 'Помощь', расположенной под строкой ввода сообщения".format(message.from_user, bot.get_me()), reply_markup=keyboard_txt)

@bot.message_handler(commands=['help'])
def help_message(message):
    # bot.send_message(message.chat.id, "Как мной пользоваться?\n Есть два варианта:\n 1.\tТы можешь нажать на кнопку 'Курс BTC', я отошлю тебе сообщение с префиксами валют, выбери один из префиксов и я отправлю тебе курс.\n 2.\tЧерез команды. Для начала установи валюту с помощью команды /SetCurrency далее выведи информацию о ней, с помощью команды /GetStat")
    bot.send_message(message.chat.id, "Как мной пользоваться?\n 1.\tНажми на кнопку «Курс BTC», расположенную под строкой ввода сообщения\n\t2. Выбери один из префиксов, которые я тебе отправил\n\t3. Получи актуальный курс")

@bot.message_handler(content_types=['text'])
def send_messages(message):
    if message.text == 'Курс BTC':
        bot.send_message(message.from_user.id, text="Выбери префикс валюты", reply_markup=keyboard_message)

    elif message.text == 'Помощь':
        help_message(message)

    elif message.text.lower() == "help":
        help_message(message)

    elif message.text.lower() == "start":
        start_message(message)

    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")

@bot.callback_query_handler(func=lambda call: True) # декоратор для обработки выбранного пункта меню в сообщении
def callback_worker(call):
    n = str(call.data)
    temp_ = 0 # Переменная для проверки изменения курса
    for key, value in data_c[n].items():
        if key == 'buy':
            temp_ = value

    while True:
        for key, value in data_c[n].items():
            if key == 'buy':
                _txt = str(value)
                if (temp_ != value): 
                    bot.send_message(call.message.chat.id, text= str("Курс изменился! Теперь:\n"+"1 BTC = "+ _txt + "\t" + n) )
                    temp_ = value
                else:
                    bot.send_message(call.message.chat.id, text= str("1 BTC = "+ _txt + "\t" + n) )
                    temp_ = value
        
        time.sleep(300)

bot.polling(none_stop=True, interval=0)
