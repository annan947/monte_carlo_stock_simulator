# API-Powered Monte Carlo Stock Simulator

An educational Python application that fetches historical US-stock data from the Alpha Vantage API and generates **5,000 possible future price paths** using Geometric Brownian Motion (GBM). It does not make trades, connect to a brokerage, or offer investment advice.

## Why this is stronger than a basic script

- Calls an external market-data API with secure API-key configuration
- Validates API errors and rate-limit messages
- Saves a local copy of the exact market data used in each run
- Splits API access, simulation logic, configuration, and charts into separate files
- Uses reproducible simulation settings and reports useful probability metrics

## What it does

1. Fetches daily AAPL prices from Alpha Vantage.
2. Uses historical log returns to estimate drift and volatility.
3. Runs 5,000 simulated paths over 126 trading days (about six months).
4. Reports a 5th–95th percentile final-price range and probabilities of profit, +10%, and -10% outcomes.
5. Saves `data/aapl_daily.csv` and `output/simulation_paths.png`.

<img width="1210" height="663" alt="image" src="https://github.com/user-attachments/assets/d1a7b42c-084d-4ef5-a915-43ee05287776" />

<img width="562" height="178" alt="image" src="https://github.com/user-attachments/assets/1ba5220b-4648-4a60-bd8a-eb46f9ad5e10" />



## Setup in VS Code on Windows

1. Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
2. Open this project folder in VS Code.
3. In the terminal, run:

```powershell
py -m pip install -r requirements.txt
copy .env.example .env
```

4. Open `.env` and replace `paste_your_key_here` with your own key. Do not put the key in `main.py`, and do not upload `.env` to GitHub.
5. Run:

```powershell
py main.py
```

## Try experiments

In `config.py`, change the ticker, number of forecast days, or number of simulations. Change one value at a time and observe how the final-price range changes.

## Important limitation

This model assumes historical behavior is informative about possible future behavior. Real prices can react to news and events that the simulation cannot predict, so its output is an educational probability exercise—not a forecast or a trading recommendation.
