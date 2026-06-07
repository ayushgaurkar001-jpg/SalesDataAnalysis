"""
generate_insights.py
Generates a business insights report as reports/insights_report.txt
"""

import pandas as pd
import numpy as np
import os

def generate_insights(input_path="data/cleaned_sales_data.csv"):
    print("🔍 Generating business insights...\n")
    df = pd.read_csv(input_path, parse_dates=["OrderDate"])
    os.makedirs("reports", exist_ok=True)

    lines = []
    def h(text): lines.append(f"\n{'='*60}\n{text}\n{'='*60}")
    def p(text): lines.append(text)

    h("SALES DATA ANALYSIS — BUSINESS INSIGHTS REPORT")
    p(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    p(f"Records analysed: {len(df):,}")

    # --- KPIs ---
    h("KEY PERFORMANCE INDICATORS")
    p(f"  Total Revenue  : ${df['Sales'].sum():>12,.2f}")
    p(f"  Total Profit   : ${df['Profit'].sum():>12,.2f}")
    p(f"  Overall Margin : {df['Profit'].sum()/df['Sales'].sum()*100:>11.1f}%")
    p(f"  Total Orders   : {df['OrderID'].nunique():>12,}")
    p(f"  Unique Customers: {df['CustomerID'].nunique():>11,}")
    p(f"  Avg Order Value : ${df['Sales'].mean():>11,.2f}")

    # --- Category ---
    h("INSIGHT 1 — Best Performing Category by Revenue")
    cat_s = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    p(cat_s.apply(lambda x: f"  {cat_s.index[cat_s==x][0]:<20} ${x:>12,.2f}").to_string())

    h("INSIGHT 2 — Most Profitable Category")
    cat_p = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    p(f"  ➤ {cat_p.idxmax()} with ${cat_p.max():,.2f} total profit")

    # --- Region ---
    h("INSIGHT 3 — Top Revenue Region")
    reg_s = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    p(f"  ➤ {reg_s.idxmax()} region leads with ${reg_s.max():,.2f}")

    h("INSIGHT 4 — Most Profitable Region")
    reg_p = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    p(f"  ➤ {reg_p.idxmax()} region with ${reg_p.max():,.2f} profit")
    for r, v in reg_p.items():
        p(f"     {r:<10} ${v:>10,.2f}")

    # --- Seasonality ---
    h("INSIGHT 5 — Peak Sales Month")
    monthly = df.groupby("Month")["Sales"].sum()
    peak_month = monthly.idxmax()
    month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    p(f"  ➤ {month_names[peak_month]} (Month {peak_month}) — ${monthly.max():,.2f}")

    h("INSIGHT 6 — Lowest Sales Month")
    p(f"  ➤ {month_names[monthly.idxmin()]} — ${monthly.min():,.2f}")

    h("INSIGHT 7 — Q4 vs Q1 Sales Comparison")
    q4 = df[df["Quarter"]==4]["Sales"].sum()
    q1 = df[df["Quarter"]==1]["Sales"].sum()
    p(f"  Q4 Sales: ${q4:,.2f}")
    p(f"  Q1 Sales: ${q1:,.2f}")
    p(f"  Q4 is {((q4-q1)/q1*100):.1f}% {'higher' if q4>q1 else 'lower'} than Q1")

    # --- Products ---
    h("INSIGHT 8 — Top 5 Products by Revenue")
    top5 = df.groupby("ProductName")["Sales"].sum().nlargest(5)
    for i, (prod, val) in enumerate(top5.items(), 1):
        p(f"  {i}. {prod:<35} ${val:>10,.2f}")

    h("INSIGHT 9 — Bottom 5 Products by Revenue")
    bot5 = df.groupby("ProductName")["Sales"].sum().nsmallest(5)
    for i, (prod, val) in enumerate(bot5.items(), 1):
        p(f"  {i}. {prod:<35} ${val:>10,.2f}")

    # --- Customers ---
    h("INSIGHT 10 — Top 5 Customers by Spending")
    top_cust = df.groupby("CustomerName")["Sales"].sum().nlargest(5)
    for i, (name, val) in enumerate(top_cust.items(), 1):
        p(f"  {i}. {name:<30} ${val:>10,.2f}")

    h("INSIGHT 11 — Customer Purchase Frequency")
    freq = df.groupby("CustomerID")["OrderID"].count()
    p(f"  Average orders per customer: {freq.mean():.1f}")
    p(f"  Max orders by one customer:  {freq.max()}")
    p(f"  Customers with 1 order only: {(freq==1).sum()}")

    # --- Sub-Category ---
    h("INSIGHT 12 — Top Sub-Categories")
    sub = df.groupby("SubCategory")["Sales"].sum().nlargest(5)
    for sc, v in sub.items():
        p(f"  {sc:<20} ${v:>10,.2f}")

    # --- Profit Margin ---
    h("INSIGHT 13 — Profit Margin Analysis")
    pm = df.groupby("Category")["ProfitMargin"].mean()
    for cat, m in pm.items():
        p(f"  {cat:<20} {m:.1f}% avg margin")
    neg = df[df["Profit"] < 0]
    p(f"\n  Orders with negative profit: {len(neg):,} ({len(neg)/len(df)*100:.1f}%)")

    # --- Yearly growth ---
    h("INSIGHT 14 — Year-over-Year Growth")
    yr = df.groupby("Year")["Sales"].sum()
    for year, sales in yr.items():
        p(f"  {year}: ${sales:,.2f}")
    if len(yr) >= 2:
        yrs = list(yr.index)
        growth = (yr[yrs[-1]] - yr[yrs[-2]]) / yr[yrs[-2]] * 100
        p(f"\n  YoY Growth ({yrs[-2]}→{yrs[-1]}): {growth:+.1f}%")

    # --- State ---
    h("INSIGHT 15 — Top 5 States by Revenue")
    states = df.groupby("State")["Sales"].sum().nlargest(5)
    for st, v in states.items():
        p(f"  {st:<20} ${v:>10,.2f}")

    # --- Recommendations ---
    h("ACTIONABLE RECOMMENDATIONS")
    best_cat = cat_p.idxmax()
    best_reg = reg_p.idxmax()
    p(f"  1. Double down on {best_cat} — highest profit category.")
    p(f"  2. Invest in {best_reg} region marketing — strongest ROI.")
    p(f"  3. Plan promotions in Q4 (peak season) to maximise revenue.")
    p(f"  4. Review bottom-5 products for discontinuation or repricing.")
    p(f"  5. Re-engage one-time buyers with loyalty programmes.")
    p(f"  6. Reduce negative-margin orders by reviewing discounting policies.")
    p(f"  7. Expand to underperforming regions with targeted campaigns.")

    report = "\n".join(lines)
    out = "reports/insights_report.txt"
    with open(out, "w") as f:
        f.write(report)
    print(report)
    print(f"\n✅ Report saved → {out}")


if __name__ == "__main__":
    generate_insights()
