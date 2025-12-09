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


def download_crypto_data(
    crypto_tickers: Union[str, List[str]],
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
) -> pd.DataFrame:
    """Download cryptocurrency price data from Yahoo Finance.

    Parameters
    ----------
    crypto_tickers : Union[str, List[str]]
        Crypto ticker(s) to download (e.g., "BTC-USD", "ETH-USD")
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
    >>> data = download_crypto_data("BTC-USD", "2020-01-01", "2021-01-01")
    >>> "BTC-USD" in data.columns
    True
    >>> data = download_crypto_data(["BTC-USD", "ETH-USD"], "2020-01-01", "2021-01-01")
    >>> len(data.columns) == 2
    True
    """
    if isinstance(crypto_tickers, str):
        crypto_tickers = [crypto_tickers]

    crypto_data = {}
    for ticker in crypto_tickers:
        yf_ticker = yf.Ticker(ticker)
        history = yf_ticker.history(start=start_date, end=end_date)
        if history.empty:
            raise ValueError(f"No data found for crypto ticker: {ticker}")
        crypto_data[ticker] = history["Close"]

    return pd.DataFrame(crypto_data)
