#!/usr/bin/env python3
import csv
from itertools import groupby
from operator import itemgetter

#main function
def main():
    company_to_category = {}
    #read company_to_category.csv to csv object
    with open("company_to_category.csv", "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            company_to_category[row[0]] = row[1]
    # create a map of companies per category using python zip
   # Sort the dictionary items by category
    sorted_items = sorted(company_to_category.items(), key=itemgetter(1))
    # Use groupby to group companies by category
    grouped_dict = {k: [item[0] for item in v] for k, v in groupby(sorted_items, key=itemgetter(1))}
    
    #save to a temp file in python format (so I can paste later) 
    with open("company_per_category.txt", "w") as f:
        f.write(str(grouped_dict))

        
    










if __name__ == "__main__":
    main()

