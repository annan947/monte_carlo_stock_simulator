"""API-powered Monte Carlo simulator for education; it never makes trades."""

import os
from pathlib import Path

from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np

from config import SETTINGS
from market_data import cache_prices, get_daily_prices, save_run_metadata
from simulation import calculate_parameters, run_simulation, summarize


def plot_paths(paths: np.ndarray) -> Path:
    output = Path("output")
    output.mkdir(exist_ok=True)
    chart_path = output / "simulation_paths.png"
    plt.figure(figsize=(11, 6))
    plt.plot(paths[:, :100], alpha=0.18, linewidth=0.8)
    plt.plot(paths.mean(axis=1), color="black", linewidth=2, label="Mean of all paths")
    plt.title(f"{SETTINGS.ticker}: {SETTINGS.simulations:,} simulated paths")
    plt.xlabel("Trading days into the future")
    plt.ylabel("Simulated price ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    return chart_path


def main() -> None:
    load_dotenv()
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key or api_key == "paste_your_key_here":
        raise ValueError("Add your Alpha Vantage key to a .env file before running the project.")

    prices = get_daily_prices(api_key)
    cache_path = cache_prices(prices)
    save_run_metadata(SETTINGS.ticker, len(prices))
    drift, volatility, start_price = calculate_parameters(prices)
    paths = run_simulation(start_price, drift, volatility, SETTINGS.forecast_days, SETTINGS.simulations, SETTINGS.random_seed)
    results = summarize(paths, start_price)
    chart_path = plot_paths(paths)

    print(f"\n{SETTINGS.ticker} Monte Carlo simulator")
    print(f"Historical rows fetched from API: {len(prices)}")
    print(f"Latest closing price: ${start_price:,.2f}")
    print(f"Estimated daily volatility: {volatility * 100:.2f}%")
    print(f"\nSix-month simulated final-price range (5th–95th percentile): ${results['p5']:,.2f}–${results['p95']:,.2f}")
    print(f"Median final price: ${results['median']:,.2f}")
    print(f"Chance of finishing above the starting price: {results['probability_profit']:.1f}%")
    print(f"Chance of gaining 10% or more: {results['probability_up_10']:.1f}%")
    print(f"Chance of losing 10% or more: {results['probability_down_10']:.1f}%")
    print(f"\nCached data: {cache_path}\nChart: {chart_path}")


if __name__ == "__main__":
    main()
