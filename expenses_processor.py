from categories import Categories
from expenses import BankTransaction, Transaction,VisaTransaction
from csv_output import save_to_csv
from database import save_to_database
from typing import List,Tuple
import pandas as pd



class ExpenseAnalysis:
    def __init__(self, bank_expenses: List[BankTransaction], visa_expenses: List[VisaTransaction]):
        columns = ['date', 'category', 'expense', 'gains']
        # For bank expenses
        self.bank_expenses_pd = pd.DataFrame([(exp.get_transaction_date(),
                                               exp.get_category(),
                                               exp.get_expense_sum(),
                                               exp.get_gains_sum()) for exp in bank_expenses], columns=columns)
        # For visa expenses
        self.visa_expenses_pd = pd.DataFrame([(exp.get_transaction_date(),
                                               exp.get_category(),
                                               exp.get_expense_sum(),
                                               exp.get_gains_sum()) for exp in visa_expenses], columns=columns)
        
     
        
        # Also convert 'date' column to datetime for bank_expenses_pd and visa_expenses_pd, and set as index
        self.bank_expenses_pd['date'] = pd.to_datetime(self.bank_expenses_pd['date'])
        self.bank_expenses_pd.set_index('date', inplace=True)
        self.visa_expenses_pd['date'] = pd.to_datetime(self.visa_expenses_pd['date'])
        self.visa_expenses_pd.set_index('date', inplace=True)

    def bank_monthly_expenses(self, year: int, month: int) -> pd.Series:
        bank_dates = self.bank_expenses_pd.index
        filtered_expenses = self.bank_expenses_pd[(bank_dates.year == year) & (bank_dates.month == month)]
        return filtered_expenses.groupby('category')['expense'].sum()
    
    def bank_monthly_gains(self, year: int, month: int) -> pd.Series:
        bank_dates = self.bank_expenses_pd.index
        filtered_gains = self.bank_expenses_pd[(bank_dates.year == year) & (bank_dates.month == month)]
        return filtered_gains.groupby('category')['gains'].sum()


    def visa_monthly_gains(self, year: int, month: int) -> pd.Series:
        visa_dates = self.visa_expenses_pd.index
        filtered_gains = self.visa_expenses_pd[(visa_dates.year == year) & (visa_dates.month == month)]
        return filtered_gains.groupby('category')['gains'].sum()
    
    def visa_monthly_expenses(self, year: int, month: int) -> pd.Series:
        visa_dates = self.visa_expenses_pd.index
        filtered_expenses = self.visa_expenses_pd[(visa_dates.year == year) & (visa_dates.month == month)]
        return filtered_expenses.groupby('category')['expense'].sum()


    #returns a tuple of DataFrame lists, one for bank gains total per month and one for bank expenses total per month.
    def bank_total_gains_and_expenses_per_month(self) ->Tuple[pd.Series, pd.Series]:
        bank_expenses = self.bank_expenses_pd.copy()
        
        gains_per_month = bank_expenses.groupby(pd.Grouper(freq='ME'))['gains'].sum()
        expenses_per_month = bank_expenses.groupby(pd.Grouper(freq='ME'))['expense'].sum()
        # Create a common date range for both gains and expenses
        all_dates = gains_per_month.index.union(expenses_per_month.index)
        # Reindex gains and expenses to the common date range and fill missing values with 0
        gains_per_month = gains_per_month.reindex(all_dates, fill_value=0)
        expenses_per_month = expenses_per_month.reindex(all_dates, fill_value=0)
        return gains_per_month, expenses_per_month
        
    


def process_expenses(visa_max_expenses: Transaction, bank_expenses: Transaction, debug : bool, month_input: int, output_file: str, save_to_db: bool) -> None:
    full_mappings = build_full_mappings(bank_expenses+visa_max_expenses, debug, month_input)
    if save_to_db:
        save_to_database(full_mappings)
    if output_file:
        save_to_csv(full_mappings, output_file)

def build_full_mappings(expenses: Transaction, debug : bool, month_input: int) -> dict:
    grouped_expenses = {}
    for month in range(1, 13):
        grouped_expenses[month] = {}
        for category in Categories:
            grouped_expenses[month][category] = [[], 0]
    for expense in expenses:
        if debug or expense.get_category() == Categories.UNKNOWN:
            if not month_input or int(month_input) == expense.date.month:
                print(expense)
        month_map = grouped_expenses[expense.get_transaction_date().month]
        month_map[expense.get_category()][0].append(expense)
    for month, cat_mapping in grouped_expenses.items():
        for cat, expenses_list in cat_mapping.items():
            sum_of_cat = sum([x.get_expense_sum() for x in expenses_list[0]])
            expenses_list[1] = sum_of_cat

    return grouped_expenses
