"""Fetch, validate, and cache daily US-stock data from Alpha Vantage."""

from pathlib import Path
import json

import pandas as pd
import requests

from config import SETTINGS


def get_daily_prices(api_key: str, ticker: str = SETTINGS.ticker) -> pd.DataFrame:
    """Request daily data, validate Alpha Vantage's response, and return oldest first."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": SETTINGS.history_output_size,
        "apikey": api_key,
    }
    response = requests.get(SETTINGS.api_url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if "Error Message" in payload:
        raise ValueError(f"API rejected ticker {ticker}: {payload['Error Message']}")
    if "Note" in payload or "Information" in payload:
        message = payload.get("Note", payload.get("Information"))
        raise RuntimeError(f"API limit or service message: {message}")

    raw_prices = payload.get("Time Series (Daily)")
    if not raw_prices:
        raise ValueError("The API response did not include daily prices.")

    rows = [{"date": date, "close": values["4. close"]} for date, values in raw_prices.items()]
    prices = pd.DataFrame(rows)
    prices["date"] = pd.to_datetime(prices["date"])
    prices["close"] = pd.to_numeric(prices["close"])
    return prices.sort_values("date").set_index("date")


def cache_prices(prices: pd.DataFrame, ticker: str = SETTINGS.ticker) -> Path:
    """Save exactly what the model used, which makes each run reproducible."""
    folder = Path("data")
    folder.mkdir(exist_ok=True)
    path = folder / f"{ticker.lower()}_daily.csv"
    prices.to_csv(path)
    return path


def save_run_metadata(ticker: str, price_rows: int) -> Path:
    folder = Path("data")
    folder.mkdir(exist_ok=True)
    path = folder / "last_run.json"
    path.write_text(json.dumps({"ticker": ticker, "price_rows": price_rows}, indent=2))
    return path
