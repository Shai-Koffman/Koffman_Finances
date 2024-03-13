class Expense(object):
    def __init__(self, date: str, company: str, expense: float):
        self.date = date
        self.company = company
        self.expense = expense
        self.category = self.get_category(company)

    def __str__(self):
        return ("  date = {0}\n"
                "  month = {1}\n"
                "  company = {2}\n"
                "  expense = {3}\n"
                "  category = {4}\n"
                .format(self.date, self.date.month, self.company, self.expense, self.category)) 

class BankExpense(Expense):
    def __init__(self, date: str, company: str, expense: float):
        super().__init__(date, company, expense)
        self.type = "Bank"

    def __str__(self):
        return "Bank Expense:\n" + super().__str__()

class VisaExpense(Expense):
    def __init__(self, date: str, company: str, expense: float):
        super().__init__(date, company, expense)
        self.type = "Visa"

    def __str__(self):
        return super().__str__() + "  type = Visa\n"
