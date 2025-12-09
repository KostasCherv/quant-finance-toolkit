"""Helper utilities for Streamlit app.

This module provides cached data loading, formatting, and utility functions
for the Streamlit web application.
"""

from typing import List, Tuple, Union

import pandas as pd
import streamlit as st

from quant_finance_toolkit.data import download_crypto_data, download_stock_data


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_stock_data(
    tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
) -> pd.DataFrame:
    """Load and cache stock data.

    Parameters
    ----------
    tickers : List[str]
        List of stock tickers
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data

    Returns
    -------
    pd.DataFrame
        Stock price data
    """
    return download_stock_data(tickers, start_date, end_date)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_crypto_data(
    tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
) -> pd.DataFrame:
    """Load and cache cryptocurrency data.

    Parameters
    ----------
    tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data

    Returns
    -------
    pd.DataFrame
        Crypto price data
    """
    return download_crypto_data(tickers, start_date, end_date)


def format_currency(value: float, decimals: int = 2) -> str:
    """Format number as currency.

    Parameters
    ----------
    value : float
        Value to format
    decimals : int, optional
        Number of decimal places, by default 2

    Returns
    -------
    str
        Formatted currency string
    """
    return f"${value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format number as percentage.

    Parameters
    ----------
    value : float
        Value to format (as decimal, e.g., 0.05 for 5%)
    decimals : int, optional
        Number of decimal places, by default 2

    Returns
    -------
    str
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def validate_date_range(start_date, end_date) -> bool:
    """Validate that start date is before end date.

    Parameters
    ----------
    start_date : Union[str, pd.Timestamp]
        Start date
    end_date : Union[str, pd.Timestamp]
        End date

    Returns
    -------
    bool
        True if valid, False otherwise
    """
    start = pd.Timestamp(start_date) if isinstance(start_date, str) else start_date
    end = pd.Timestamp(end_date) if isinstance(end_date, str) else end_date
    return start < end


def validate_tickers(tickers: List[str]) -> Tuple[bool, str]:
    """Validate ticker list is not empty.

    Parameters
    ----------
    tickers : List[str]
        List of tickers

    Returns
    -------
    tuple[bool, str]
        (is_valid, error_message)
    """
    if not tickers or len(tickers) == 0:
        return False, "Please select at least one ticker."
    if len(tickers) < 2 and "portfolio" in st.session_state.get("page", ""):
        return False, "Please select at least two tickers for portfolio analysis."
    return True, ""
