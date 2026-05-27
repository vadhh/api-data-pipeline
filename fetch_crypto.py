# fetch_crypto.py

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
