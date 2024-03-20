from currency_converter import CurrencyConverter
from enum import Enum




class CoinType(Enum):
    SHEKEL = CurrencyConverter().convert(1, 'ILS', 'ILS')
    EURO = CurrencyConverter().convert(1, 'EUR', 'ILS')
    DOLLAR = CurrencyConverter().convert(1, 'USD', 'ILS')
    @staticmethod
    def get_coin_from_symbol(symbol: str) -> 'CoinType':
        if symbol == '₪':
            return CoinType.SHEKEL
        elif symbol == '€':
            return CoinType.EURO
        elif symbol == '$':
            return CoinType.DOLLAR
    
    def get_coin_from_name(name: str) -> 'CoinType':
        if name == 'ILS':
            return CoinType.SHEKEL
        elif name == 'EUR':
            return CoinType.EURO
        elif name == 'USD':
            return CoinType.DOLLAR
    
    @staticmethod
    def normalize_sum(sum: int, coin: 'CoinType') -> float:
        return sum * coin.value
