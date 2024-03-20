#! python
# -*- coding: utf-8 -*-
import argparse
from investements import  InvestementProcessor, get_investement_list
from leumi_bank_parser import parse_bank_file
from max_visa_parser import parse_visa_max_file
from expenses_processor import TransactionsAnalysis
from dashboard import Dashboard



def main():
    parser = argparse.ArgumentParser(description='Summarize bank and Visa expendatures for the Koffman household')
    parser.add_argument('-b', '--bank', help='bank files', required=False )
    parser.add_argument('-v', '--visa_max', help='Visa MAX file', required=False)
    parser.add_argument('-i', '--investements', help='Investements file', required=False)




    args = parser.parse_args()
    print(args)
    visa_max_file = vars(args)["visa_max"]
    bank_file = vars(args)["bank"]
    investements_file = vars(args)["investements"]

    visa_max_transactions = []
    bank_transactions = []
    if visa_max_file:
        visa_max_transactions += parse_visa_max_file(visa_max_file)   
    if bank_file:
        bank_transactions += parse_bank_file(bank_file)
    
    transaction_analysis = TransactionsAnalysis(bank_transactions, visa_max_transactions)
    investements_list = get_investement_list(investements_file)
    ip = InvestementProcessor(investements_list)

    dashboard = Dashboard(transaction_analysis, ip)
    dashboard.run()


if __name__ == '__main__':
    main()


