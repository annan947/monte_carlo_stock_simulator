from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    ticker: str = "AAPL"
    api_url: str = "https://www.alphavantage.co/query"
    history_output_size: str = "compact"
    forecast_days: int = 126  # approximately six months of trading days
    simulations: int = 5_000
    random_seed: int = 42


SETTINGS = Settings()
