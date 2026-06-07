"""
main.py — Run the full Sales Data Analysis pipeline.
Usage:  python main.py
Then:   streamlit run dashboard/app.py
"""

import subprocess
import sys
import os

def run(script, label):
    print(f"\n{'─'*50}")
    print(f"▶  {label}")
    print(f"{'─'*50}")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"❌  {label} failed — check output above.")
        sys.exit(1)
    print(f"✅  {label} complete.")

def main():
    print("=" * 50)
    print("  SALES DATA ANALYSIS — Full Pipeline Runner")
    print("=" * 50)

    os.makedirs("data", exist_ok=True)
    os.makedirs("visualizations", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    run("scripts/generate_data.py",      "Phase 1 — Generate Dataset")
    run("scripts/clean_data.py",         "Phase 2 — Clean Data")
    run("scripts/eda_visualizations.py", "Phase 3 — EDA & Visualizations")
    run("scripts/generate_insights.py",  "Phase 4 — Business Insights")

    print("\n" + "="*50)
    print("  ✅  ALL PHASES COMPLETE!")
    print("="*50)
    print("\nFiles created:")
    print("  📁 data/cleaned_sales_data.csv")
    print("  📁 visualizations/*.png  (10 charts)")
    print("  📁 reports/insights_report.txt")
    print("\n🚀  Launch dashboard:")
    print("     streamlit run dashboard/app.py")
    print()

if __name__ == "__main__":
    main()
