
from xlrd  import open_workbook  
from expenses import BankExpense  
from categories import get_category
from datetime import datetime


def parse_bank_file(filename):
    wb = open_workbook(filename)
    
    items = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        for row in range(1, number_of_rows):
            in_cell_date = int(sheet.cell(row, 0).value)
            parsedDate = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + in_cell_date - 2)
            company = sheet.cell(row, 1).value
            category = get_category(company)
            in_file_expense = sheet.cell(row, 3).value
            if not in_file_expense:
                continue
            expense = float(in_file_expense)
            item = BankExpense(parsedDate, company,category, expense)
            items.append(item)
        
        return items

