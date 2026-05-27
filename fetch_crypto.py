# fetch_crypto.py

import time
import sys
import requests
import os
from datetime import date
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, numbers

HEADERS = [
    "Rank",
    "Name",
    "Symbol",
    "Current Price (USD)",
    "24h Change %",
    "7d Change %",
    "Market Cap",
    "24h Volume",
    "Circulating Supply",
    "Volatility",
]


def derive_volatility(change_24h):
    if change_24h is None:
        return "NORMAL"
    return "HIGH" if abs(change_24h) > 10 else "NORMAL"


def transform_coin(raw):
    change_24h = raw.get("price_change_percentage_24h")
    return {
        "Rank": raw.get("market_cap_rank"),
        "Name": raw.get("name"),
        "Symbol": raw.get("symbol", "").upper() if raw.get("symbol") is not None else "",
        "Current Price (USD)": raw.get("current_price"),
        "24h Change %": change_24h,
        "7d Change %": raw.get("price_change_percentage_7d_in_currency"),
        "Market Cap": raw.get("market_cap"),
        "24h Volume": raw.get("total_volume"),
        "Circulating Supply": raw.get("circulating_supply"),
        "Volatility": derive_volatility(change_24h),
    }


COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS_BASE = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "sparkline": "false",
    "price_change_percentage": "7d",
}


def fetch_page(page, max_retries=3):
    params = {**PARAMS_BASE, "page": page}
    for attempt in range(max_retries):
        try:
            resp = requests.get(COINGECKO_URL, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            wait = 2 ** (attempt + 1)
            print(f"  Retry {attempt + 1}/{max_retries} for page {page} "
                  f"(waiting {wait}s): {e}")
            time.sleep(wait)
    return None


def fetch_all_coins():
    all_coins = []
    for page in range(1, 4):
        print(f"Fetching page {page}/3...")
        data = fetch_page(page)
        if data is None:
            print(f"ERROR: Failed to fetch page {page} after retries. Aborting.")
            sys.exit(1)
        all_coins.extend(data)
        if page < 3:
            time.sleep(2)
    print(f"Fetched {len(all_coins)} coins.")
    return [transform_coin(c) for c in all_coins]


def get_sheet_name(wb, base_name):
    if base_name not in wb.sheetnames:
        return base_name
    counter = 2
    while f"{base_name}_{counter}" in wb.sheetnames:
        counter += 1
    return f"{base_name}_{counter}"


def write_to_excel(rows, filepath, sheet_date=None):
    if sheet_date is None:
        sheet_date = date.today().isoformat()

    if os.path.exists(filepath):
        wb = load_workbook(filepath)
    else:
        wb = Workbook()
        if "Sheet" in wb.sheetnames:
            del wb["Sheet"]

    sheet_name = get_sheet_name(wb, sheet_date)
    ws = wb.create_sheet(title=sheet_name)

    bold = Font(bold=True)
    for col_idx, header in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = bold

    for row_idx, coin in enumerate(rows, 2):
        for col_idx, header in enumerate(HEADERS, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=coin.get(header))

    col_widths = {
        "Rank": 6,
        "Name": 22,
        "Symbol": 8,
        "Current Price (USD)": 20,
        "24h Change %": 14,
        "7d Change %": 14,
        "Market Cap": 18,
        "24h Volume": 16,
        "Circulating Supply": 20,
        "Volatility": 12,
    }
    for col_idx, header in enumerate(HEADERS, 1):
        col_letter = ws.cell(row=1, column=col_idx).column_letter
        ws.column_dimensions[col_letter].width = col_widths.get(header, 14)

    ws.freeze_panes = "A2"

    wb.save(filepath)
    wb.close()
    print(f"Saved sheet '{sheet_name}' to {filepath}")

