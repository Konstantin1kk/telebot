import requests
import json

TOKEN = '6377040747:AAHczbNxE88INENvuzQOBAWfYY8x8vxR5Wg'
APP_ID = 'c5b09901fc5a2a91672002cc'


currencies = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
    'стерлинг': 'GBP',
}


class APIException(Exception):
    pass


class API:
    @staticmethod
    def get_price(base: str, quote: str, amount: int):
        if base == quote:
            raise APIException(f'Одинаковые валюты {base}')

        try:
            value_ticket = float(amount)
        except ValueError:
            raise APIException('Неверное количество валюты')

        try:
            base_ticket = currencies[base]
        except KeyError:
            raise APIException(f'Неверная валюта {base}')

        try:
            quote_ticket = currencies[quote]
        except KeyError:
            raise APIException(f'Неверная валюта {quote}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{APP_ID}/latest/{base_ticket}')
        data = json.loads(r.content)['conversion_rates'][quote_ticket]

        return data, value_ticket
