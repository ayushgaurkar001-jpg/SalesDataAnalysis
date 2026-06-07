"""
clean_data.py
Loads raw CSV, cleans it, engineers features, and saves cleaned version.
No database required — works purely from CSV.
"""

import pandas as pd
import numpy as np
import os

def clean_sales_data(input_path="data/sales_data.csv",
                     output_path="data/cleaned_sales_data.csv"):

    print("📂 Loading raw data...")
    df = pd.read_csv(input_path)
    print(f"   Loaded {len(df)} rows, {len(df.columns)} columns")

    # --- 1. Remove duplicates ---
    before = len(df)
    df.drop_duplicates(subset=["OrderID"], inplace=True)
    print(f"   Removed {before - len(df)} duplicate rows")

    # --- 2. Handle missing values ---
    df["Sales"].fillna(df["Sales"].median(), inplace=True)
    df["Profit"].fillna(0, inplace=True)
    df["Quantity"].fillna(1, inplace=True)
    df.dropna(subset=["OrderDate", "CustomerID", "Category"], inplace=True)
    print(f"   Missing values handled")

    # --- 3. Convert data types ---
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["Sales"] = df["Sales"].astype(float).round(2)
    df["Profit"] = df["Profit"].astype(float).round(2)
    df["Quantity"] = df["Quantity"].astype(int)
    print("   Data types converted")

    # --- 4. Feature engineering ---
    df["Month"] = df["OrderDate"].dt.month
    df["MonthName"] = df["OrderDate"].dt.strftime("%b")
    df["Year"] = df["OrderDate"].dt.year
    df["Quarter"] = df["OrderDate"].dt.quarter
    df["DayOfWeek"] = df["OrderDate"].dt.day_name()
    df["ProfitMargin"] = np.where(
        df["Sales"] != 0,
        (df["Profit"] / df["Sales"] * 100).round(2),
        0
    )
    df["RevenuePerUnit"] = (df["Sales"] / df["Quantity"]).round(2)
    print("   Feature engineering done: Month, Year, Quarter, ProfitMargin, RevenuePerUnit")

    # --- 5. Outlier detection (IQR method on Sales) ---
    Q1 = df["Sales"].quantile(0.01)
    Q3 = df["Sales"].quantile(0.99)
    IQR = Q3 - Q1
    before_outlier = len(df)
    df = df[(df["Sales"] >= Q1 - 1.5 * IQR) & (df["Sales"] <= Q3 + 1.5 * IQR)]
    print(f"   Removed {before_outlier - len(df)} outlier rows from Sales")

    # --- 6. Save ---
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Cleaned data saved → {output_path}")
    print(f"   Final shape: {df.shape}")
    print(f"\n📊 Summary:")
    print(f"   Total Sales:  ${df['Sales'].sum():,.2f}")
    print(f"   Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"   Date Range:   {df['OrderDate'].min().date()} → {df['OrderDate'].max().date()}")
    return df


if __name__ == "__main__":
    clean_sales_data()
