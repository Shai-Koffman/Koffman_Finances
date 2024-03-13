from categories import Categories
import csv

def save_to_csv(grouped_expenses, month_input, output_file):
    fieldnames = ['Month'] + Categories._member_names_
    with open(output_file, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print(f"fieldnames: {fieldnames}")
        print(f"writer: {writer}")
        print(f"csv file: {csvfile}")
        writer.writeheader()
        for month, cat_mapping in grouped_expenses.items():
            if not month_input or int(month_input) == month:
                row_dict = {"Month": month}
                for cat, expenses_tuple in cat_mapping.items():
                    row_dict[cat] = expenses_tuple[1]
                writer.writerow(row_dict)
