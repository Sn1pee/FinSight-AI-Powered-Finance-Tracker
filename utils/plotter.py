import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('dark_background')

def plot_finance_dashboard(df: pd.DataFrame, summary: dict) -> plt.Figure:
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("📊 FinSight – Financial Overview", fontsize=16)

    fig.tight_layout(pad=3.0)
    # Style for fig
 
    # 1️⃣ Line Chart – Daily Spend
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    daily = df[df["Type"] == "Debit"].groupby("Date")["Amount"].sum()
    axs[0, 0].plot(daily.index, daily.values, marker="o", color="tomato")
    axs[0, 0].set_title("🧾 Daily Expenses")
    axs[0, 0].set_ylabel("Amount (₹)")
    axs[0, 0].tick_params(axis="x", rotation=30)

    # 2️⃣ Bar Chart – Category Spend
    cat = summary["category_summary"]
    axs[0, 1].bar(cat.index, cat.values, color="skyblue")
    axs[0, 1].set_title("📊 Expenses by Category")
    axs[0, 1].tick_params(axis="x", rotation=30)

    # 3️⃣ Pie Chart – Expense Split
    axs[1, 0].pie(cat, labels=cat.index,colors= ["#3498db", "#7f8c8d", "#34495e", "#ec7063", "#6c3483", "#1d8348"] ,  autopct="%1.1f%%", startangle=140)
    axs[1, 0].set_title("🧁 Expense Distribution")

    # 4️⃣ Bar – Income vs Expenses
    axs[1, 1].bar(["Income", "Expense", "Savings"], [
        summary["income"],
        summary["expense"],
        summary["savings"]
    ], color=["green", "red", "blue"])
    axs[1, 1].set_title("🟩 Income vs Expense vs Savings")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig
        