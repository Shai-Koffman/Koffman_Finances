#!/usr/bin/env python
# -*- coding: utf-8 -*-

from categories import Categories



def main():
    unknown_companies = []

    #read the .unknown_companies.txt into a list
    with open(".unknown_companies.txt", "r") as f:
        unknown_companies = f.readlines()
    
    #turn the list to a set
    unknown_companies = set(unknown_companies)
    #save to a file unique_unknown_companies.csv, each company in a new line
    with open("unique_unknown_companies.csv", "w") as f:
        for company in unknown_companies:
            f.write(company)

      
   

    


    
   
    


#main
if __name__ == "__main__":
    main()

