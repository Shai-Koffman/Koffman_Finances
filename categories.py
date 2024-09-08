import yaml
from enum import Enum, auto
from functools import total_ordering

@total_ordering
class Categories(Enum):
    SUPER = auto()
    ELECTRICITY = auto()
    INTERNET_AND_PHONES = auto()
    OTHER_FOOD = auto()
    RESTAURANTS_AND_HOTELS = auto()
    WATER = auto()
    ARNONA = auto()
    CAR_INSURANCE = auto()
    CAR_EXPENSES = auto()
    HEALTH_INSURANCE = auto()
    OTHER_INSURANCE = auto()
    GAS = auto()
    FUEL = auto()
    INCOME_TAX = auto()
    HEALTH_AND_MACABI = auto()
    SCHOOLS = auto()
    STARTUP = auto()
    HUGIM = auto()
    INVESTMENTS = auto()
    CASPOMAT = auto()
    CLOTHING = auto()
    PRESENTS = auto()
    INTERNET_SERVICES_AND_SHOPPING = auto()
    ABROAD_EXPENSES = auto()
    VISA_MAX = auto()
    ISRACARD = auto()
    CHECKS = auto()
    BANK_AMLOT = auto()
    HOME_RELATED = auto()
    FUN_AND_MOVIES = auto()
    MISC = auto()
    INCOMING_TRANSFERS = auto()
    SALARIES = auto()
    BANK_TRANSFERS_AND_MONEY_TRANSFERS = auto()
    UNKNOWN = auto()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    def __hash__(self):
        return hash(self.value)
    
    def to_string(self):
        return str(self)
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Categories.{self.name}"
    
    def __reduce__(self):
        return (self.__class__, (self.name,))

# Load Categorizations from YAML file
with open('categories.yaml', 'r', encoding='utf-8') as f:
    categories_data = yaml.safe_load(f)

Categorizations = [(getattr(Categories, cat), items) for cat, items in categories_data.items()]

unknown_companies = []

def get_category(company: str) -> Categories:
    """
    Determines the category of a given company based on predefined categorizations.

    Args:
    - company (str): The name of the company to categorize.

    Returns:
    - Categories: The category the company belongs to. Returns Categories.UNKNOWN if no match is found.
    """
    if company is None:
        return Categories.UNKNOWN
    
    for category, matches in Categorizations:
        try:
            if any(match in company for match in matches):
                return category
        except TypeError:
            print(f"Error processing company {company}")
    
    if company not in unknown_companies:
        unknown_companies.append(company)
        with open(".unknown_companies.txt", "a", encoding='utf-8') as f:
            f.write(company + "\n")
            print(f"Unknown category for company {company}")

    return Categories.UNKNOWN


