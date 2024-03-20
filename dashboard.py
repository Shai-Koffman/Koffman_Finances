import streamlit as st
import pandas as pd
import inspect
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

        # Calculate monthly expenses and gains
        gains_per_month, expenses_per_month = self.expense_analysis.bank_total_gains_and_expenses_per_month()
        
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

        st.header(f"Expenses and Gains for {selected_date.strftime('%B %Y')}")

        # Bank expenses and gains
        st.subheader("Bank Expenses and Gains")
        bank_expenses = self.expense_analysis.bank_monthly_expenses(year, month).round().astype(int)
        bank_gains = self.expense_analysis.bank_monthly_gains(year, month).round().astype(int)

        # Filter out 0 expenses and gains, then sort in descending order
        bank_expenses = bank_expenses[bank_expenses > 0].sort_values(ascending=False)
        bank_gains = bank_gains[bank_gains > 0].sort_values(ascending=False)

        # Display expenses with Shekel sign in a table using Markdown
        if not bank_expenses.empty:
            st.write("Expenses:")
            expenses_table = "<table><tr><th style='text-align: left;'>Category</th><th style='text-align: right;'>Expense</th></tr>"
            expenses_table += "\n".join([f"<tr><td>{category}</td><td style='text-align: right;'>₪{expense:,}</td></tr>" for category, expense in bank_expenses.items()])
            # Calculate and append the total row
            total_expenses = bank_expenses.sum()
            expenses_table += f"<tr style='font-weight: bold; background-color: #f0f0f0;'><td>Total</td><td style='text-align: right;'>₪{total_expenses:,}</td></tr>"
            expenses_table += "</table>"
            st.markdown(expenses_table, unsafe_allow_html=True)
        else:
            st.write("No bank expenses for this month.")

        # Display gains with Shekel sign in a table using Markdown
        if not bank_gains.empty:
            st.write("Gains:")
            gains_table = "<table><tr><th style='text-align: left;'>Category</th><th style='text-align: right;'>Gains</th></tr>"
            gains_table += "\n".join([f"<tr><td>{category}</td><td style='text-align: right;'>₪{gains:,}</td></tr>" for category, gains in bank_gains.items()])
            # Calculate and append the total row
            total_gains = bank_gains.sum()
            gains_table += f"<tr style='font-weight: bold; background-color: #f0f0f0;'><td>Total</td><td style='text-align: right;'>₪{total_gains:,}</td></tr>"
            gains_table += "</table>"
            st.markdown(gains_table, unsafe_allow_html=True)
        else:
            st.write("No bank gains for this month.")

        # Visa expenses and gains
        st.subheader("Visa Max Expenses and Gains")
        visa_max_expenses = self.expense_analysis.visa_max_monthly_expenses(year, month).round().astype(int)
        visa_max_gains = self.expense_analysis.visa_max_monthly_gains(year, month).round().astype(int)

        # Filter out 0 expenses and gains, then sort in descending order
        visa_max_expenses = visa_max_expenses[visa_max_expenses > 0].sort_values(ascending=False)
        visa_max_gains = visa_max_gains[visa_max_gains > 0].sort_values(ascending=False)

        # Display Visa Max expenses with Shekel sign in a table using Markdown
        if not visa_max_expenses.empty:
            st.write("Visa Max Expenses:")
            visa_expenses_table = "<table><tr><th style='text-align: left;'>Category</th><th style='text-align: right;'>Expense</th></tr>"
            visa_expenses_table += "\n".join([f"<tr><td>{category}</td><td style='text-align: right;'>₪{expense:,}</td></tr>" for category, expense in visa_max_expenses.items()])
            # Calculate and append the total row
            total_visa_expenses = visa_max_expenses.sum()
            visa_expenses_table += f"<tr style='font-weight: bold; background-color: #f0f0f0;'><td>Total</td><td style='text-align: right;'>₪{total_visa_expenses:,}</td></tr>"
            visa_expenses_table += "</table>"
            st.markdown(visa_expenses_table, unsafe_allow_html=True)
        else:
            st.write("No Visa Max expenses for this month.")

        # Display Visa Max gains with Shekel sign in a table using Markdown
        if not visa_max_gains.empty:
            st.write("Visa Max Gains:")
            visa_gains_table = "<table><tr><th style='text-align: left;'>Category</th><th style='text-align: right;'>Gains</th></tr>"
            visa_gains_table += "\n".join([f"<tr><td>{category}</td><td style='text-align: right;'>₪{gains:,}</td></tr>" for category, gains in visa_max_gains.items()])
            # Calculate and append the total row
            total_visa_gains = visa_max_gains.sum()
            visa_gains_table += f"<tr style='font-weight: bold; background-color: #f0f0f0;'><td>Total</td><td style='text-align: right;'>₪{total_visa_gains:,}</td></tr>"
            visa_gains_table += "</table>"
            st.markdown(visa_gains_table, unsafe_allow_html=True)
        else:
            st.write("No Visa Max gains for this month.")
