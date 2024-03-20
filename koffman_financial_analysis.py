#! python
# -*- coding: utf-8 -*-
import argparse
from leumi_bank_parser import parse_bank_file
from max_visa_parser import parse_visa_max_file
from expenses_processor import ExpenseAnalysis
from dashboard import ExpenseDashboard



def main():
    parser = argparse.ArgumentParser(description='Summarize bank and Visa expendatures for the Koffman household')
    parser.add_argument('-b', '--bank', help='bank files', required=False )
    parser.add_argument('-v', '--visa_max', help='Visa MAX file', required=False)



    args = parser.parse_args()
    print(args)
    visa_max_file = vars(args)["visa_max"]
    bank_file = vars(args)["bank"]

    visa_max_expenses = []
    bank_expenses = []
    if visa_max_file:
        visa_max_expenses += parse_visa_max_file(visa_max_file)   
    if bank_file:
        bank_expenses += parse_bank_file(bank_file)
    
    expense_analysis = ExpenseAnalysis(bank_expenses, visa_max_expenses)
    expense_dashboard = ExpenseDashboard(expense_analysis)
    expense_dashboard.run()


if __name__ == '__main__':
    main()


