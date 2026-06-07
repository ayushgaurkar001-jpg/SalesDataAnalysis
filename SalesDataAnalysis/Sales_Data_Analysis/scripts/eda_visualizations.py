"""
eda_visualizations.py
Generates all EDA charts and saves them to the visualizations/ folder.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# --- Setup ---
os.makedirs("visualizations", exist_ok=True)
sns.set_theme(style="darkgrid", palette="muted")
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]
plt.rcParams.update({"figure.dpi": 120, "font.family": "DejaVu Sans"})


def load_data():
    path = "data/cleaned_sales_data.csv"
    if not os.path.exists(path):
        print("⚠️  Cleaned data not found. Run clean_data.py first.")
        raise FileNotFoundError(path)
    df = pd.read_csv(path, parse_dates=["OrderDate"])
    return df


def save(name):
    plt.tight_layout()
    plt.savefig(f"visualizations/{name}.png", bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved: visualizations/{name}.png")


def plot_monthly_sales_trend(df):
    monthly = df.groupby(["Year", "Month"])["Sales"].sum().reset_index()
    monthly["Period"] = pd.to_datetime(monthly[["Year","Month"]].assign(day=1))
    fig, ax = plt.subplots(figsize=(13, 5))
    for yr, grp in monthly.groupby("Year"):
        ax.plot(grp["Period"], grp["Sales"], marker="o", label=str(yr), linewidth=2)
    ax.set_title("Monthly Sales Trend by Year", fontsize=15, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(title="Year")
    save("01_monthly_sales_trend")


def plot_revenue_by_category(df):
    cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(cat["Category"], cat["Sales"], color=PALETTE[:len(cat)], edgecolor="white", linewidth=1.2)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=10)
    ax.set_title("Revenue by Category", fontsize=14, fontweight="bold")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    save("02_revenue_by_category")


def plot_profit_by_category(df):
    cat = df.groupby("Category")["Profit"].sum().sort_values(ascending=False).reset_index()
    colors = ["#55A868" if v >= 0 else "#C44E52" for v in cat["Profit"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(cat["Category"], cat["Profit"], color=colors, edgecolor="white")
    ax.set_title("Profit by Category", fontsize=14, fontweight="bold")
    ax.set_ylabel("Total Profit ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.axhline(0, color="black", linewidth=0.8)
    save("03_profit_by_category")


def plot_region_sales(df):
    reg = df.groupby("Region")[["Sales","Profit"]].sum().reset_index().sort_values("Sales", ascending=False)
    x = np.arange(len(reg))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width/2, reg["Sales"], width, label="Sales", color=PALETTE[0])
    ax.bar(x + width/2, reg["Profit"], width, label="Profit", color=PALETTE[2])
    ax.set_xticks(x)
    ax.set_xticklabels(reg["Region"])
    ax.set_title("Region-wise Sales vs Profit", fontsize=14, fontweight="bold")
    ax.set_ylabel("Amount ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend()
    save("04_region_sales_profit")


def plot_top10_products(df):
    top = df.groupby("ProductName")["Sales"].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top, x="Sales", y="ProductName", palette="Blues_d", ax=ax)
    ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Sales ($)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    save("05_top10_products")


def plot_top10_customers(df):
    top = df.groupby("CustomerName")["Sales"].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top, x="Sales", y="CustomerName", palette="Oranges_d", ax=ax)
    ax.set_title("Top 10 Customers by Spending", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Sales ($)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    save("06_top10_customers")


def plot_monthly_heatmap(df):
    pivot = df.pivot_table(values="Sales", index="Year", columns="Month", aggfunc="sum")
    pivot.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][:len(pivot.columns)]
    fig, ax = plt.subplots(figsize=(13, 4))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax,
                annot_kws={"size": 9}, linewidths=0.5)
    ax.set_title("Monthly Revenue Heatmap ($)", fontsize=14, fontweight="bold")
    save("07_monthly_heatmap")


def plot_correlation_matrix(df):
    num_cols = ["Sales", "Profit", "Quantity", "ProfitMargin", "RevenuePerUnit"]
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap="coolwarm", center=0,
                fmt=".2f", ax=ax, linewidths=0.5)
    ax.set_title("Correlation Matrix", fontsize=14, fontweight="bold")
    save("08_correlation_matrix")


def plot_profit_margin_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df["ProfitMargin"], bins=40, kde=True, ax=axes[0], color=PALETTE[0])
    axes[0].set_title("Profit Margin Distribution", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Profit Margin (%)")
    sns.boxplot(data=df, x="Category", y="ProfitMargin", palette=PALETTE[:3], ax=axes[1])
    axes[1].set_title("Profit Margin by Category", fontsize=12, fontweight="bold")
    save("09_profit_margin_distribution")


def plot_yearly_growth(df):
    yearly = df.groupby("Year")[["Sales","Profit"]].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.35
    x = np.arange(len(yearly))
    ax.bar(x - width/2, yearly["Sales"], width, label="Sales", color=PALETTE[0])
    ax.bar(x + width/2, yearly["Profit"], width, label="Profit", color=PALETTE[2])
    ax.set_xticks(x)
    ax.set_xticklabels(yearly["Year"].astype(str))
    ax.set_title("Yearly Sales & Profit", fontsize=14, fontweight="bold")
    ax.set_ylabel("Amount ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend()
    save("10_yearly_growth")


def run_all():
    print("📊 Generating visualizations...\n")
    df = load_data()
    plot_monthly_sales_trend(df)
    plot_revenue_by_category(df)
    plot_profit_by_category(df)
    plot_region_sales(df)
    plot_top10_products(df)
    plot_top10_customers(df)
    plot_monthly_heatmap(df)
    plot_correlation_matrix(df)
    plot_profit_margin_distribution(df)
    plot_yearly_growth(df)
    print(f"\n✅ All 10 charts saved to visualizations/")


if __name__ == "__main__":
    run_all()
