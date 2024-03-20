from categories import Categories
from transactions import BankTransaction,VisaMaxTransaction,Transaction
from typing import List,Tuple
from enum import Enum, auto
import pandas as pd

class AccountType(Enum):
    BANK = auto()
    VISA_MAX = auto()

class ExpenseAnalysis:
    def __init__(self, bank_transactions: List[BankTransaction], visa_transactions: List[VisaMaxTransaction]):
        columns = ['date', 'category', 'expense', 'gains']
        # For bank expenses
        self.detailed_bank_transactions = bank_transactions
        self.detailed_visa_max_transactions = visa_transactions
        self.bank_transactions_pd = pd.DataFrame([(exp.get_transaction_date(),
                                               exp.get_category(),
                                               exp.get_expense_sum(),
                                               exp.get_gains_sum()) for exp in bank_transactions], columns=columns)
        # For visa max expenses
        self.visa_max_transactions_pd = pd.DataFrame([(exp.get_transaction_date(),
                                               exp.get_category(),
                                               exp.get_expense_sum(),
                                               exp.get_gains_sum()) for exp in visa_transactions], columns=columns)
        
        
        
        # Also convert 'date' column to datetime for bank_expenses_pd and visa_expenses_pd, and set as index
        self.bank_transactions_pd['date'] = pd.to_datetime(self.bank_transactions_pd['date'])
        self.bank_transactions_pd.set_index('date', inplace=True)
        self.visa_max_transactions_pd['date'] = pd.to_datetime(self.visa_max_transactions_pd['date'])
        self.visa_max_transactions_pd.set_index('date', inplace=True)

        

    def bank_monthly_expenses(self, year: int, month: int) -> pd.Series:
        bank_dates = self.bank_transactions_pd.index
        filtered_expenses = self.bank_transactions_pd[(bank_dates.year == year) & (bank_dates.month == month)]
        return filtered_expenses.groupby('category')['expense'].sum()
    
    def bank_monthly_gains(self, year: int, month: int) -> pd.Series:
        bank_dates = self.bank_transactions_pd.index
        filtered_gains = self.bank_transactions_pd[(bank_dates.year == year) & (bank_dates.month == month)]
        return filtered_gains.groupby('category')['gains'].sum()


    def visa_max_monthly_gains(self, year: int, month: int) -> pd.Series:
        visa_dates = self.visa_max_transactions_pd.index
        filtered_gains = self.visa_max_transactions_pd[(visa_dates.year == year) & (visa_dates.month == month)]
        return filtered_gains.groupby('category')['gains'].sum()
    
    def visa_max_monthly_expenses(self, year: int, month: int) -> pd.Series:
        visa_dates = self.visa_max_transactions_pd.index
        filtered_expenses = self.visa_max_transactions_pd[(visa_dates.year == year) & (visa_dates.month == month)]
        return filtered_expenses.groupby('category')['expense'].sum()


    #returns a tuple of DataFrame lists, one for bank gains total per month and one for bank expenses total per month.
    def bank_total_gains_and_expenses_per_month(self, exclude_transfers: bool) ->Tuple[pd.Series, pd.Series]:
        bank_transactions = self.bank_transactions_pd.copy()
        if exclude_transfers:
            bank_transactions = bank_transactions[bank_transactions['category'] != Categories.BANK_TRANSFERS_AND_MONEY_TRANSFERS]

        
        gains_per_month = bank_transactions.groupby(pd.Grouper(freq='ME'))['gains'].sum()
        expenses_per_month = bank_transactions.groupby(pd.Grouper(freq='ME'))['expense'].sum()
            

        # Create a common date range for both gains and expenses
        all_dates = gains_per_month.index.union(expenses_per_month.index)
        # Reindex gains and expenses to the common date range and fill missing values with 0
        gains_per_month = gains_per_month.reindex(all_dates, fill_value=0)
        expenses_per_month = expenses_per_month.reindex(all_dates, fill_value=0)
        return gains_per_month, expenses_per_month
        
    def get_categories(self) -> List[str]:
        # Combine categories from both bank and visa transactions, then remove duplicates
        bank_categories = self.bank_transactions_pd['category'].unique().tolist()
        visa_max_categories = self.visa_max_transactions_pd['category'].unique().tolist()
        all_categories = list(set(bank_categories + visa_max_categories))
        all_categories.sort()  # Optional: sort the categories alphabetically
        return all_categories

    def get_monthly_expenses_and_gains_by_category(self, category: str, account_type: AccountType) -> Tuple[pd.DataFrame, pd.DataFrame]:
        transactions = pd.DataFrame()  # Initialize to an empty DataFrame to handle unexpected account_type values
        if account_type == AccountType.BANK:
            transactions = self.bank_transactions_pd[self.bank_transactions_pd['category'] == category]
        elif account_type == AccountType.VISA_MAX:
            transactions = self.visa_max_transactions_pd[self.visa_max_transactions_pd['category'] == category]
     
        # Group by month and calculate total expenses and gains
        expenses_per_month = transactions.groupby(pd.Grouper(freq='ME'))['expense'].sum()
        gains_per_month = transactions.groupby(pd.Grouper(freq='ME'))['gains'].sum()

        # Create a common date range for both gains and expenses
        all_dates = expenses_per_month.index.union(gains_per_month.index)
        # Reindex gains and expenses to the common date range and fill missing values with 0
        expenses_per_month = expenses_per_month.reindex(all_dates, fill_value=0)
        gains_per_month = gains_per_month.reindex(all_dates, fill_value=0)

        return expenses_per_month, gains_per_month

    def get_detailed_expenses(self, account_type: AccountType, year: int, month: int, category: str) -> List[Transaction]:
        if account_type == AccountType.BANK:
            return [transaction for transaction in self.detailed_bank_transactions if transaction.get_transaction_date().year == year and transaction.get_transaction_date().month == month and transaction.get_category() == category]
        elif account_type == AccountType.VISA_MAX:
            return [transaction for transaction in self.detailed_visa_max_transactions if transaction.get_transaction_date().year == year and transaction.get_transaction_date().month == month and transaction.get_category() == category]
