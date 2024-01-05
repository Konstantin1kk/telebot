from telebot import TeleBot, types
from extencions import TOKEN, currencies, APIException, API


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: types.Message):
    msg_info = 'Мы хотим узнать от вас: \n<имя валюты, цену которой вы хотите узнать> \n<имя валюты,\
 в которой надо узнать цену первой валюты> <количество первой валюты>.\n!Всё вводится в одну строчку через пробел!'
    bot.send_message(message.chat.id, msg_info)


@bot.message_handler(commands=['values'])
def values(message: types.Message):
    msg_info = 'Доступные валюты:'
    currencies_list = [*currencies.keys()]
    for i in currencies_list:
        msg_info += f'\n{i}'
    bot.send_message(message.chat.id, msg_info)


@bot.message_handler(content_types=['text'])
def convert(message: types.Message):
    try:
        values_text = message.text.split(' ')

        if len(values_text) != 3:
            raise APIException(f'Неверное количество параметров ({len(values_text)})')

        base, quote, amount = values_text
        total, amount = API().get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {base} в {quote} = {total * amount}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
