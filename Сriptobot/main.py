import telebot
from extensions import CurrencyConverter, APIException
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = (
        'Привет! Я бот для конвертации валют.\n'
        'Чтобы узнать цену на определенное количество валюты, '
        'отправьте мне сообщение в следующем формате:\n'
        '<имя валюты, цену которой вы хотите узнать> '
        '<имя валюты, в которой надо узнать цену первой валюты> '
        '<количество первой валюты>\n\n'
        'Например:\n'
        'USD RUB 100\n'
        'EUR USD 50\n\n'
        'Для получения списка доступных валют введите команду /values.'
    )
    bot.send_message(message.chat.id, instructions)


@bot.message_handler(commands=['values'])
def handle_values(message):
    available_currencies = (
        'Доступные валюты:\n'
        'USD - Доллар США\n'
        'EUR - Евро\n'
        'RUB - Российский рубль'
    )
    bot.send_message(message.chat.id, available_currencies)


@bot.message_handler(func=lambda message: True)
def handle_conversion(message):
    try:
        base, quote, amount = message.text.split()
        result = CurrencyConverter.get_price(base, quote, amount)
        response = f'{amount} {base} = {result} {quote}'
    except APIException as e:
        response = f'Ошибка: {type(e).__name__} - {e.message}'
    except Exception:
        response = 'Произошла ошибка при обработке запроса.'

    bot.send_message(message.chat.id, response)


if __name__ == '__main__':
    bot.polling()