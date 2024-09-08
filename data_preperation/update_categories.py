import os
import sys
import yaml
import re

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from categories import Categories

def is_hebrew(text):
    return any("\u0590" <= char <= "\u05FF" for char in text)

def display_text(text):
    if is_hebrew(text):
        return text[::-1]
    return text

def get_user_category_choice():
    print("Choose a category by entering its number:")
    for i, category in enumerate(Categories):
        print(f"{i + 1}. {category.name}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(Categories):
                return list(Categories)[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def update_categories_yaml(category, company):
    yaml_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "categories.yaml")
    
    with open(yaml_file, 'r', encoding='utf-8') as f:
        categories_data = yaml.safe_load(f)
    
    if category.name not in categories_data:
        categories_data[category.name] = []
    
    if company not in categories_data[category.name]:
        categories_data[category.name].append(company)
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(categories_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"Added {display_text(company)} to {category.name}")
    else:
        print(f"{display_text(company)} already exists in {category.name}")

def company_exists_in_categories(company, categories_data):
    return any(company in category_items for category_items in categories_data.values())

def main():
    unknown_companies_file = os.path.join(os.path.dirname(__file__), ".unknown_companies.txt")
    yaml_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "categories.yaml")
    
    if not os.path.exists(unknown_companies_file):
        print(f"File {unknown_companies_file} not found.")
        return

    with open(yaml_file, 'r', encoding='utf-8') as f:
        categories_data = yaml.safe_load(f)

    with open(unknown_companies_file, "r", encoding='utf-8') as f:
        companies = f.read().splitlines()

    for company in companies:
        if not company_exists_in_categories(company, categories_data):
            print(f"\nProcessing company: {display_text(company)}")
            category = get_user_category_choice()
            
            update_choice = input(f"Do you want to update the categories file with {display_text(company)} in {category.name}? (y/n): ").lower()
            if update_choice == 'y':
                update_categories_yaml(category, company)
            else:
                print("Skipped updating categories.yaml")
        else:
            print(f"Skipping {display_text(company)} as it already exists in a category")

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()