"""Data fetching utilities for financial market data."""

from datetime import datetime
from typing import List, Union

import pandas as pd
import yfinance as yf


def download_stock_data(
    stocks: Union[str, List[str]],
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
) -> pd.DataFrame:
    """Download stock price data from Yahoo Finance.

    Parameters
    ----------
    stocks : Union[str, List[str]]
        Stock ticker(s) to download
    start_date : Union[str, datetime]
        Start date for data
    end_date : Union[str, datetime]
        End date for data

    Returns
    -------
    pd.DataFrame
        DataFrame with Close prices. For single ticker, column is ticker name.
        For multiple tickers, columns are ticker names.

    Examples
    --------
    >>> data = download_stock_data("AAPL", "2020-01-01", "2021-01-01")
    >>> "AAPL" in data.columns
    True
    """
    if isinstance(stocks, str):
        stocks = [stocks]

    stock_data = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        history = ticker.history(start=start_date, end=end_date)
        if history.empty:
            raise ValueError(f"No data found for ticker: {stock}")
        stock_data[stock] = history["Close"]

    return pd.DataFrame(stock_data)
