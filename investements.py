import json
from currency import CoinType
import pandas as pd



class Investement:
    def __init__(self, name: str, url: str, amount: float, currency: str, last_update_date: str, itd: float, itd_date: str):
        self.name = name
        self.url = url
        self.amount = amount
        self.coin_type = CoinType.get_coin_from_name(currency)
        self.normalized_amount = CoinType.normalize_sum(self.amount, self.coin_type)
        self.last_update_date = last_update_date
        self.itd = itd
        self.itd_date = itd_date




def get_investement_list(invesement_json_file: str) -> list[Investement]:
    inv_list = []
    with open(invesement_json_file, 'r') as file:
        investments_data = json.load(file)
    return [Investement(**data) for data in investments_data.get('investements')]
    

class InvestementProcessor:

    def __init__(self, investements: list[Investement]):
        self.investements = investements

    def get_investements_series(self) -> pd.Series:
        investements = self.investements
        investements_dict = {
            "name": [investement.name for investement in investements],
            "url": [investement.url for investement in investements],
            "amount": [investement.amount for investement in investements],
            "currency": [investement.coin_type.name for investement in investements],
            "last_update_date": [investement.last_update_date for investement in investements],
            "itd": [investement.itd for investement in investements],
            "itd_date": [investement.itd_date for investement in investements],
        }
        return pd.DataFrame(investements_dict)


