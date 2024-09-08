import sys
import os
import yaml

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from categories import Categories, Categorizations

def convert_to_yaml():
    categories_dict = {}
    for category, items in Categorizations:
        categories_dict[category.name] = items

    with open('categories.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(categories_dict, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print("Conversion complete. Check categories.yaml in the current directory.")

if __name__ == "__main__":
    convert_to_yaml()