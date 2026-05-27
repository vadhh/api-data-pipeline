# tests/test_transform.py

from fetch_crypto import transform_coin, derive_volatility


def test_derive_volatility_high_positive():
    assert derive_volatility(15.5) == "HIGH"


def test_derive_volatility_high_negative():
    assert derive_volatility(-12.3) == "HIGH"


def test_derive_volatility_normal():
    assert derive_volatility(5.0) == "NORMAL"


def test_derive_volatility_boundary():
    assert derive_volatility(10.0) == "NORMAL"
    assert derive_volatility(-10.0) == "NORMAL"


def test_derive_volatility_none():
    assert derive_volatility(None) == "NORMAL"


def test_transform_coin_full():
    raw = {
        "market_cap_rank": 1,
        "name": "Bitcoin",
        "symbol": "btc",
        "current_price": 68432.12,
        "price_change_percentage_24h": 2.5,
        "price_change_percentage_7d_in_currency": -1.3,
        "market_cap": 1340000000000,
        "total_volume": 28000000000,
        "circulating_supply": 19700000.0,
    }
    result = transform_coin(raw)
    assert result == {
        "Rank": 1,
        "Name": "Bitcoin",
        "Symbol": "BTC",
        "Current Price (USD)": 68432.12,
        "24h Change %": 2.5,
        "7d Change %": -1.3,
        "Market Cap": 1340000000000,
        "24h Volume": 28000000000,
        "Circulating Supply": 19700000.0,
        "Volatility": "NORMAL",
    }


def test_transform_coin_high_volatility():
    raw = {
        "market_cap_rank": 50,
        "name": "Shiba Inu",
        "symbol": "shib",
        "current_price": 0.0000234,
        "price_change_percentage_24h": -18.7,
        "price_change_percentage_7d_in_currency": 5.2,
        "market_cap": 14000000000,
        "total_volume": 900000000,
        "circulating_supply": 589000000000000.0,
    }
    result = transform_coin(raw)
    assert result["Volatility"] == "HIGH"
    assert result["Symbol"] == "SHIB"


def test_transform_coin_missing_fields():
    raw = {
        "market_cap_rank": None,
        "name": "Unknown",
        "symbol": "unk",
        "current_price": None,
        "price_change_percentage_24h": None,
        "price_change_percentage_7d_in_currency": None,
        "market_cap": None,
        "total_volume": None,
        "circulating_supply": None,
    }
    result = transform_coin(raw)
    assert result["Rank"] is None
    assert result["Current Price (USD)"] is None
    assert result["Volatility"] == "NORMAL"
