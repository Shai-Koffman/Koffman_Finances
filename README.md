# Leumi_financial_analysis
To prepare the data for analysis, follow these steps:

1. **Collect Raw Data**: Get the files from the bank  MAX and Isracard, Remember that Isracard is per month.
    - Bank:
       -  Clean header
       -  Switch sides
       -  Delete column B after switching sides
       -  Save as xls
    - MAX:
       -  Clean headers and footers in all tabs, leave titles in each tab.
       -  Save as xlsx
    - Isracard: 
       - use Dina ID and card 570096 (Need Dinas phone for access number for SMS) 
       - download missing files
       - Remove footer rows from all new files. 
    - Change launch.json to point to the correct paths.

2. **Feed the data**: Feed the data, Make sure to add unknown categories to the categories file (from the unknown_companies.txt)

3. **Investements** - Add the investements to the investements file and update the dates, Follow the links in the existing file.

4. **Look at the data** - Go to the website and introspect the data

