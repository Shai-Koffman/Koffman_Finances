import streamlit as st


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

        # Visa Max expenses and gains
        st.subheader("Visa Max Expenses and Gains")
        visa_max_expenses = expense_analysis.visa_max_monthly_expenses(year, month).round().astype(int)
        visa_max_gains = expense_analysis.visa_max_monthly_gains(year, month).round().astype(int)

        # Filter out 0 expenses and gains, then sort in descending order
        visa_max_expenses = visa_max_expenses[visa_max_expenses > 0].sort_values(ascending=False)
        visa_max_gains = visa_max_gains[visa_max_gains > 0].sort_values(ascending=False)

        # Display Visa expenses with Shekel sign in a table using Markdown
        if not visa_max_expenses.empty:
            st.write("Visa Max Expenses:")
            visa_max_expenses_table = "<table><tr><th>Category</th><th>Expense</th></tr>"
            visa_max_expenses_table += "\n".join([f"<tr><td>{category}</td><td>₪{expense:,}</td></tr>" for category, expense in visa_max_expenses.items()])
            # Calculate and append the total row
            total_visa_max_expenses = visa_max_expenses.sum()
            visa_max_expenses_table += f"<tr style='font-weight: bold;'><td>Total</td><td>₪{total_visa_max_expenses:,}</td></tr>"
            visa_max_expenses_table += "</table>"
            st.markdown(visa_max_expenses_table, unsafe_allow_html=True)
        else:
            st.write("No Visa expenses for this month.")

        # Display Visa Max gains with Shekel sign in a table using Markdown
        if not visa_max_gains.empty:
            st.write("Visa Max Gains:")
            visa_max_gains_table = "<table><tr><th>Category</th><th>Gains</th></tr>"
            visa_max_gains_table += "\n".join([f"<tr><td>{category}</td><td>₪{gains:,}</td></tr>" for category, gains in visa_max_gains.items()])
            # Calculate and append the total row
            total_visa_max_gains = visa_max_gains.sum()
            visa_max_gains_table += f"<tr style='font-weight: bold;'><td>Total</td><td>₪{total_visa_max_gains:,}</td></tr>"
            visa_max_gains_table += "</table>"
            st.markdown(visa_max_gains_table, unsafe_allow_html=True)
        else:
            st.write("No Visa Max gains for this month.")
        
            # Isracard expenses and gains
        st.subheader("Isracard Expenses and Gains")
        isracard_expenses = expense_analysis.isracard_monthly_expenses(year, month).round().astype(int)
        isracard_gains = expense_analysis.isracard_monthly_gains(year, month).round().astype(int)

        # Filter out 0 expenses and gains, then sort in descending order
        isracard_expenses = isracard_expenses[isracard_expenses > 0].sort_values(ascending=False)
        isracard_gains = isracard_gains[isracard_gains > 0].sort_values(ascending=False)

        # Display Isracard expenses with Shekel sign in a table using Markdown
        if not isracard_expenses.empty:
            st.write("Isracard Expenses:")
            isracard_expenses_table = "<table><tr><th>Category</th><th>Expense</th></tr>"
            isracard_expenses_table += "\n".join([f"<tr><td>{category}</td><td>₪{expense:,}</td></tr>" for category, expense in isracard_expenses.items()])
            # Calculate and append the total row
            total_isracard_expenses = isracard_expenses.sum()
            isracard_expenses_table += f"<tr style='font-weight: bold;'><td>Total</td><td>₪{total_isracard_expenses:,}</td></tr>"
            isracard_expenses_table += "</table>"
            st.markdown(isracard_expenses_table, unsafe_allow_html=True)
        else:
            st.write("No Isracard expenses for this month.")

        # Display Isracard gains with Shekel sign in a table using Markdown
        if not isracard_gains.empty:
            st.write("Isracard Gains:")
            isracard_gains_table = "<table><tr><th>Category</th><th>Gains</th></tr>"
            isracard_gains_table += "\n".join([f"<tr><td>{category}</td><td>₪{gains:,}</td></tr>" for category, gains in isracard_gains.items()])
            # Calculate and append the total row
            total_isracard_gains = isracard_gains.sum()
            isracard_gains_table += f"<tr style='font-weight: bold;'><td>Total</td><td>₪{total_isracard_gains:,}</td></tr>"
            isracard_gains_table += "</table>"
            st.markdown(isracard_gains_table, unsafe_allow_html=True)
        else:
            st.write("No Isracard gains for this month.")

