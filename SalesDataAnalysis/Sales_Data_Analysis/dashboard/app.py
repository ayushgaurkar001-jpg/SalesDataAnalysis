"""
app.py — Streamlit Sales Analysis Dashboard
Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# --- Page config ---
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS styling ---
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card h3 { margin:0; font-size:0.85rem; opacity:0.8; text-transform:uppercase; letter-spacing:1px; }
    .metric-card h2 { margin:0.3rem 0 0; font-size:1.6rem; font-weight:700; }
    .section-header { font-size:1.2rem; font-weight:600; color:#1e3a5f; margin:1.5rem 0 0.5rem; border-bottom:2px solid #e0e7ef; padding-bottom:0.3rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    # Try loading cleaned data first, fallback to raw, then generate
    for path in ["data/cleaned_sales_data.csv", "data/sales_data.csv"]:
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["OrderDate"])
            if "Month" not in df.columns:
                df["Month"] = df["OrderDate"].dt.month
                df["Year"] = df["OrderDate"].dt.year
                df["Quarter"] = df["OrderDate"].dt.quarter
                df["ProfitMargin"] = (df["Profit"] / df["Sales"] * 100).round(2)
            return df
    # Auto-generate if missing
    st.warning("Data not found — generating sample dataset...")
    sys.path.insert(0, "scripts")
    from generate_data import generate_sales_data
    from clean_data import clean_sales_data
    generate_sales_data()
    return clean_sales_data()


df_full = load_data()

# ─── SIDEBAR ──────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/bar-chart.png", width=60)
st.sidebar.title("📊 Sales Analytics")
st.sidebar.markdown("---")

years = sorted(df_full["Year"].unique())
sel_years = st.sidebar.multiselect("📅 Year", years, default=years)

regions = sorted(df_full["Region"].unique())
sel_regions = st.sidebar.multiselect("🌍 Region", regions, default=regions)

categories = sorted(df_full["Category"].unique())
sel_cats = st.sidebar.multiselect("📦 Category", categories, default=categories)

st.sidebar.markdown("---")
st.sidebar.caption("Sales Data Analysis Project\n\nBuilt with Python + Streamlit")

# --- Filter ---
df = df_full[
    df_full["Year"].isin(sel_years) &
    df_full["Region"].isin(sel_regions) &
    df_full["Category"].isin(sel_cats)
]

# ─── HEADER ───────────────────────────────────────────────
st.title("📊 Sales Data Analysis Dashboard")
st.caption(f"Showing {len(df):,} orders · Filters applied: Year={sel_years}, Region={sel_regions}, Category={sel_cats}")

# ─── KPI CARDS ────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

def kpi(col, icon, label, value):
    col.markdown(f"""
    <div class="metric-card">
        <h3>{icon} {label}</h3>
        <h2>{value}</h2>
    </div>""", unsafe_allow_html=True)

kpi(k1, "💰", "Total Sales",    f"${df['Sales'].sum():,.0f}")
kpi(k2, "📈", "Total Profit",   f"${df['Profit'].sum():,.0f}")
kpi(k3, "🛒", "Total Orders",   f"{df['OrderID'].nunique():,}")
kpi(k4, "👥", "Customers",      f"{df['CustomerID'].nunique():,}")

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 1: Sales Trend + Category Breakdown ──────────────
st.markdown('<div class="section-header">📅 Sales & Revenue Trends</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    monthly = df.groupby(df["OrderDate"].dt.to_period("M").astype(str))["Sales"].sum().reset_index()
    monthly.columns = ["Month", "Sales"]
    fig = px.area(monthly, x="Month", y="Sales", title="Monthly Sales Trend",
                  color_discrete_sequence=["#2d5986"],
                  labels={"Sales": "Revenue ($)"})
    fig.update_traces(fill="tozeroy", line_color="#2d5986")
    fig.update_layout(showlegend=False, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    cat_data = df.groupby("Category")["Sales"].sum().reset_index()
    fig = px.pie(cat_data, names="Category", values="Sales", title="Sales by Category",
                 color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
    fig.update_layout(margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ─── ROW 2: Region + Sub-Category ─────────────────────────
st.markdown('<div class="section-header">🌍 Regional & Sub-Category Performance</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    reg = df.groupby("Region")[["Sales","Profit"]].sum().reset_index()
    fig = go.Figure()
    fig.add_bar(x=reg["Region"], y=reg["Sales"], name="Sales", marker_color="#4C72B0")
    fig.add_bar(x=reg["Region"], y=reg["Profit"], name="Profit", marker_color="#55A868")
    fig.update_layout(title="Region: Sales vs Profit", barmode="group",
                      legend=dict(orientation="h"), margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    sub = df.groupby("SubCategory")["Sales"].sum().nlargest(8).reset_index()
    fig = px.bar(sub, x="Sales", y="SubCategory", orientation="h",
                 title="Top Sub-Categories", color="Sales",
                 color_continuous_scale="Blues", labels={"Sales": "Revenue ($)"})
    fig.update_layout(showlegend=False, margin=dict(t=40, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ─── ROW 3: Top Products + Top Customers ──────────────────
st.markdown('<div class="section-header">🏆 Top Performers</div>', unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    top_prod = df.groupby("ProductName")["Sales"].sum().nlargest(10).reset_index()
    fig = px.bar(top_prod, x="Sales", y="ProductName", orientation="h",
                 title="Top 10 Products by Revenue",
                 color="Sales", color_continuous_scale="Blues_r")
    fig.update_layout(margin=dict(t=40, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    top_cust = df.groupby("CustomerName")["Sales"].sum().nlargest(10).reset_index()
    fig = px.bar(top_cust, x="Sales", y="CustomerName", orientation="h",
                 title="Top 10 Customers by Spending",
                 color="Sales", color_continuous_scale="Oranges_r")
    fig.update_layout(margin=dict(t=40, b=20), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ─── ROW 4: Profit Margin + Yearly ────────────────────────
st.markdown('<div class="section-header">💹 Profit & Growth Analysis</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)

with col7:
    pm = df.groupby("Category")["ProfitMargin"].mean().reset_index()
    pm.columns = ["Category", "AvgMargin"]
    colors = ["#55A868" if v >= 0 else "#C44E52" for v in pm["AvgMargin"]]
    fig = go.Figure(go.Bar(x=pm["Category"], y=pm["AvgMargin"],
                           marker_color=colors, text=pm["AvgMargin"].round(1),
                           texttemplate="%{text}%", textposition="outside"))
    fig.update_layout(title="Avg Profit Margin by Category (%)",
                      yaxis_title="Margin (%)", margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col8:
    yr = df.groupby("Year")[["Sales","Profit"]].sum().reset_index()
    fig = go.Figure()
    fig.add_bar(x=yr["Year"].astype(str), y=yr["Sales"], name="Sales", marker_color="#4C72B0")
    fig.add_bar(x=yr["Year"].astype(str), y=yr["Profit"], name="Profit", marker_color="#55A868")
    fig.update_layout(title="Yearly Sales & Profit", barmode="group",
                      legend=dict(orientation="h"), margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ─── HEATMAP ──────────────────────────────────────────────
st.markdown('<div class="section-header">🗓️ Monthly Revenue Heatmap</div>', unsafe_allow_html=True)
pivot = df.pivot_table(values="Sales", index="Year", columns="Month", aggfunc="sum").fillna(0)
pivot.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][:len(pivot.columns)]
fig = px.imshow(pivot, text_auto=".0f", color_continuous_scale="YlOrRd",
                title="Revenue Heatmap by Year & Month",
                labels={"color": "Sales ($)"})
fig.update_layout(margin=dict(t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

# ─── RAW DATA TABLE ───────────────────────────────────────
with st.expander("🔍 View Raw Data"):
    st.dataframe(df.head(500), use_container_width=True)
    st.caption(f"Showing first 500 of {len(df):,} rows")
