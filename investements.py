import json
from currency import CoinType
import pandas as pd
from financial_projector import FinancialProjector




class Investement:
    def __init__(self, name: str,
                url: str,
                amount: float,
                currency: str,
                last_update_date: str,
                initial_investement: float,
                initial_investement_currency: str,
                provided_anual_interest_rate: float, 
                itd_date: str):
        self.name = name
        self.url = url
        self.amount = amount
        self.coin_type = CoinType.get_coin_from_name(currency)
        self.normalized_amount = CoinType.normalize_sum(self.amount, self.coin_type)
        self.last_update_date = last_update_date
        self.initial_investment = initial_investement
        self.initial_investment_currency = CoinType.get_coin_from_name(initial_investement_currency)
        self.normalized_initial_investment = CoinType.normalize_sum(self.initial_investment, self.initial_investment_currency)
        self.provided_annual_interest_rate = provided_anual_interest_rate
        self.itd_date = itd_date
        



def get_investement_list(invesement_json_file: str) -> list[Investement]:
    with open(invesement_json_file, 'r') as file:
        investments_data = json.load(file)
    return [Investement(**data) for data in investments_data.get('investements')]
    

class InvestementProcessor:

    def __init__(self, investements: list[Investement]):
        self.investements = investements
        

    def get_investements_df(self) -> pd.DataFrame:
        investements = self.investements
        investements_dict = {
            "name": [investement.name for investement in investements],
            "url": [investement.url for investement in investements],
            "amount": [investement.amount for investement in investements],
            "currency": [investement.coin_type.name for investement in investements],
            "last_update_date": [investement.last_update_date for investement in investements],
            "initial_investment": [investement.initial_investment for investement in investements],
            "initial_investment_currency": [investement.initial_investment_currency.name for investement in investements],
            "provided_annual_interest_rate": [investement.provided_annual_interest_rate for investement in investements],
            "itd_date": [investement.itd_date for investement in investements],
            "calculated_historical_annual_interest_rate": [
                FinancialProjector.calculate_projected_historical_annual_interest_rate(investement) for investement in investements
            ],
        }
        return pd.DataFrame(investements_dict)
