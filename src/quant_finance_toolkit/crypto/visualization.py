"""Visualization utilities for cryptocurrency analysis."""

from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..data.fetchers import download_crypto_data
from ..portfolio.markowitz import calculate_returns


def plot_crypto_prices(
    crypto_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    normalize: bool = True,
    show_plot: bool = True,
    figsize: tuple = (12, 6),
) -> None:
    """Plot cryptocurrency price history.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data
    normalize : bool, optional
        If True, normalize prices to start at 100 for comparison, by default True
    show_plot : bool, optional
        Whether to display the plot, by default True
    figsize : tuple, optional
        Figure size, by default (12, 6)

    Examples
    --------
    >>> plot_crypto_prices(["BTC-USD", "ETH-USD"], "2020-01-01", "2023-01-01", show_plot=False)
    """
    # Download data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    plt.figure(figsize=figsize)

    if normalize:
        # Normalize to start at 100
        for ticker in crypto_tickers:
            prices = crypto_data[ticker].dropna()
            if len(prices) > 0:
                normalized = (prices / prices.iloc[0]) * 100
                plt.plot(normalized.index, normalized.values, label=ticker, linewidth=2)
        plt.ylabel("Normalized Price (Base = 100)")
        plt.title("Cryptocurrency Price Comparison (Normalized)")
    else:
        # Plot actual prices
        for ticker in crypto_tickers:
            prices = crypto_data[ticker].dropna()
            if len(prices) > 0:
                plt.plot(prices.index, prices.values, label=ticker, linewidth=2)
        plt.ylabel("Price (USD)")
        plt.title("Cryptocurrency Price History")

    plt.xlabel("Date")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if show_plot:
        plt.show()


def plot_crypto_returns(
    crypto_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    show_plot: bool = True,
    figsize: tuple = (14, 6),
) -> None:
    """Plot daily returns for cryptocurrencies.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data
    show_plot : bool, optional
        Whether to display the plot, by default True
    figsize : tuple, optional
        Figure size, by default (14, 6)

    Examples
    --------
    >>> plot_crypto_returns(["BTC-USD", "ETH-USD"], "2020-01-01", "2023-01-01", show_plot=False)
    """
    # Download data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    # Calculate returns
    returns = calculate_returns(crypto_data)

    num_cryptos = len(crypto_tickers)
    fig, axes = plt.subplots(num_cryptos, 1, figsize=figsize, sharex=True)

    if num_cryptos == 1:
        axes = [axes]

    for i, ticker in enumerate(crypto_tickers):
        ticker_returns = returns[ticker].dropna()
        axes[i].plot(
            ticker_returns.index, ticker_returns.values, alpha=0.7, linewidth=1
        )
        axes[i].axhline(y=0, color="black", linestyle="--", linewidth=0.5)
        axes[i].set_ylabel(f"{ticker}\nDaily Returns")
        axes[i].grid(True, alpha=0.3)
        axes[i].set_title(f"{ticker} Daily Returns", fontsize=10)

    axes[-1].set_xlabel("Date")
    plt.suptitle("Cryptocurrency Daily Returns", fontsize=14, y=1.02)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if show_plot:
        plt.show()


def plot_crypto_correlation_heatmap(
    correlation_matrix: pd.DataFrame,
    title: str = "Cryptocurrency Returns Correlation Matrix",
    show_plot: bool = True,
    figsize: tuple = (10, 8),
) -> None:
    """Create correlation heatmap for cryptocurrency returns.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Correlation matrix (from crypto_correlation_matrix or returns.corr())
    title : str, optional
        Plot title, by default "Cryptocurrency Returns Correlation Matrix"
    show_plot : bool, optional
        Whether to display the plot, by default True
    figsize : tuple, optional
        Figure size, by default (10, 8)

    Examples
    --------
    >>> import pandas as pd
    >>> corr = pd.DataFrame([[1.0, 0.8], [0.8, 1.0]], index=["BTC-USD", "ETH-USD"], columns=["BTC-USD", "ETH-USD"])
    >>> plot_crypto_correlation_heatmap(corr, show_plot=False)
    """
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(correlation_matrix, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)

    # Set ticks and labels
    tickers = correlation_matrix.index.tolist()
    ax.set_xticks(np.arange(len(tickers)))
    ax.set_yticks(np.arange(len(tickers)))
    ax.set_xticklabels(tickers, rotation=45, ha="right")
    ax.set_yticklabels(tickers)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Correlation", rotation=270, labelpad=20)

    # Add text annotations
    for i in range(len(tickers)):
        for j in range(len(tickers)):
            text = ax.text(
                j,
                i,
                f"{correlation_matrix.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                color="black" if abs(correlation_matrix.iloc[i, j]) < 0.5 else "white",
                fontweight="bold" if i == j else "normal",
            )

    ax.set_title(title, fontsize=14, pad=20)
    plt.tight_layout()

    if show_plot:
        plt.show()


def plot_crypto_volatility_comparison(
    volatility_data: pd.DataFrame,
    metric: str = "annualized_volatility",
    show_plot: bool = True,
    figsize: tuple = (10, 6),
) -> None:
    """Create bar chart comparing volatility across cryptocurrencies.

    Parameters
    ----------
    volatility_data : pd.DataFrame
        DataFrame with volatility metrics (from crypto_volatility_analysis)
    metric : str, optional
        Which volatility metric to plot, by default "annualized_volatility"
    show_plot : bool, optional
        Whether to display the plot, by default True
    figsize : tuple, optional
        Figure size, by default (10, 6)

    Examples
    --------
    >>> import pandas as pd
    >>> vol_data = pd.DataFrame({"annualized_volatility": [0.8, 1.2]}, index=["BTC-USD", "ETH-USD"])
    >>> plot_crypto_volatility_comparison(vol_data, show_plot=False)
    """
    if metric not in volatility_data.columns:
        raise ValueError(f"Metric '{metric}' not found in volatility_data")

    plt.figure(figsize=figsize)
    tickers = volatility_data.index.tolist()
    values = volatility_data[metric].values

    bars = plt.bar(tickers, values, alpha=0.7, color="steelblue", edgecolor="black")
    plt.xlabel("Cryptocurrency")
    plt.ylabel(metric.replace("_", " ").title())
    plt.title(
        f"Cryptocurrency Volatility Comparison ({metric.replace('_', ' ').title()})"
    )
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3, axis="y")

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.3f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()

    if show_plot:
        plt.show()
