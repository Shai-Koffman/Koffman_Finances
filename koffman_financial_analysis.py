#! python
# -*- coding: utf-8 -*-
import argparse
from csv_output import save_to_csv
from leumi_bank_parser import parse_bank_file
from max_visa_parser import parse_visa_max_file
from grouping import build_full_mappings
from database import save_to_database



def main():
    parser = argparse.ArgumentParser(description='Summarize bank and Visa expendatures for the Koffman household')
    parser.add_argument('-b', '--bank', help='bank files', required=False )
    parser.add_argument('-v', '--visa_max', help='Visa MAX file', required=False)
    parser.add_argument('-o', '--output', help='output csv', required=False)
    parser.add_argument('-m', '--month', help='month to summarize', required=False)
    parser.add_argument('-d', '--debug', help='write all expenses', required=False)
    parser.add_argument('-s', '--save_to_db', help='save expenses to database', action='store_true')

    args = parser.parse_args()
    print(args)
    debug = bool(vars(args)["debug"])
    month_input = vars(args)["month"]
    save_to_db = vars(args)["save_to_db"]
    output_file = vars(args)["output"]
    visa_max_file = vars(args)["visa_max"]
    bank_file = vars(args)["bank"]

    expenses = []
    if visa_max_file:
        expenses += parse_visa_max_file(visa_max_file)   
    if bank_file:
        expenses += parse_bank_file(bank_file)
    
    grouped_expenses = build_full_mappings(expenses, debug, month_input)

    if save_to_db:
        save_to_database(grouped_expenses)
    if output_file:
        save_to_csv(grouped_expenses, month_input, output_file)
    if debug:
        for month, cat_mapping in grouped_expenses.items():
            if not month_input or int(month_input) == month:
                print("--------------------------Month %s----------------------------" % (month))
                for cat, expenses_tuple in cat_mapping.items():
                    print("total expense of category %s is %d " % (cat, expenses_tuple[1]))


if __name__ == '__main__':
    main()


