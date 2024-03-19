from categories import Categories
from expenses import BankExpense, Expense,VisaExpense
from csv_output import save_to_csv
from database import save_to_database
from typing import List
import pandas as pd



class ExpenseAnalysis:
    def __init__(self, bank_expenses: List[BankExpense], visa_expenses: List[VisaExpense]):
        bank_expenses_df = pd.DataFrame([vars(exp) for exp in bank_expenses])
        visa_expenses_df = pd.DataFrame([vars(exp) for exp in visa_expenses])
        self.expenses = pd.concat([bank_expenses_df, visa_expenses_df])
        self.expenses['date'] = pd.to_datetime(self.expenses['date'])
        self.expenses['category'] = self.expenses['category'].apply(lambda x: x.name if isinstance(x, Categories) else None)
        self.expenses.set_index('date', inplace=True)

    def monthly_expenses_by_category(self) -> pd.DataFrame:
        return self.expenses.groupby([pd.Grouper(freq='ME'), 'category'])['expense'].sum()

    def category_month_by_month(self, category: Categories) -> pd.Series:
        return self.expenses[self.expenses['category'] == category].groupby(pd.Grouper(freq='ME'))['expense'].sum()

    def yearly_expenses_by_category(self) -> pd.DataFrame:
        return self.expenses.groupby([pd.Grouper(freq='YE'), 'category'])['expense'].sum()
        



def process_expenses(visa_max_expenses: Expense, bank_expenses: Expense, debug : bool, month_input: int, output_file: str, save_to_db: bool) -> None:
    full_mappings = build_full_mappings(bank_expenses+visa_max_expenses, debug, month_input)
    if save_to_db:
        save_to_database(full_mappings)
    if output_file:
        save_to_csv(full_mappings, output_file)

def build_full_mappings(expenses: Expense, debug : bool, month_input: int) -> dict:
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
