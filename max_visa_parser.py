from dateutil.parser import parse
import openpyxl
from expenses import VisaExpense


def parse_visa_max_file(filename):
    wb = openpyxl.load_workbook(filename)
    items = []
    for sheet in wb.worksheets:
        number_of_rows = sheet.max_row
        for row in range(2, number_of_rows + 1):  # Adjusted to start from row 2 assuming row 1 has headers
            date_cell = sheet.cell(row, 1)  # Assuming date is in the first column
            date = date_cell.value
            parsedDate = parse(date.strftime('%d/%m/%Y'), dayfirst=True)  # Adjusted for openpyxl datetime object
            company_cell = sheet.cell(row, 3)  # Assuming company name is in the third column
            company = company_cell.value
            company_correct = company[::-1].encode("utf8")
            expense_cell = sheet.cell(row, 7)  # Assuming expense is in the seventh column
            expense = float(expense_cell.value)
            item = VisaExpense(parsedDate, company_correct, expense)
            items.append(item)
    return items

