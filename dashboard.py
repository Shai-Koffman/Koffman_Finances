import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from display_expense_for_month import ExpenseForMonthDisplay
from expenses_processor import TransactionsAnalysis, AccountType
from investements import InvestementProcessor
from financial_projector import FinancialProjector
import matplotlib.pyplot as plt
from categories import Categories
import plotly.express as px

class Dashboard:
    def __init__(self, expense_analysis: TransactionsAnalysis, investements_processor: InvestementProcessor):
        self.expense_analysis = expense_analysis
        self.investements_processor = investements_processor

    def run(self):
        st.title("Koffman Financial Dashboard")

        # Register display methods using a decorator
        self.display_methods = [
            self.display_bank_monthly_expenses_vs_gains,
            self.display_expenses_for_month,
            self.display_monthly_expenses_by_category,
            self.display_detailed_transactions,
            self.display_invested_money_distribution,
            self.display_projected_financials
        ]

        # Sidebar menu for navigation, with "Monthly Expenses vs Gains" as the default selection
        menu_options = [method.__name__.replace('display_', '').replace('_', ' ').title() for method in self.display_methods]
        default_index = menu_options.index("Bank Monthly Expenses Vs Gains")  # Assuming this is the exact method name after title formatting
        selection = st.sidebar.selectbox("Menu", menu_options, index=default_index)

        # Mapping selection to method call
        selected_method = next((method for method in self.display_methods if method.__name__ == f"display_{selection.replace(' ', '_').lower()}"), None)
        
        # Execute the selected method
        if selected_method:
            selected_method()

    @staticmethod
    def display_method(func):
        func.display_method = True
        return func

    @display_method
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
        fig = go.Figure()
        fig.add_trace(go.Bar(x=difference_data['Month'], y=difference_data['Difference'], marker_color=['green' if x > 0 else 'red' for x in difference_data['Difference']]))
        fig.add_shape(type='line', x0=difference_data['Month'].min(), y0=0, x1=difference_data['Month'].max(), y1=0, line=dict(color='black', width=2))
        fig.update_layout(xaxis_tickangle=-45, yaxis_title='Difference (Gains - Expenses)', title='Monthly Difference in Gains and Expenses')
        st.plotly_chart(fig)

    @display_method
    def display_expenses_for_month(self):
        # Use Streamlit's date_input to select a year and month
        selected_date = st.date_input("Select a year and month", value=pd.to_datetime("today"), min_value=None, max_value=None, key=None)
        year, month = selected_date.year, selected_date.month
        efmd = ExpenseForMonthDisplay() 
        efmd.display_expenses_for_month(self.expense_analysis, year, month)

    @display_method
    def display_monthly_expenses_by_category(self):
        st.header("Monthly Expenses by Category")
        # Fetching expenses data for all categories across all account types
        all_categories = self.expense_analysis.get_categories()
      
        total_expenses_per_category = pd.Series(dtype=float)
        for category in all_categories:
            bank_expenses, _ = self.expense_analysis.get_monthly_expenses_and_gains_by_category(category, AccountType.BANK)
            visa_max_expenses, _ = self.expense_analysis.get_monthly_expenses_and_gains_by_category(category, AccountType.VISA_MAX)
            isracard_expenses, _ = self.expense_analysis.get_monthly_expenses_and_gains_by_category(category, AccountType.ISRACARD)
            # Sum expenses for each category across all account types
            total_category_expenses = bank_expenses.add(visa_max_expenses, fill_value=0).add(isracard_expenses, fill_value=0)
            # Save the sum of expenses for each month
            total_expenses_per_category[category] = total_category_expenses.sum()
            # Save the number of months with expenses to calculate the average correctly later
            months_with_expenses = total_category_expenses.count()
            total_expenses_per_category[f"{category}_months"] = months_with_expenses
        # Calculate average monthly expenses per category
        avg_monthly_expenses_per_category = pd.Series({category: total_expenses_per_category[category] / total_expenses_per_category[f"{category}_months"] for category in all_categories})

        # Improved plotting of the pie chart for average monthly expenses per category with better label management using Plotly
        category_names = [category.to_string() for category in avg_monthly_expenses_per_category.index]
        fig = px.pie(
            avg_monthly_expenses_per_category,
            values=avg_monthly_expenses_per_category.values,
            names=category_names,
            title='Average Monthly Expenses Per Category',
            color_discrete_sequence=px.colors.qualitative.Set3  # This is a built-in color sequence, but you can customize it
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True)

        st.plotly_chart(fig, use_container_width=True)
        # Dropdown to select category
        categories = self.expense_analysis.get_categories()  # Assuming this method exists and returns a list of categories
        selected_category = st.selectbox("Select a Category", categories)

        # Fetching expenses and gains data for the selected category across all account types
        bank_expenses, bank_gains = self.expense_analysis.get_monthly_expenses_and_gains_by_category(selected_category, AccountType.BANK)
        visa_max_expenses, visa_max_gains = self.expense_analysis.get_monthly_expenses_and_gains_by_category(selected_category, AccountType.VISA_MAX)
        isracard_expenses, isracard_gains = self.expense_analysis.get_monthly_expenses_and_gains_by_category(selected_category, AccountType.ISRACARD)

        # Combine data from all account types
        all_expenses = bank_expenses.add(visa_max_expenses, fill_value=0).add(isracard_expenses, fill_value=0)
        all_gains = bank_gains.add(visa_max_gains, fill_value=0).add(isracard_gains, fill_value=0)

        # Create a common date range for both gains and expenses
        all_dates = all_expenses.index.union(all_gains.index)
        # Reindex gains and expenses to the common date range and fill missing values with 0
        all_expenses = all_expenses.reindex(all_dates, fill_value=0)
        all_gains = all_gains.reindex(all_dates, fill_value=0)

        # Expenses Data
        expenses_data = pd.DataFrame({'Month': all_expenses.index, 'Expenses': all_expenses.values})
        expenses_data['Month'] = pd.to_datetime(expenses_data['Month']).dt.strftime('%Y-%m')
        expenses_data.sort_values(by='Month', inplace=True)
        st.subheader(f"Total Monthly Expenses for {selected_category}")
        st.bar_chart(expenses_data.set_index('Month'))

        # Gains Data
        gains_data = pd.DataFrame({'Month': all_gains.index, 'Gains': all_gains.values})
        gains_data['Month'] = pd.to_datetime(gains_data['Month']).dt.strftime('%Y-%m')
        gains_data.sort_values(by='Month', inplace=True)
        st.subheader(f"Total Monthly Gains for {selected_category}")
        st.bar_chart(gains_data.set_index('Month'))

    @display_method
    def display_detailed_transactions(self):
        st.header("Detailed Transactions")

        # Dropdown to select category
        categories = self.expense_analysis.get_categories()
        selected_category = st.selectbox("Select a Category", categories)

        # Radio buttons to choose between Bank or Visa
        account_type = st.radio("Choose Account Type", ('Bank', 'Visa Max', 'Isracard'))
        account_type_enum = {
            'Bank': AccountType.BANK,
            'Visa Max': AccountType.VISA_MAX,
            'Isracard': AccountType.ISRACARD
        }[account_type]

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
            case AccountType.ISRACARD:
                for transaction in detailed_transactions:
                    data.append([
                        transaction.get_transaction_date().strftime('%Y-%m-%d'),
                        transaction.get_category().name,
                        transaction.get_expense_sum(),
                        transaction.get_gains_sum(),
                        transaction.company
                    ])
                columns = ['Date', 'Category', 'Expense Sum', 'Gains Sum', 'Company']

        # Displaying transactions in a table
        df = pd.DataFrame(data, columns=columns)
        st.table(df)

    @display_method
    def display_invested_money_distribution(self):
        st.header("Invested Money Distribution")
        
        # Fetch investment data as a DataFrame using the existing investements_processor instance
        investments_df = self.investements_processor.get_investements_df()
        #round the calculated_historical_annual_interest_rate to 2 decimal points
        investments_df['calculated_historical_annual_interest_rate'] = investments_df['calculated_historical_annual_interest_rate'].round(2)
        # Round numbers in the 'amount' column to full numbers
        investments_df['amount'] = investments_df['amount'].round()
        st.dataframe(investments_df, width=700)  # Adjust the width as needed

        # Calculate and display the total amount invested
        total_invested = investments_df['amount'].sum()
        st.markdown(f"**Total Amount Invested:** {total_invested:,.0f} NIS")

    @display_method
    def display_projected_financials(self):
        st.header("Projected Financials")

        # Checkbox to exclude BANK_TRANSFERS_AND_MONEY_TRANSFERS
        exclude_transfers = st.checkbox('Exclude money transfers')

        # Calculate monthly expenses and gains, excluding bank transfers as specified
        _, expenses_per_month = self.expense_analysis.bank_total_gains_and_expenses_per_month(exclude_transfers=exclude_transfers)

        # Calculate the average monthly expenses
        average_monthly_expenses = expenses_per_month.mean()

        # Calculate the static annual expenses (average monthly expenses * 12) and display in a larger font inside a box
        static_annual_expenses = (average_monthly_expenses * 12).round()
        st.markdown(f"<div style='border: 2px solid #4CAF50; padding: 10px; font-size: 20px;'>Static Annual Expenses: {static_annual_expenses} NIS</div>", unsafe_allow_html=True)

        # Fetch investment data as a list of Investement objects
        investments = self.investements_processor.get_investement_list()
        projected_investments = []

        yearly_totals = {year: 0 for year in range(1, 11)}  # Initialize yearly totals
        for investment in investments:
            historical_annual_interest_rate = FinancialProjector.calculate_projected_historical_annual_interest_rate(investment)
            for year in range(1, 11):
                if historical_annual_interest_rate != 0:
                    future_value = FinancialProjector.calculate_future_compounded_value(
                        investment, year, historical_annual_interest_rate / 100)
                else:
                    future_value = investment.normalized_amount
                projected_investments.append({
                    'Investment Name': investment.name,
                    'Year': year,
                    'Projected Value': f"{future_value:,.0f}"
                })
                yearly_totals[year] += future_value  # Add to yearly total

        # Store yearly totals separately
        yearly_totals_rows = []
        for year, total in yearly_totals.items():
            yearly_totals_rows.append({
                'Investment Name': 'Total for Year',
                'Year': year,
                'Projected Value': f"₪{total:,.0f}"
            })

        # Append yearly totals to projected_investments after all individual investments have been processed
        projected_investments.extend(yearly_totals_rows)

        projected_investments_df = pd.DataFrame(projected_investments)
        st.subheader("Projected Investment Values for Next 10 Years")
        pivoted_df = projected_investments_df.pivot(index='Investment Name', columns='Year', values='Projected Value')
        st.dataframe(pivoted_df)

        # Convert 'Projected Value' to numeric, ensuring errors are handled (e.g., set to NaN)
        projected_investments_df['Projected Value'] = pd.to_numeric(projected_investments_df['Projected Value'].str.replace(',', ''), errors='coerce')

        # Summing up 'Projected Value' for each year after conversion
        total_projected_investments = projected_investments_df.groupby('Year')['Projected Value'].sum()

        # Now perform the subtraction for 'Net Worth' using the static annual expenses
        financial_projection = pd.DataFrame({
            'Year': range(1, 11),
            'Net Worth': total_projected_investments.values - static_annual_expenses
        })

        st.subheader("Projected Net Worth Over 10 Years (Current Growth rate)")
        st.line_chart(financial_projection.set_index('Year'))

        st.subheader("Projected Future Net Worth - With configuration")
        # Allow users to choose the yearly interest rate in percentile
        static_growth_rate = st.number_input("Choose Yearly Interest Rate in Percentile", value=8.0, min_value=0.0, max_value=100.0) / 100
        initial_net_worth = sum([investment.normalized_amount for investment in self.investements_processor.get_investement_list()])
        
        # Allow users to override the monthly expenses
        monthly_expenses_override = st.number_input("Override Monthly Expenses", value=static_annual_expenses / 12, format="%.2f")
        static_annual_expenses = monthly_expenses_override * 12

        years = range(1, 11)
        net_worth_with_growth = []


        for year in years:
            # Compounded growth calculation for each year
            net_worth_for_year = (initial_net_worth * ((1 + static_growth_rate) ** year)) - static_annual_expenses
            net_worth_with_growth.append(net_worth_for_year)

        # Create DataFrame for plotting
        df_growth = pd.DataFrame({
            'Year': list(years),
            'Net Worth': net_worth_with_growth
        })

        # Plotting the line chart
        st.line_chart(df_growth.set_index('Year'))

