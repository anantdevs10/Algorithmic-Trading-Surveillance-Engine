import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .database import SessionLocal, engine, Base
from .models import Symbol, MarketData, OrderEvent

def random_walk_ohlcv(start_price=100.0, periods=500, seed=None): # generates 500 minutes of fake prices starting at £100 a share
    rng = np.random.default_rng(seed) # random number generator created
    returns = rng.normal(loc=0.0, scale=0.01, size=periods)   # 1% per-step volatility, creates 500 random percentage changes where prices fluctuate around 1% up or down. 
    # this is our random value which fluctuates the graph/.
    close = start_price * np.exp(np.cumsum(returns)) # calculates the closing prices, cumulative product means that its compounding each steps percentage on the price before.
    high = close * (1 + rng.uniform(0, 0.005, periods)) # adds a 0 - 0.5% bump t ostimulate the highest price reached before reaching the closing price
    low = close * (1 - rng.uniform(0, 0.005, periods)) # same thing but subtracts for lowest price
    open_ = np.roll(close, 1); open_[0] = start_price # opening price = clsing price with np roll shifgting array values.
    volume = rng.integers(1000, 50000, periods) # Generates a random whole number between 1,000 and 50,000 for trading volume
    timestamps = [datetime.now() - timedelta(minutes=periods - i) for i in range(periods)] # Builds a list of 500 sequential timestamps counting up minute-by-minute until right now.
    return pd.DataFrame({
        "timestamp": timestamps, "open": open_, "high": high,
        "low": low, "close": close, "volume": volume,
    })
# all pakages generated into a pandas dataframe and is returned

def seed_database(db):
    watchlist = ["AAPL", "MSFT", "TSLA"]
    for i, ticker in enumerate(watchlist):
        db.add(Symbol(ticker=ticker, name=ticker))
        df = random_walk_ohlcv(seed=i)
        for _, row in df.iterrows():
            db.add(MarketData(ticker=ticker, **row.to_dict()))
    db.commit()

# adding 1500 market data rows in the database for the 3 stock symbols

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing = db.query(Symbol).first()
    if existing:
        print("Existing seed data found — clearing MarketData and Symbol tables before reseeding.")
        db.query(MarketData).delete()
        db.query(Symbol).delete()
        db.commit()

    seed_database(db)
    print("Seeded 3 symbols with 500 rows of simulated OHLCV data each.")

'''
Building my stimulated stock market data using the Random Walk (Geometric Bownian Motion)
The Math:

Share price grows in an exponentional manner.
Brownian Motion gives the share price its jaggedness in the gaph.
This brownian motion is mimicked here by pulling a random return from a normal distribution. 
rng.normal(loc=0.0, scale=0.01)
This creates fluctuation
The NumpySeed
'''