# Crypto Data Pipeline — Design Spec

## Overview

A single Python script that fetches the top 250 cryptocurrencies by market cap from the CoinGecko free API and appends a date-stamped sheet to an Excel workbook. Designed for a non-technical assistant to run daily.

## Project Structure

```
api-data-pipeline/
├── fetch_crypto.py      # Main script — single entry point
├── requirements.txt     # requests, openpyxl
├── README.md            # Step-by-step instructions for assistant
└── crypto_data.xlsx     # Generated on first run, appended daily
```

## Dependencies

- Python 3.8+
- `requests` — HTTP client for CoinGecko API
- `openpyxl` — Excel read/write (supports appending sheets to existing workbooks)

No API key required (CoinGecko free tier).

## API Usage

**Endpoint:** `GET https://api.coingecko.com/api/v3/coins/markets`

**Parameters:**
- `vs_currency=usd`
- `order=market_cap_desc`
- `per_page=100` (max allowed per request)
- `page=1,2,3` (three requests for 250 coins)
- `sparkline=false`
- `price_change_percentage=7d`

**Rate limiting:** 2-second delay between each paginated request.

## Data Flow

1. Make 3 paginated API calls (100 + 100 + 50 coins)
2. Extract relevant fields from each coin object
3. Derive Volatility column: "HIGH" if `abs(24h Change %) > 10` (flags both pumps and dumps), else "NORMAL"
4. Open existing `crypto_data.xlsx` or create new workbook
5. Add sheet named `YYYY-MM-DD` (with `_2`, `_3` suffix if run multiple times per day)
6. Write header row + 250 data rows with formatting
7. Save workbook, print success message

## Column Mapping

| Column              | API Field                               | Format                          |
|---------------------|------------------------------------------|---------------------------------|
| Rank                | `market_cap_rank`                       | Integer                         |
| Name                | `name`                                  | Text                            |
| Symbol              | `symbol`                                | Text, uppercased                |
| Current Price (USD) | `current_price`                         | 2 decimal places, `$` prefix   |
| 24h Change %        | `price_change_percentage_24h`           | 2 decimal places, `%` suffix   |
| 7d Change %         | `price_change_percentage_7d_in_currency`| 2 decimal places, `%` suffix   |
| Market Cap          | `market_cap`                            | Number with comma separators    |
| 24h Volume          | `total_volume`                          | Number with comma separators    |
| Circulating Supply  | `circulating_supply`                    | Number with comma separators    |
| Volatility          | Derived from 24h Change %              | "HIGH" or "NORMAL"              |

## Excel Formatting

- Header row: bold, frozen (stays visible when scrolling)
- Column widths: auto-sized to fit header text
- No charts or conditional coloring

## Error Handling

- Each API call retries up to 3 times with exponential backoff (2s, 4s, 8s)
- On total failure: print clear error to console and exit without touching the Excel file (no partial writes)
- All status/error messages printed to console (no log file)

## Scheduling

Run-once script. The assistant runs it manually each day or configures:
- **macOS/Linux:** cron job
- **Windows:** Task Scheduler

The README covers setup for both platforms.

## Constraints

- No API key needed (CoinGecko free tier)
- Budget: $75 / Deadline: 4 days
- Target audience: non-technical assistant running via terminal
