from categories import Categories


def build_full_mappings(expenses, debug, month_input):
    grouped_expenses = {}
    for month in range(1, 13):
        grouped_expenses[month] = {}
        for category in Categories:
            grouped_expenses[month][category] = [[], 0]
    for expense in expenses:
        if debug or expense.category == Categories.OTHERS:
            if not month_input or int(month_input) == expense.date.month:
                print(expense)
        month_map = grouped_expenses[expense.date.month]
        month_map[expense.category][0].append(expense)
    for month, cat_mapping in grouped_expenses.items():
        for cat, expenses_list in cat_mapping.items():
            sum_of_cat = sum([x.expense for x in expenses_list[0]])
            expenses_list[1] = sum_of_cat

    return grouped_expenses
