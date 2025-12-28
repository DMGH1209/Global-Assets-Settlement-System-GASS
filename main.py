"""
Project: Global Assets Settlement System (GASS)
Author: Daniel Godoy
GitHub: https://github.com/DxGodoy-dev
Repository: https://github.com/DxGodoy-dev/Global-Assets-Settlement-System-GASS
Version: 1.0
Description: Financial asset settlement system with real-time BCV rate integration.
"""

import pandas as pd
from pyBCV import Currency
import sys
from pathlib import Path

# --- CONFIGURATION & PATHS ---
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "history_reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- FINANCIAL CONSTANTS ---
LIQUIDATION_RATE = 0.75  # Gift Card to USDT conversion
SERVICE_FEE_RATE = 0.10  # Management fee
SPREAD_FACTOR = 1.824    # Market correction factor (USDT-Parallel / BCV)

# --- EXCHANGE RATE (BCV) ---
print("Connecting to Financial Services for BCV rate...")
try:
    currency = Currency()
    bcv_rate = float(currency.get_rate(currency_code="USD", prettify=False))
    print(f"✅ Connection successful. Official Rate: {bcv_rate} VES/USD")
except Exception as e:
    print(f"⚠️ Automatic fetch failed: {e}")
    bcv_rate = float(input("Please enter the official BCV rate manually: "))

# --- PROCESSING LOGIC ---
def get_stats(df_series):
    """Aggregates tasks by asset value."""
    counts = df_series.value_counts().to_list()
    types = df_series.value_counts().index.to_list()
    return counts, types

def process_type_1(counts, types, print_func):
    """Processes Type 1 Assets (Scale: 100 points = 1 USD)."""
    t_points = 0
    t_tasks = 0
    for c, t in zip(counts, types):
        subtotal = t * c
        if print_func: print_func(f"{t:g} PTS: {c:g} units ---> Subtotal: {subtotal:g} points")
        t_points += subtotal
        t_tasks += c
    
    total_usd = t_points / 100 
    if print_func:
        print_func(f"\nTOTAL TYPE 1: {t_points:g} PTS ---> {total_usd:.2f} $")
        print_func(f"TOTAL TASKS: {t_tasks:g}\n")
    return total_usd

def process_type_2(counts, types, print_func):
    """Processes Type 2 Assets (Direct USD valuation)."""
    total_usd = 0
    t_tasks = 0
    for c, t in zip(counts, types):
        subtotal = t * c
        if print_func: print_func(f"{t:g} $: {c:g} units ---> Subtotal: {subtotal:g} $")
        total_usd += subtotal
        t_tasks += c
    
    if print_func:
        print_func(f"\nTOTAL TYPE 2: {total_usd:.2f} $")
        print_func(f"TOTAL TASKS: {t_tasks:g}\n")
    return total_usd

# --- DATA SELECTION ---
DATA_DIR = BASE_DIR / "data"
if not DATA_DIR.exists():
    print(f"❌ Error: Data directory not found.")
    sys.exit()

files = [f.name for f in DATA_DIR.glob("*.xlsx")]
if not files:
    print(f"❌ Error: No datasets found in {DATA_DIR}")
    sys.exit()

print("\n--- Available Accounts for Settlement ---")
for i, filename in enumerate(files, 1):
    print(f"{i}. {filename}")

try:
    choice = int(input("\nSelect account number to process: ")) 
    selected_file = files[choice - 1]
    account_id = selected_file.replace(".xlsx", "").upper() 
    excel_path = DATA_DIR / selected_file
except:
    print("❌ Invalid selection.")
    sys.exit()

# --- LOAD & CLEAN DATA ---
try:
    df = pd.read_excel(excel_path)
    df["date"] = pd.to_datetime(df["date"])
except Exception as e:
    print(f"❌ Loading error: {e}")
    sys.exit()

ignored_entries = ["Punchcard", "Weekly Badge Bonus", "Bonus Welcome Survey"]
df_clean = df[~df.description.isin(ignored_entries)].copy().reset_index(drop=True)

