#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xlrd  import open_workbook  
from transactions import IsracardTransaction  
from categories import get_category
from dateutil.parser import parse
import os

def parse_isracard_dir(isracard_dir):
    transactions = []
    for filename in os.listdir(isracard_dir):
        if filename.endswith(".xls"):
            transactions += parse_isracard_file(os.path.join(isracard_dir, filename))
    return transactions



def parse_isracard_file(filename):
    wb = open_workbook(filename)
    
    items = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        for row in range(6, number_of_rows - 1):
            date_string = sheet.cell(row, 0).value
            parsedDate = parse(date_string, dayfirst=True)  
            company = sheet.cell(row, 1).value
            category = get_category(company)
            in_file_expense = sheet.cell(row, 4).value
            
            if not in_file_expense:
                expense = 0
            else:
                expense = float(in_file_expense)
            item = IsracardTransaction(parsedDate, company,category, expense)
            items.append(item)
        
        return items



