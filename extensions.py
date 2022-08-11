import requests
import json
from config import keys

class APIExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIExeption('Валюты для перевода одинаковые')

        try:
            inp_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не опознана валюта {quote}')

        try:
            out_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не опознана валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption('Проблема с количеством валюты')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={inp_ticker}&tsyms={out_ticker}')
        total = json.loads(r.content)[keys[base]]

        return total