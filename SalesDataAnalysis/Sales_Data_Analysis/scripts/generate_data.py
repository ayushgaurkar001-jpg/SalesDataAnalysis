"""
generate_data.py
Generates a realistic retail sales dataset with 10,000 records.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

np.random.seed(42)
random.seed(42)

# --- Configuration ---
N_RECORDS = 10000
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2023, 12, 31)

CATEGORIES = {
    "Furniture": {
        "sub": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "products": ["Executive Chair", "Standing Desk", "Bookcase Pro", "Filing Cabinet",
                     "Lounge Chair", "Coffee Table", "Office Desk", "Storage Unit"]
    },
    "Technology": {
        "sub": ["Phones", "Laptops", "Accessories", "Printers"],
        "products": ["iPhone 14", "MacBook Pro", "USB Hub", "Wireless Mouse",
                     "HP LaserJet", "Samsung Galaxy", "Dell XPS", "Mechanical Keyboard"]
    },
    "Office Supplies": {
        "sub": ["Paper", "Pens", "Binders", "Storage", "Labels"],
        "products": ["A4 Paper Ream", "Ballpoint Pens Set", "3-Ring Binder", "Stapler Pro",
                     "Sticky Notes Pack", "File Folders", "Tape Dispenser", "Scissors Set"]
    }
}

REGIONS = {
    "East": ["New York", "Massachusetts", "Pennsylvania", "New Jersey", "Connecticut"],
    "West": ["California", "Washington", "Oregon", "Nevada", "Arizona"],
    "South": ["Texas", "Florida", "Georgia", "North Carolina", "Virginia"],
    "North": ["Illinois", "Michigan", "Ohio", "Minnesota", "Wisconsin"]
}

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
               "William", "Barbara", "David", "Susan", "Richard", "Jessica", "Joseph", "Sarah",
               "Thomas", "Karen", "Charles", "Lisa", "Christopher", "Nancy", "Daniel", "Betty"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris"]


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_sales_data(n=N_RECORDS):
    rows = []
    customer_pool = [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(300)]
    customer_ids = {name: f"CUST-{1000 + i}" for i, name in enumerate(set(customer_pool))}

    for i in range(n):
        cat = random.choice(list(CATEGORIES.keys()))
        sub = random.choice(CATEGORIES[cat]["sub"])
        product = random.choice(CATEGORIES[cat]["products"])
        region = random.choice(list(REGIONS.keys()))
        state = random.choice(REGIONS[region])
        customer_name = random.choice(customer_pool)
        customer_id = customer_ids[customer_name]

        # Seasonal boost: Q4 sells more
        order_date = random_date(START_DATE, END_DATE)
        if order_date.month in [11, 12]:
            sales_multiplier = random.uniform(1.2, 2.0)
        elif order_date.month in [6, 7, 8]:
            sales_multiplier = random.uniform(0.8, 1.3)
        else:
            sales_multiplier = 1.0

        base_price = {
            "Furniture": random.uniform(50, 1500),
            "Technology": random.uniform(30, 2500),
            "Office Supplies": random.uniform(5, 200)
        }[cat]

        quantity = random.randint(1, 10)
        sales = round(base_price * sales_multiplier, 2)
        # Profit margin varies by category
        margin = {
            "Furniture": random.uniform(-0.05, 0.35),
            "Technology": random.uniform(-0.10, 0.25),
            "Office Supplies": random.uniform(0.05, 0.45)
        }[cat]
        profit = round(sales * margin, 2)

        rows.append({
            "OrderID": f"ORD-{10000 + i}",
            "OrderDate": order_date.strftime("%Y-%m-%d"),
            "CustomerID": customer_id,
            "CustomerName": customer_name,
            "ProductName": f"{product} {random.choice(['V1','V2','Pro','Plus','Elite','Standard'])}",
            "Category": cat,
            "SubCategory": sub,
            "Quantity": quantity,
            "Sales": sales,
            "Profit": profit,
            "Region": region,
            "State": state
        })

    df = pd.DataFrame(rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/sales_data.csv", index=False)
    print(f"✅ Dataset generated with {len(df)} records → data/sales_data.csv")
    return df


if __name__ == "__main__":
    generate_sales_data()
