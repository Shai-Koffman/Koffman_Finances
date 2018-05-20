#! python
# -*- coding: utf-8 -*-
import datetime
from xlrd import open_workbook
from dateutil.parser import parse
import argparse
import csv


class Enumeration(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def __setattr__(self, name, value):
        raise RuntimeError("Cannot override values")

    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")


Categories_names = [
    "SUPER",
    "ELECTRICITY",
    "INTERNET_AND_PHONES",
    "OTHER_FOOD",
    "RESTOURANTS_AND_HOTELS",
    "WATER",
    "ARNONA",
    "CAR_INSURANCE",
    "CAR_EXPENSES",
    "HEALTH_INSURANCE",
    "OTHER_INSURANCE",
    "GAS",
    "FUEL",
    "HEALTH_AND_MACABI",
    "SCHOOLS",
    "HUGIM",
    "INVESTMENTS",
    "CASPOMAT",
    "CLOTHING",
    "PRESENTS",
    "AMAZON_AND_GOOGLE",
    "ABROAD_EXPENSES",
    "VISA",
    "CHECKS",
    "MONEY_TRANSFERS",
    "FUN_AND_MOVIES",

    "OTHERS"
]

Categories = Enumeration(Categories_names)


class Expense(object):
    def __init__(self, date, company, expense):
        self.date = date
        self.company = company
        self.expense = expense
        self.category = self.get_category(company)

    def __str__(self):
        return ("Expense object:\n"
                "  date = {0}\n"
                "  month = {1}\n"
                "  company = {2}\n"
                "  expense = {3}\n"
                "  category = {4}\n"
                .format(self.date, self.date.month, self.company, self.expense, self.category))

    def get_category(self, company):
        categorizations = [
            (Categories.SUPER,
             ["םניח", " רפוס", "לסרפוש", "ףוננחוי", "ןתיב תוניי", "MP MA", "MP:MA", "יול ימר", "םעט ביט",
              "תואנועמק הגמ", "הננער קוש"]),
            (Categories.ELECTRICITY, ["למשח"]),
            (Categories.INTERNET_AND_PHONES, ["TOH"]),
            (Categories.OTHER_FOOD,
             ["תייפאמ", "םחל", "ןידלור", "הפאמ", "םימחל", "וסרפסנ", "הטספ הל", "היילק", "זילטיא", "רכיכה תילק",
              "הננער תימע", "וגוט", "HSIF RM"]),
            (Categories.RESTOURANTS_AND_HOTELS,
             ["הניל'גנא", "איצרג", "המלא", "דלישטור", "הדלוג", "והיתתמ", "היישוסה", "יצימ", "הנינמחל", "טרוגוי",
              "הלדנח", "ןשייטסיפוק", "הדנ'גל", "רוודנל", "ףר'יג", "NEHCTIK", "ONON", "םירק ילד", "למרק הפק", "הרבוזוז",
              "הני'צוק", "ALLEB AZZIP", "ןנוג יפונ", "2 בולוקוס"]),
            (Categories.WATER, ["ןורשה דוה ימ", "4 ימת"]),
            (Categories.ARNONA, ["ןורשה דוה תייריע"]),
            (Categories.CAR_INSURANCE, ["סקינפה"]),
            (Categories.CAR_EXPENSES, ["תונוישר", "רטמומניד"]),
            (Categories.HEALTH_INSURANCE, ["לדגמ", "חוטיב-לארה", "חוטיב-GIA"]),
            (Categories.OTHER_INSURANCE, ["תוגספ", "הריד חוטיב הרונמ"]),
            (Categories.GAS, ["זגרפוס"]),
            (Categories.FUEL,
             ["קלד", "ןולא רוד", "ןט", "לונוס", "/זפ", "קלד", "/WOLLEYזפ", "ךרבא הנוי", "סורוטומ טנירפס", "WOLLEY זפ", "הכאלמה טנירפס"]),
            (Categories.HEALTH_AND_MACABI, ["יבכמ", "ינאה עיבר רד", "הילצרה םראפ-רפוס", "הידפוטרופס", "הרואל 'רד"]),
            (Categories.SCHOOLS, ["ךוניח", "ןיטילש ןג", "ןורהצ- םודיקל הרבחה"]),
            (Categories.HUGIM, ["רוד זכרמ", "הכלממה"]),
            (Categories.INVESTMENTS, ["םייח חוטיב - םיחטבמ הרונמ", "תורדתסה"]),
            (Categories.CASPOMAT, ["טמופסכ"]),
            (Categories.CLOTHING,
             ["וגנמ", "והוס", "זיירוססקא", "FLOG", "ורטסק", "סדיק-יימ", "ילענ", "סידוה", "לטילא", "הלדיימ", "יול תירש",
              "וילס", "M&H", "האדיא", "שימ§ שימ", "התלד", "הנפוא תשר טקלס", "טראוד", "סקופ","ץורע יבליב", "םירפרפ", "ירצומ-יקונית", "רב דנא לופ", ]),
            (Categories.PRESENTS, ["םיעושעשה רפכ", "טאריפה", "יוט", "תמוצ", "תונתמה", "ןד הרוא", "יקצמיטס", "םיעוצעצה", "גאב"]),
            (Categories.AMAZON_AND_GOOGLE, ["NOZAMA", "SU LLIB/MOC.NZMA", "ELGOOG", "SU stmp/moc.nzma", "LAPYAP"]),
            (Categories.VISA, ["הזיו ימואל", "י-ב דראק ימואל"]),
            (Categories.CHECKS, ["קיש"]),
            (Categories.MONEY_TRANSFERS, ["007טנרטניא .עה", "696הדקפה/הרבעה"]),
            (Categories.FUN_AND_MOVIES, ["םיקוניפ","המניס" ])
        ]

        for category, matches in categorizations:
            if any(match in company for match in matches):
                return category
        return Categories.OTHERS


def parse_visa_abroad_file(filename):
    wb = open_workbook(filename)
    items = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        rows = []
        for row in range(1, number_of_rows):
            values = []
            date = sheet.cell(row, 0).value
            parsedDate = parse(date, dayfirst=True)
            company = sheet.cell(row, 2).value
            company_correct = company[::-1].encode("utf8")
            expense = float(sheet.cell(row, 6).value)
            item = Expense(parsedDate, company_correct, expense)
            if (item.category == Categories.OTHERS):
                item.category = Categories.ABROAD_EXPENSES
            items.append(item)
        # print "number of items in %s is %d" % (filename, len(items))
        return items


def parse_visa_file(filename):
    wb = open_workbook(filename)
    items = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        rows = []
        for row in range(1, number_of_rows):
            values = []
            date = sheet.cell(row, 0).value
            parsedDate = parse(date, dayfirst=True)
            company = sheet.cell(row, 2).value
            company_correct = company[::-1].encode("utf8")
            expense = float(sheet.cell(row, 6).value)
            item = Expense(parsedDate, company_correct, expense)
            items.append(item)
        # print "number of items in %s is %d" % (filename, len(items))
        return items


def parse_bank_file(filename):
    wb = open_workbook(filename)
    items = []
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols
        rows = []
        for row in range(1, number_of_rows):
            values = []
            parsedDate = datetime.datetime.fromordinal(
                datetime.datetime(1900, 1, 1).toordinal() + int(sheet.cell(row, 0).value) - 2)
            company = sheet.cell(row, 1).value
            company_correct = company[::-1].encode("utf8")
            in_file_expense = sheet.cell(row, 3).value
            if not in_file_expense:
                continue
            expense = float(in_file_expense)
            item = Expense(parsedDate, company_correct, expense)
            items.append(item)
        # print "number of items in %s is %d" % (filename, len(items))
        return items


def build_full_mappings(expenses, debug, month_input):
    grouped_expenses = {}
    for month in xrange(1, 13):
        grouped_expenses[month] = {}
        for category in Categories:
            grouped_expenses[month][category] = [[], 0]
    for expense in expenses:
        if debug or expense.category == Categories.OTHERS:
            if not month_input or int(month_input) == expense.date.month:
                print expense
        month_map = grouped_expenses[expense.date.month]
        month_map[expense.category][0].append(expense)
    for month, cat_mapping in grouped_expenses.iteritems():
        for cat, expenses_list in cat_mapping.iteritems():
            sum_of_cat = sum([x.expense for x in expenses_list[0]])
            expenses_list[1] = sum_of_cat

    return grouped_expenses


def main():
    parser = argparse.ArgumentParser(description='Summarize bank and Visa expendatures for the Koffman household')
    parser.add_argument('-b', '--bank', help='bank files', required=False, )
    parser.add_argument('-v', '--visa', help='Visa files', action='append', default=[], required=False)
    parser.add_argument('-a', '--visa_abroad', help='Visa abroad', action='append', default=[], required=False)
    parser.add_argument('-o', '--output', help='output csv', required=False)
    parser.add_argument('-m', '--month', help='month to summarize', required=False)
    parser.add_argument('-d', '--debug', help='write all expenses', required=False)

    args = parser.parse_args()
    print args
    debug = bool(vars(args)["debug"])
    month_input = vars(args)["month"]

    expenses = []
    for visa_file in vars(args)["visa"]:
        print "====================analyzing %s==================" % (visa_file)
        expenses += parse_visa_file(visa_file)
    for visa_abroad in vars(args)["visa_abroad"]:
        print "====================analyzing %s==================" % (visa_abroad)
        expenses += parse_visa_abroad_file(visa_abroad)
    bank_file = vars(args)["bank"]
    if bank_file:
        print "====================analyzing %s==================" % (bank_file)
        expenses += parse_bank_file(bank_file)
    grouped_expenses = build_full_mappings(expenses, debug, month_input)

    for month, cat_mapping in grouped_expenses.iteritems():
        if not month_input or int(month_input) == month:
            print "--------------------------Month %s----------------------------" % (month)
            for cat, expenses_tuple in cat_mapping.iteritems():
                print "total expense of category %s is %d " % (cat, expenses_tuple[1])

    output_file = vars(args)["output"]
    if output_file:
        csvfile = open(output_file, 'w+')
        fieldnames = ['Month']
        fieldnames += Categories_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print "fieldnames", fieldnames
        print "writer ", writer
        print "csv file ", csvfile
        writer.writeheader()
        for month, cat_mapping in grouped_expenses.iteritems():
            if not month_input or int(month_input) == month:
                row_dict = {"Month": month}
                for cat, expenses_tuple in cat_mapping.iteritems():
                    row_dict[cat] = expenses_tuple[1]
                writer.writerow(row_dict)
        csvfile.close()


if __name__ == '__main__':
    main()
