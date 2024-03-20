import streamlit as st
import pandas as pd

class ExpenseForMonthDisplay:
    def display_expenses_for_month(self, expense_analysis, year, month):
        st.header(f"Expenses and Gains for {month}/{year}")

        # Bank expenses and gains
        st.subheader("Bank Expenses and Gains")
        bank_expenses = expense_analysis.bank_monthly_expenses(year, month).round().astype(int)
        bank_gains = expense_analysis.bank_monthly_gains(year, month).round().astype(int)

        # Filter out 0 expenses and gains, then sort in descending order
        bank_expenses = bank_expenses[bank_expenses > 0].sort_values(ascending=False)
        bank_gains = bank_gains[bank_gains > 0].sort_values(ascending=False)

        # Display expenses with Shekel sign in a table using Markdown
        if not bank_expenses.empty:
            st.write("Expenses:")
            expenses_table = "<table><tr><th>Category</th><th>Expense</th></tr>"
            expenses_table += "\n".join([f"<tr><td>{category}</td><td>₪{expense:,}</td></tr>" for category, expense in bank_expenses.items()])
            # Calculate and append the total row
            total_expenses = bank_expenses.sum()
            expenses_table += f"<tr style='font-weight: bold;'><td>Total</td><td>₪{total_expenses:,}</td></tr>"
            expenses_table += "</table>"
            st.markdown(expenses_table, unsafe_allow_html=True)
        else:
            st.write("No bank expenses for this month.")

        # Display gains with Shekel sign in a table using Markdown
        if not bank_gains.empty:
            st.write("Gains:")
            gains_table = "<table><tr><th>Category</th><th>Gains</th></tr>"
            gains_table += "\n".join([f"<tr><td>{category}</td><td>₪{gains:,}</td></tr>" for category, gains in bank_gains.items()])
            # Calculate and append the total row
            total_gains = bank_gains.sum()
            gains_table += f"<tr style='font-weight: bold;'><td>Total</td><td>₪{total_gains:,}</td></tr>"
            gains_table += "</table>"
            st.markdown(gains_table, unsafe_allow_html=True)
        else:
            st.write("No bank gains for this month.")