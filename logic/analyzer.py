def analyze(df):
    income = df[df['Type'] == 'Credit']['Amount'].sum()
    expense = df[df['Type'] == 'Debit']['Amount'].sum()
    savings = income - expense
    category_summary = df[df['Type'] == 'Debit'].groupby('Category')['Amount'].sum().sort_values(ascending=False)
    return {
        "income": income,
        "expense": expense,
        "savings": savings,
        "category_summary": category_summary
    }
