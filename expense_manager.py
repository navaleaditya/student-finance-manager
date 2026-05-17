import pandas as pd
from datetime import date
import os

FILE = "expenses.csv"

def _ensure_file():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=["date", "category", "amount"])
        df.to_csv(FILE, index=False)

def add_expense(category, amount):
    _ensure_file()
    df = pd.read_csv(FILE)
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    new_row = {
        "date": date.today().isoformat(),
        "category": category,
        "amount": amount
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE, index=False)

def get_all_expenses():
    _ensure_file()
    return pd.read_csv(FILE)

def get_monthly_expenses(year=None, month=None):
    _ensure_file()
    df = pd.read_csv(FILE)
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    today = date.today()
    y = year or today.year
    m = month or today.month
    return df[(df["date"].dt.year == y) & (df["date"].dt.month == m)]

def delete_expense(index):
    _ensure_file()
    df = pd.read_csv(FILE)
    if index < 0 or index >= len(df):
        raise IndexError("Invalid expense index")
    df = df.drop(index=index).reset_index(drop=True)
    df.to_csv(FILE, index=False)