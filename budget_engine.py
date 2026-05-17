from expense_manager import get_monthly_expenses

def analyze_budget(monthly_income):
    df = get_monthly_expenses()

    if df.empty:
        return 0, 0, "No expenses recorded this month.", {}

    total_spent = df["amount"].sum()
    percentage = (total_spent / monthly_income) * 100 if monthly_income > 0 else 0

    # Category breakdown
    category_breakdown = df.groupby("category")["amount"].sum().to_dict()

    if percentage > 100:
        status = "🚨 Overspending! You have exceeded your monthly income."
    elif percentage > 80:
        status = "⚠️ Warning! You have used more than 80% of your income."
    else:
        status = "✅ Your spending is under control."

    return total_spent, percentage, status, category_breakdown