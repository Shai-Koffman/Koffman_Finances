import os
import sys
import yaml

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from categories import Categories

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
        print(f"Added {company} to {category.name}")
    else:
        print(f"{company} already exists in {category.name}")

def main():
    unknown_companies_file = os.path.join(os.path.dirname(__file__), ".unknown_companies.txt")
    
    if not os.path.exists(unknown_companies_file):
        print(f"File {unknown_companies_file} not found.")
        return

    with open(unknown_companies_file, "r", encoding='utf-8') as f:
        companies = f.read().splitlines()

    for company in companies:
        print(f"\nProcessing company: {company}")
        category = get_user_category_choice()
        
        update_choice = input(f"Do you want to update the categories file with {company} in {category.name}? (y/n): ").lower()
        if update_choice == 'y':
            update_categories_yaml(category, company)
        else:
            print("Skipped updating categories.yaml")

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()