start_date = pd.to_datetime(input("Settlement Start Date (YYYY-MM-DD): "))
end_date = pd.to_datetime(input("Settlement End Date (YYYY-MM-DD): "))

df_filtered = df_clean[(df_clean["date"] >= start_date) & (df_clean["date"] <= end_date)]
df_t1 = df_filtered[df_filtered.platform == "Digital_Assets_Type_1"].copy().sort_values('date')
df_t2 = df_filtered[df_filtered.platform == "Digital_Assets_Type_2"].copy().sort_values('date')

def get_unique_dates(target_df):
    if target_df.empty: return []
    return target_df["date"].value_counts().index.sort_values().to_list()

# --- AUDIT REPORT GENERATION ---
report_name = f"Settlement_{account_id}_{start_date.date()}.txt"
report_path = OUTPUT_DIR / report_name

with open(report_path, "w", encoding="utf-8") as report_file:
    def smart_print(text=""):
        print(text); report_file.write(text + "\n")

    smart_print("========================================")
    smart_print("       GLOBAL ASSETS SETTLEMENT")
    smart_print(f"       ACCOUNT ID: {account_id}")
    smart_print(f"       PERIOD: {start_date.date()} TO {end_date.date()}")
    smart_print("========================================\n")

    smart_print(">>> PROVIDER: DIGITAL ASSETS TYPE 1 (POINTS)")
    for d in get_unique_dates(df_t1):
        smart_print(f"----------------------------------------\nDATE: {d.date()}")
        c, t = get_stats(df_t1[df_t1.date == d]["amount"])
        process_type_1(c, t, smart_print)

    smart_print("\n>>> PROVIDER: DIGITAL ASSETS TYPE 2 (DIRECT USD)")
    for d in get_unique_dates(df_t2):
        smart_print(f"----------------------------------------\nDATE: {d.date()}")
        c, t = get_stats(df_t2[df_t2.date == d]["amount"])
        process_type_2(c, t, smart_print)

    # --- FINAL CALCULATIONS ---
    total_val_t1 = process_type_1(*get_stats(df_t1["amount"]), None) if not df_t1.empty else 0
    total_val_t2 = process_type_2(*get_stats(df_t2["amount"]), None) if not df_t2.empty else 0
    total_raw_usd = total_val_t1 + total_val_t2
    
    # 1. Market Liquidation (Gift Cards to USDT)
    total_usdt = total_raw_usd * LIQUIDATION_RATE
    
    # 2. Commission & Payout (USDT)
    comm_usdt = total_usdt * SERVICE_FEE_RATE
    owner_usdt = total_usdt - comm_usdt
    
    # 3. Final Settlement (VES) using Spread Factor
    market_rate = bcv_rate * SPREAD_FACTOR
    comm_ves = comm_usdt * market_rate
    owner_ves = owner_usdt * market_rate

    # 4. Purchasing Power (VES to Official USD)
    # Most stores use BCV rate for pricing
    comm_purchasing_usd = comm_ves / bcv_rate
    owner_purchasing_usd = owner_ves / bcv_rate

    smart_print("========================================")
    smart_print("           FINANCIAL SUMMARY")
    smart_print("========================================")
    smart_print(f"RAW ASSETS TOTAL:      {total_raw_usd:.2f} $")
    smart_print(f"LIQUIDATED (USDT):     {total_usdt:.2f} USDT")
    smart_print(f"MARKET RATE APPLIED:   {market_rate:.2f} VES/USDT")
    smart_print("----------------------------------------")
    smart_print(f"YOUR FEE (10%):        {comm_ves:.2f} VES ({comm_purchasing_usd:.2f} $ BCV)")
    smart_print(f"OWNER PAYOUT:          {owner_ves:.2f} VES ({owner_purchasing_usd:.2f} $ BCV)")
    smart_print(f"OFFICIAL BCV RATE:     {bcv_rate:.2f} VES")
    smart_print("========================================\n")

print(f"\n✅ Report saved at:\n./history_reports/{report_name}")