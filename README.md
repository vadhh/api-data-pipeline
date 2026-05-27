# Crypto Data Pipeline

Fetches the top 250 cryptocurrencies by market cap from CoinGecko and saves them to an Excel file. Each run adds a new date-stamped sheet so you can track changes over time.

## What You Get

An Excel file (`crypto_data.xlsx`) with one sheet per day containing:

| Column | Description |
|---|---|
| Rank | Market cap ranking |
| Name | Coin name (e.g., Bitcoin) |
| Symbol | Ticker symbol (e.g., BTC) |
| Current Price (USD) | Price in US dollars |
| 24h Change % | Price change in the last 24 hours |
| 7d Change % | Price change in the last 7 days |
| Market Cap | Total market capitalization |
| 24h Volume | Trading volume in the last 24 hours |
| Circulating Supply | Number of coins in circulation |
| Volatility | HIGH if 24h change exceeds 10%, otherwise NORMAL |

## Setup (One-Time)

### 1. Install Python

- **Windows:** Download from https://www.python.org/downloads/ — check "Add Python to PATH" during install
- **Mac:** Run `brew install python3` (or download from python.org)
- **Linux:** Run `sudo apt install python3 python3-pip python3-venv`

Verify: open a terminal and run:
```
python --version
```
(On Mac/Linux you may need `python3 --version`)

### 2. Set Up Virtual Environment & Install Dependencies

Open a terminal in this folder and run:

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Daily Usage

Open a terminal in this folder, activate the virtual environment, and run:

**Mac/Linux:**
```bash
source .venv/bin/activate
python fetch_crypto.py
```

**Windows:**
```cmd
.venv\Scripts\activate
python fetch_crypto.py
```

The script takes about 10 seconds. You'll see progress messages. When it says "Done!", open `crypto_data.xlsx` to see the data.

If you run it more than once in the same day, each run gets its own sheet (e.g., `2026-05-27`, `2026-05-27_2`).

## Automate It (Optional)

### Mac/Linux (cron)

Run `crontab -e` and add this line to run daily at 9 AM (replace `/path/to/api-data-pipeline` with the actual folder path):
```
0 9 * * * cd /path/to/api-data-pipeline && .venv/bin/python fetch_crypto.py
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name: "Crypto Data Fetch"
4. Trigger: Daily, at your preferred time
5. Action: Start a program
6. Program: `C:\path\to\api-data-pipeline\.venv\Scripts\python.exe`
7. Arguments: `fetch_crypto.py`
8. Start in: the folder path (e.g., `C:\path\to\api-data-pipeline`)

## Troubleshooting

| Problem | Solution |
|---|---|
| `python: command not found` | Try `python3` instead, or reinstall Python with "Add to PATH" checked |
| `ModuleNotFoundError: No module named 'requests'` | Make sure you activated the virtual environment (`.venv`) first |
| `ConnectionError` or timeout | Check your internet connection and try again — the script retries automatically |
| Excel file won't open | Make sure it's not already open in another program |

## No API Key Needed

This uses the CoinGecko free public API. No account or API key required.
