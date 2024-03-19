import streamlit as st
import pandas as pd
from expenses_processor import ExpenseAnalysis


class ExpenseDashboard:
    def __init__(self, expense_analysis: ExpenseAnalysis):
        self.expense_analysis = expense_analysis


    def run(self):
        st.title("Koffman Household financial Dashboard")
        self.display_monthly_expenses_vs_gains()
        # self.display_monthly_expenses_by_category()
        # self.display_category_month_by_month()
        # self.display_yearly_expenses_by_category()
        # self.display_expenses_by_date_range()

    def display_monthly_expenses_vs_gains(self):
        st.header("Monthly Expenses vs Gains")

        # Calculate monthly expenses and gains
        gains_per_month, expenses_per_month = self.expense_analysis.total_gains_and_expenses_per_month()
        monthly_data = pd.DataFrame({'Month': expenses_per_month.index, 'Expenses': expenses_per_month.values, 'Gains': -gains_per_month.values})

        # Format the 'Month' column to only show year and month
        monthly_data['Month'] = monthly_data['Month'].dt.strftime('%m/%Y')

        # Create a bar chart using Streamlit's native functionality
        st.bar_chart(monthly_data.set_index('Month'))




    #The method below should display the monthly expenses in a pie chart of categories per month.
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

    def display_yearly_expenses_by_category(self):
        st.header("Yearly Expenses by Category")
        yearly_expenses = self.expense_analysis.yearly_expenses_by_category().reset_index()
        st.write(yearly_expenses)

    def display_expenses_by_date_range(self):
        start_date = st.date_input("Start Date", value=self.expense_analysis.all_generic_expenses.index.min())
        end_date = st.date_input("End Date", value=self.expense_analysis.all_generic_expenses.index.max())
        filtered_expenses = self.expense_analysis.all_generic_expenses.loc[start_date:end_date]

        st.header(f"Monthly Expenses by Category ({start_date} - {end_date})")
        monthly_expenses_filtered = filtered_expenses.groupby([pd.Grouper(freq='ME'), 'category'])['expense'].sum().reset_index()
        st.write(monthly_expenses_filtered)

