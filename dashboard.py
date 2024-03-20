import streamlit as st
import pandas as pd
import inspect
import matplotlib.pyplot as plt
from display_expense_for_month import ExpenseForMonthDisplay
from expenses_processor import ExpenseAnalysis

class ExpenseDashboard:
    def __init__(self, expense_analysis: ExpenseAnalysis):
        self.expense_analysis = expense_analysis

    def run(self):
        st.title("Koffman Financial Dashboard")

        # Dynamically get display methods
        display_methods = [method_name for method_name, method in inspect.getmembers(self, predicate=inspect.ismethod) if method_name.startswith('display_')]

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
        
        # Expenses Data
        expenses_data = pd.DataFrame({'Month': expenses_per_month.index, 'Expenses': expenses_per_month.values})
        expenses_data['Month'] = pd.to_datetime(expenses_data['Month']).dt.strftime('%Y-%m')
        expenses_data.sort_values(by='Month', inplace=True)
        st.subheader("Monthly Expenses")
        st.bar_chart(expenses_data.set_index('Month'))

        # Gains Data
        gains_data = pd.DataFrame({'Month': gains_per_month.index, 'Gains': gains_per_month.values})
        gains_data['Month'] = pd.to_datetime(gains_data['Month']).dt.strftime('%Y-%m')
        gains_data.sort_values(by='Month', inplace=True)
        st.subheader("Monthly Gains")
        st.bar_chart(gains_data.set_index('Month'))

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

    def display_monthly_expenses_by_category(self):
        st.header("Monthly Expenses by Category")
        monthly_expenses = self.expense_analysis.monthly_expenses_by_category().reset_index()

        # Filter out categories where total expenses are over 1000
        monthly_expenses = monthly_expenses[monthly_expenses['expense'] > 1000]

        # Format the 'date' column to only show year and month
        monthly_expenses['date'] = monthly_expenses['date'].dt.strftime('%m/%Y')

        # Rename the columns for better readability
        monthly_expenses.columns = ['Month', 'Category', 'Expense Total']

        # Sort the data by month
        monthly_expenses.sort_values('Month', inplace=True)
         # Add a separator row between different months
        last_month = None
        separator_rows = []
        for i, row in monthly_expenses.iterrows():
            if last_month != row['Month']:
                if last_month is not None:
                    # Add a separator row
                    separator_rows.append({'Month': '', 'Category': '', 'Expense Total': ''})
                last_month = row['Month']
            separator_rows.append(row.to_dict())

        # Create a new DataFrame with the separator rows
        monthly_expenses = pd.DataFrame(separator_rows)

        # Display the data table
        st.table(monthly_expenses)

    def display_category_month_by_month(self):
        category = st.selectbox("Select a category", self.expense_analysis.all_generic_expenses['category'].unique())
        st.header(f"Month by Month Expenses for {category}")
        category_monthly_expenses = self.expense_analysis.category_month_by_month(category).reset_index()
        st.write(category_monthly_expenses)

    def display_expenses_for_month(self):
        # Use Streamlit's date_input to select a year and month
        selected_date = st.date_input("Select a year and month", value=pd.to_datetime("today"), min_value=None, max_value=None, key=None)
        year, month = selected_date.year, selected_date.month
        efmd = ExpenseForMonthDisplay() 
        efmd.display_expenses_for_month(self.expense_analysis, year, month)

       