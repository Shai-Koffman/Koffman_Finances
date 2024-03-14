import datetime

from currency import CoinType
from categories import Categories
from builtins import NotImplementedError
class Expense(object):
    def __init__(self):
        pass

    def get_category(self) -> Categories:
        raise NotImplementedError("This method should be implemented in a subclass")
    
    def get_transaction_date(self) -> datetime.datetime:
        raise NotImplementedError("This method should be implemented in a subclass")
    
    def get_expense_sum(self) -> int:
        raise NotImplementedError("This method should be implemented in a subclass")
        
class BankExpense(Expense):
    def __init__(self, date: datetime.datetime, company: str, expense: float):
        self.date = date
        self.company = company
        self.expense = expense
        self.category = self.get_category(company)
    
    def __str__(self):
        return ("Bank Expense:\n"
                "  date = {0}\n"
                "  month = {1}\n"
                "  company = {2}\n"
                "  expense = {3}\n"
                "  category = {4}\n"
                .format(self.date, self.date.month, self.company, self.expense, self.category)) 
    
    def get_category(self, company: str) -> Categories:
        return self.category
    def get_transaction_date(self) -> datetime.datetime:
        return self.date
    def get_expense_sum(self) -> int:
        return self.expense



class VisaExpense(Expense):
    
    def __init__(self, sheet_title: str, company: str, known_category: Categories, visa_max_category: str, visa_card_number: str, expense_sum: int, coin: CoinType, expense_date: datetime.datetime):
        self.sheet_title = sheet_title
        self.company = company
        self.known_category = known_category
        self.visa_max_category = visa_max_category
        self.visa_card_number = visa_card_number
        self.expense_sum = expense_sum
        self.coin = coin
        self.expense_date = expense_date
        self.normalized_expense_sum = CoinType.normalize_expense_sum(self.expense_sum, self.coin)

    
    def __str__(self):
        return ("Visa Expense:\n"
                "  sheet_title = {0}\n"
                "  company = {1}\n"
                "  visa_max_category = {2}\n"
                "  visa_card_number = {3}\n"
                "  expense_sum = {4}\n"
                "  coin_type = {5}\n"
                "  expense_date = {6}\n"
                "  normalized_expense_sum = {7}\n"
                .format(self.sheet_title, self.company, self.visa_max_category, self.visa_card_number, self.expense_sum, self.coin.name, self.expense_date, self.normalized_expense_sum))
    
    def get_category(self) -> Categories:
        return self.known_category
    
    def get_transaction_date(self) -> datetime.datetime:
        return self.expense_date
    
    def get_expense_sum(self) -> int:
        return self.normalized_expense_sum


