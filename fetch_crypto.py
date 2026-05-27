# fetch_crypto.py

import time
import sys
import requests

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
