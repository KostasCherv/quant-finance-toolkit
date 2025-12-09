"""Crypto portfolio optimization and analysis.

Note: This module uses portfolio optimization functions that assume 252 trading days
for annualization. Since crypto trades 24/7 (365 days), the annualized metrics
may be slightly underestimated. For more accurate crypto-specific calculations,
consider using the crypto models and risk modules directly.
"""

from typing import Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..data.fetchers import download_crypto_data
from ..portfolio.markowitz import (
    calculate_returns,
    generate_portfolios,
    optimize_portfolio,
    print_optimized_portfolio,
    show_optimized_portfolio,
    show_portfolios,
    statistics,
)


def optimize_crypto_portfolio(
    crypto_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    num_portfolios: int = 10000,
    show_plot: bool = False,
) -> Dict:
    """Optimize cryptocurrency portfolio using Markowitz model.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for historical data
    end_date : Union[str, pd.Timestamp]
        End date for historical data
    num_portfolios : int, optional
        Number of random portfolios to generate, by default 10000
    show_plot : bool, optional
        Whether to display efficient frontier plot, by default False

    Returns
    -------
    Dict
        Dictionary containing:
        - optimized_weights: Optimal portfolio weights
        - portfolio_stats: Portfolio statistics (return, volatility, Sharpe ratio)
        - all_portfolios: All generated portfolios data
        - returns: Returns DataFrame

    Examples
    --------
    >>> result = optimize_crypto_portfolio(["BTC-USD", "ETH-USD"], "2020-01-01", "2023-01-01")
    >>> "optimized_weights" in result
    True
    """
    # Download crypto data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    # Calculate returns
    returns = calculate_returns(crypto_data)

    # Generate random portfolios
    p_weights, p_means, p_risks = generate_portfolios(
        returns, num_portfolios=num_portfolios
    )

    # Optimize portfolio
    optimized_result = optimize_portfolio(returns)

    # Calculate optimal portfolio statistics
    optimal_weights = optimized_result["x"]
    portfolio_stats = statistics(optimal_weights, returns)

    if show_plot:
        show_optimized_portfolio(
            optimized_result, returns, p_means, p_risks, show_plot=True
        )

    return {
        "optimized_weights": dict(zip(crypto_tickers, optimal_weights)),
        "portfolio_stats": {
            "expected_return": portfolio_stats[0],
            "volatility": portfolio_stats[1],
            "sharpe_ratio": portfolio_stats[2],
        },
        "all_portfolios": {
            "weights": p_weights,
            "returns": p_means,
            "risks": p_risks,
        },
        "returns": returns,
        "optimization_result": optimized_result,
    }


def crypto_correlation_matrix(
    crypto_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    show_plot: bool = False,
) -> pd.DataFrame:
    """Calculate correlation matrix for cryptocurrency returns.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data
    show_plot : bool, optional
        Whether to display correlation heatmap, by default False

    Returns
    -------
    pd.DataFrame
        Correlation matrix of returns

    Examples
    --------
    >>> corr_matrix = crypto_correlation_matrix(["BTC-USD", "ETH-USD"], "2020-01-01", "2023-01-01")
    >>> corr_matrix.shape[0] == len(["BTC-USD", "ETH-USD"])
    True
    """
    # Download data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    # Calculate returns
    returns = calculate_returns(crypto_data)

    # Calculate correlation matrix
    correlation_matrix = returns.corr()

    if show_plot:
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(
            correlation_matrix, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1
        )

        # Set ticks and labels
        ax.set_xticks(np.arange(len(crypto_tickers)))
        ax.set_yticks(np.arange(len(crypto_tickers)))
        ax.set_xticklabels(crypto_tickers, rotation=45, ha="right")
        ax.set_yticklabels(crypto_tickers)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Correlation", rotation=270, labelpad=20)

        # Add text annotations
        for i in range(len(crypto_tickers)):
            for j in range(len(crypto_tickers)):
                text = ax.text(
                    j,
                    i,
                    f"{correlation_matrix.iloc[i, j]:.2f}",
                    ha="center",
                    va="center",
                    color=(
                        "black" if abs(correlation_matrix.iloc[i, j]) < 0.5 else "white"
                    ),
                )

        ax.set_title("Cryptocurrency Returns Correlation Matrix", fontsize=14, pad=20)
        plt.tight_layout()
        plt.show()

    return correlation_matrix
