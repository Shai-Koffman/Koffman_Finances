import sqlite3

def save_to_database(grouped_expenses):
    with sqlite3.connect('expenses.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS expenses
                     (month INTEGER, category TEXT, amount REAL)''')
        c.execute('DELETE FROM expenses')
        for month, cat_mapping in grouped_expenses.items():
            for category, expenses_tuple in cat_mapping.items():
                c.execute("INSERT INTO expenses VALUES (?, ?, ?)",
                          (month, category, expenses_tuple[1]))
        # Cursor is manually closed here, but it's optional in this context
        c.close()
        print("Expenses saved to database successfully.")
