import requests
import json
from config import TOKEN


class APIException(Exception):
    def __init__(self, message):
        self.message = message


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException('Нельзя конвертировать валюту саму в себя.')

        try:
            base = base.upper()
            quote = quote.upper()
            amount = float(amount)
        except ValueError:
            raise APIException('Некорректно введено число.')

        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}')
        data = json.loads(response.text)

        if 'error' in data:
            raise APIException(f'Не удалось получить курс валюты {base}.')

        conversion_rate = data['rates'].get(quote)

        if conversion_rate is None:
            raise APIException(f'Не удалось получить курс валюты {quote}.')

        result = amount * conversion_rate
        return result


class TelegramBot:
    def __init__(self):
        self.token = TOKEN
        self.api_url = f'https://api.telegram.org/bot{self.token}'

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(f'{self.api_url}/sendMessage', json=params)
        return response.json()

    def process_message(self, message):
        chat_id = message['chat']['id']
        text = message['text']

        if text.startswith('/start') or text.startswith('/help'):
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
            self.send_message(chat_id, instructions)

        elif text.startswith('/values'):
            available_currencies = (
                'Доступные валюты:\n'
                'USD - Доллар США\n'
                'EUR - Евро\n'
                'RUB - Российский рубль'
            )
            self.send_message(chat_id, available_currencies)

        else:
            try:
                base, quote, amount = text.split()
                result = CurrencyConverter.get