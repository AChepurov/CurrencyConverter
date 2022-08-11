import telebot
from config import keys, TOKEN
from extensions import APIExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите команду в виде: <имя валюты, цену которой надо узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nПосмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIExeption('Что-то в запросе лишнее. Попробуйте еще.')
        if len(values) < 3:
            raise APIExeption('Чего-то не хватает в запросе. Попробуйте еще.')

        quote, base, amount = values
        total = CryptoConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')
    else:
        text = f'В {amount} {quote} содержится {total} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
