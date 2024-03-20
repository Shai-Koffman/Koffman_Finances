import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from display_expense_for_month import ExpenseForMonthDisplay
from expenses_processor import ExpenseAnalysis, AccountType

class ExpenseDashboard:
    def __init__(self, expense_analysis: ExpenseAnalysis):
        self.expense_analysis = expense_analysis

    def run(self):
        st.title("Koffman Financial Dashboard")

        # Manually list display methods in the desired order
        display_methods = [
            'display_bank_monthly_expenses_vs_gains',
            'display_expenses_for_month',
            'display_monthly_expenses_by_category',
            'display_detailed_transactions'
        ]

        # Sidebar menu for navigation, with "Monthly Expenses vs Gains" as the default selection
        menu_options = [method.replace('display_', '').replace('_', ' ').title() for method in display_methods]
        default_index = menu_options.index("Bank Monthly Expenses Vs Gains")  # Assuming this is the exact method name after title formatting
        selection = st.sidebar.selectbox("Menu", menu_options, index=default_index)

        # Mapping selection to method call
        selected_method_name = display_methods[menu_options.index(selection)]
        selected_method = getattr(self, selected_method_name)
        
        # Execute the selected method
        selected_method()

    def display_bank_monthly_expenses_vs_gains(self):
        st.header("Bank Monthly Expenses vs Gains")

        # Checkbox to exclude BANK_TRANSFERS_AND_MONEY_TRANSFERS
        exclude_transfers = st.checkbox('Exclude money transfers')

        # Calculate monthly expenses and gains
        gains_per_month, expenses_per_month = self.expense_analysis.bank_total_gains_and_expenses_per_month(exclude_transfers=exclude_transfers)
        
        # Generate a list of unique months from the data
        all_months = pd.to_datetime(expenses_per_month.index.union(gains_per_month.index)).strftime('%Y-%m').unique()
        excluded_months = st.multiselect('Select months to exclude', all_months)

        # Expenses Data
        expenses_data = pd.DataFrame({'Month': expenses_per_month.index, 'Expenses': expenses_per_month.values})
        expenses_data['Month'] = pd.to_datetime(expenses_data['Month']).dt.strftime('%Y-%m')
        expenses_data = expenses_data[~expenses_data['Month'].isin(excluded_months)]  # Exclude selected months
        expenses_data.sort_values(by='Month', inplace=True)
        st.subheader("Monthly Expenses")
        st.bar_chart(expenses_data.set_index('Month'))
        # Calculate and display average expenses 
        average_expenses = expenses_data['Expenses'].mean()
        st.write(f"Average Monthly Expenses: {average_expenses:.2f}")

        # Gains Data
        gains_data = pd.DataFrame({'Month': gains_per_month.index, 'Gains': gains_per_month.values})
        gains_data['Month'] = pd.to_datetime(gains_data['Month']).dt.strftime('%Y-%m')
        gains_data = gains_data[~gains_data['Month'].isin(excluded_months)]  # Exclude selected months
        gains_data.sort_values(by='Month', inplace=True)
        st.subheader("Monthly Gains")
        st.bar_chart(gains_data.set_index('Month'))
        # Calculate and display average gains
        average_gains = gains_data['Gains'].mean()
        st.write(f"Average Monthly Gains: {average_gains:.2f}")

        # Difference Data
        difference_data = pd.DataFrame({
            'Month': expenses_data['Month'],
            'Difference': gains_data['Gains'].values - expenses_data['Expenses'].values
        })
        difference_data.sort_values(by='Month', inplace=True)

        # Plotting the difference as a bar chart with colors based on value
        fig, ax = plt.subplots()
        ax.bar(difference_data['Month'], difference_data['Difference'], color=['green' if x > 0 else 'red' for x in difference_data['Difference']])
        ax.axhline(0, color='black', lw=2)  # X-axis
        plt.xticks(rotation=45)
        plt.ylabel('Difference (Gains - Expenses)')
        plt.title('Monthly Difference in Gains and Expenses')

        # Display the plot in Streamlit
        st.pyplot(fig)

    def display_expenses_for_month(self):
        # Use Streamlit's date_input to select a year and month
        selected_date = st.date_input("Select a year and month", value=pd.to_datetime("today"), min_value=None, max_value=None, key=None)
        year, month = selected_date.year, selected_date.month
        efmd = ExpenseForMonthDisplay() 
        efmd.display_expenses_for_month(self.expense_analysis, year, month)

    def display_monthly_expenses_by_category(self):
        st.header("Monthly Expenses by Category")

        # Dropdown to select category
        categories = self.expense_analysis.get_categories()  # Assuming this method exists and returns a list of categories
        selected_category = st.selectbox("Select a Category", categories)

        # Radio buttons to choose between Bank or Visa
        account_type = st.radio("Choose Account Type", ( 'Visa Max','Bank'))
        if account_type == 'Visa Max':
            account_type = AccountType.VISA_MAX
        else:
            account_type = AccountType.BANK

        # Fetching expenses and gains data for the selected category and account type
        expenses_per_month, gains_per_month = self.expense_analysis.get_monthly_expenses_and_gains_by_category(selected_category, account_type)

        # Expenses Data
        expenses_data = pd.DataFrame({'Month': expenses_per_month.index, 'Expenses': expenses_per_month.values})
        expenses_data['Month'] = pd.to_datetime(expenses_data['Month']).dt.strftime('%Y-%m')
        expenses_data.sort_values(by='Month', inplace=True)
        st.subheader(f"Monthly Expenses for {selected_category}")
        st.bar_chart(expenses_data.set_index('Month'))

        # Gains Data
        gains_data = pd.DataFrame({'Month': gains_per_month.index, 'Gains': gains_per_month.values})
        gains_data['Month'] = pd.to_datetime(gains_data['Month']).dt.strftime('%Y-%m')
        gains_data.sort_values(by='Month', inplace=True)
        st.subheader(f"Monthly Gains for {selected_category}")
        st.bar_chart(gains_data.set_index('Month'))

    def display_detailed_transactions(self):
        st.header("Detailed Transactions")

        # Dropdown to select category
        categories = self.expense_analysis.get_categories()
        selected_category = st.selectbox("Select a Category", categories)

        # Radio buttons to choose between Bank or Visa
        account_type = st.radio("Choose Account Type", ('Bank', 'Visa Max'))
        account_type_enum = AccountType.VISA_MAX if account_type == 'Visa Max' else AccountType.BANK

        # Use Streamlit's date_input to select a year and month
        selected_date = st.date_input("Select a year and month", value=pd.to_datetime("today"))
        year, month = selected_date.year, selected_date.month

        # Fetching detailed transactions
        detailed_transactions = self.expense_analysis.get_detailed_expenses(account_type_enum, year, month, selected_category)

        # Sorting transactions by amount in the expense or gain
        detailed_transactions.sort(key=lambda x: max(x.get_expense_sum(), x.get_gains_sum()), reverse=True)

        # Preparing data for display based on account type
        data = []
        match account_type_enum:
            case AccountType.BANK:
                for transaction in detailed_transactions:
                    data.append([
                        transaction.get_transaction_date().strftime('%Y-%m-%d'),
                        transaction.get_category().name,
                        transaction.get_expense_sum(),
                        transaction.get_gains_sum(),
                        transaction.company,
                        # BankTransaction specific fields here (placeholders for VisaMaxTransaction fields)
                    ])
                columns = ['Date', 'Category', 'Expense Sum', 'Gains Sum', 'Company']
        
            case AccountType.VISA_MAX:
                for transaction in detailed_transactions:
                    data.append([
                        transaction.get_transaction_date().strftime('%Y-%m-%d'),
                        transaction.get_category().name,
                        transaction.get_expense_sum(),
                        transaction.get_gains_sum(),
                        transaction.company,
                        transaction.visa_card_number,
                        transaction.coin.name,
                        transaction.normalized_expense_sum,
                        transaction.visa_max_category,
                        transaction.sheet_title
                    ])
                columns = [
                    'Date', 'Category', 'Expense Sum', 'Gains Sum', 'Company', 
                    'Visa Card Number', 'Coin Type', 'Normalized Expense Sum', 
                    'Visa Max Category', 'Sheet Title'
                ]

        # Displaying transactions in a table
        df = pd.DataFrame(data, columns=columns)
        st.table(df)
