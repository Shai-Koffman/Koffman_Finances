from categories import Categories
from expenses import Expense



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
