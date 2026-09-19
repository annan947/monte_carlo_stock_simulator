"""Monte Carlo price simulation using Geometric Brownian Motion (GBM)."""

import numpy as np
import pandas as pd


def calculate_parameters(prices: pd.DataFrame) -> tuple[float, float, float]:
    """Estimate daily drift, daily volatility, and the latest closing price."""
    log_returns = np.log(prices["close"] / prices["close"].shift(1)).dropna()
    return float(log_returns.mean()), float(log_returns.std()), float(prices["close"].iloc[-1])


def run_simulation(start_price: float, drift: float, volatility: float, forecast_days: int, simulations: int, seed: int) -> np.ndarray:
    """Return an array shaped (forecast_days + 1, simulations)."""
    rng = np.random.default_rng(seed)
    shocks = rng.normal(0, 1, size=(forecast_days, simulations))
    daily_multipliers = np.exp((drift - 0.5 * volatility**2) + volatility * shocks)
    paths = np.empty((forecast_days + 1, simulations))
    paths[0] = start_price
    paths[1:] = start_price * np.cumprod(daily_multipliers, axis=0)
    return paths


def summarize(paths: np.ndarray, start_price: float) -> dict[str, float]:
    """Create outcomes that a user can understand without reading every path."""
    final_prices = paths[-1]
    return {
        "p5": float(np.percentile(final_prices, 5)),
        "median": float(np.percentile(final_prices, 50)),
        "p95": float(np.percentile(final_prices, 95)),
        "probability_profit": float((final_prices > start_price).mean() * 100),
        "probability_up_10": float((final_prices >= start_price * 1.10).mean() * 100),
        "probability_down_10": float((final_prices <= start_price * 0.90).mean() * 100),
    }
