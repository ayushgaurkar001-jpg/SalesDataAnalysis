# 📊 Sales Data Analysis Project

A complete end-to-end data analytics project built with Python, Pandas, Matplotlib, Seaborn, and Streamlit.

## 🚀 Quick Start (3 steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run full pipeline
python main.py

# 3. Launch dashboard
streamlit run dashboard/app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
Sales_Data_Analysis/
├── data/                        # CSV datasets (auto-generated)
├── sql/queries.sql              # MySQL queries
├── scripts/
│   ├── generate_data.py         # Generates 10,000 sample records
│   ├── clean_data.py            # Data cleaning & feature engineering
│   ├── eda_visualizations.py    # 10 Matplotlib/Seaborn charts
│   └── generate_insights.py     # 15 business insights report
├── dashboard/app.py             # Streamlit interactive dashboard
├── visualizations/              # Saved charts (PNG)
├── reports/insights_report.txt  # Auto-generated business report
├── main.py                      # One-click full pipeline runner
├── requirements.txt
└── README.md
```

---

## 📊 Features

- **Data Generation**: Realistic 10,000-record retail dataset with seasonal patterns
- **Data Cleaning**: Duplicate removal, missing value handling, outlier detection
- **Feature Engineering**: Month, Year, Quarter, Profit Margin, Revenue Per Unit
- **10 Visualizations**: Trend lines, heatmaps, bar charts, correlation matrix
- **Interactive Dashboard**: KPI cards, filters by year/region/category
- **15 Business Insights**: Automated report with actionable recommendations
- **SQL Scripts**: Full MySQL schema + 10 analytical queries

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Core language |
| Pandas / NumPy | Data manipulation |
| Matplotlib / Seaborn | Static visualizations |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |
| Faker | Sample data generation |
| MySQL (optional) | Database backend |

---

## 💼 Portfolio Notes

This project demonstrates:
- End-to-end data pipeline design
- EDA and statistical analysis
- Dashboard development
- Business communication of insights
- Clean, modular, documented Python code

Built for CS student portfolio and placement interviews.
