
from math import exp
from xlrd  import open_workbook  
from transactions import BankTransaction  
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
            in_file_gains = sheet.cell(row, 4).value
            if not in_file_expense:
                expense = 0
            else:
                expense = float(in_file_expense)
            if not in_file_gains:
                gains = 0
            else:
                gains = float(in_file_gains)    
            item = BankTransaction(parsedDate, company,category, expense, gains)
            items.append(item)
        
        return items

