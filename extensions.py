import json                                 # Модуль json для преобразования json-данных в словарь.
import requests                             # Модуль requests для отправки запросов по url.
from config import exchanges                # Импорт из собственного файла 'config' с константами.


class APIException(Exception):
    '''
    Класс собственных исключений. Наследует атрибуты и методы базового класса.
    '''
    pass

class Convertor:
    '''
    Класс для проверки данных от пользователя и перевода валюты.
    Возвращает словарь, полученный в результате обработки данных json от get запроса.
    '''
    @staticmethod
    def get_price(quote : str, base : str, amount : str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            base_ticker = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_ticker = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        resp = json.loads(r.content)[exchanges[base]]
        return resp
