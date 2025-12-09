"""Crypto-specific financial models."""

from typing import Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..data.fetchers import download_crypto_data, download_stock_data
from ..models.stochastic import simulate_gbm
from ..portfolio.markowitz import calculate_returns

# Cryptocurrencies trade 24/7, so use 365 days per year
NUM_TRADING_DAYS = 365


def crypto_price_simulation(
    crypto_ticker: str,
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    T: float = 1.0,
    num_simulations: int = 1000,
    show_plot: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Simulate crypto price using GBM based on historical data.

    Downloads historical crypto data, calculates historical returns and volatility,
    then runs Monte Carlo GBM simulations.

    Parameters
    ----------
    crypto_ticker : str
        Crypto ticker (e.g., "BTC-USD")
    start_date : Union[str, pd.Timestamp]
        Start date for historical data
    end_date : Union[str, pd.Timestamp]
        End date for historical data
    T : float, optional
        Time horizon for simulation in years, by default 1.0
    num_simulations : int, optional
        Number of Monte Carlo simulations, by default 1000
    show_plot : bool, optional
        Whether to display simulation plot, by default False

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, float]]
        Tuple of (simulation results DataFrame, statistics dictionary)
        Statistics include: mean_final_price, std_final_price, min_price, max_price

    Examples
    --------
    >>> results, stats = crypto_price_simulation("BTC-USD", "2020-01-01", "2023-01-01", T=1.0, num_simulations=100)
    >>> "mean_final_price" in stats
    True
    """
    # Download historical data
    historical_data = download_crypto_data(crypto_ticker, start_date, end_date)
    prices = historical_data[crypto_ticker].dropna()

    # Calculate returns
    returns = np.log(prices / prices.shift(1)).dropna()

    # Calculate historical statistics
    mu = returns.mean() * NUM_TRADING_DAYS  # Annualized return
    sigma = returns.std() * np.sqrt(NUM_TRADING_DAYS)  # Annualized volatility
    s0 = prices.iloc[-1]  # Current price

    # Run simulations
    simulation_results = []
    for _ in range(num_simulations):
        _, price_path = simulate_gbm(
            s0=s0, T=T, N=int(T * NUM_TRADING_DAYS), mu=mu, sigma=sigma
        )
        simulation_results.append(price_path)

    simulation_df = pd.DataFrame(simulation_results).T

    # Calculate statistics
    final_prices = simulation_df.iloc[-1]
    stats = {
        "mean_final_price": float(final_prices.mean()),
        "std_final_price": float(final_prices.std()),
        "min_price": float(final_prices.min()),
        "max_price": float(final_prices.max()),
        "historical_mu": float(mu),
        "historical_sigma": float(sigma),
        "current_price": float(s0),
    }

    if show_plot:
        plt.figure(figsize=(12, 6))
        # Plot sample of simulations
        sample_size = min(50, num_simulations)
        for i in range(sample_size):
            plt.plot(simulation_df.iloc[:, i], alpha=0.1, color="blue")
        plt.plot(
            simulation_df.mean(axis=1), color="red", linewidth=2, label="Mean Path"
        )
        plt.axhline(y=s0, color="green", linestyle="--", label="Current Price")
        plt.xlabel("Time Steps")
        plt.ylabel("Price (USD)")
        plt.title(f"{crypto_ticker} Price Simulation (GBM)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    return simulation_df, stats


def crypto_volatility_analysis(
    crypto_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
) -> pd.DataFrame:
    """Analyze volatility across multiple cryptocurrencies.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data

    Returns
    -------
    pd.DataFrame
        DataFrame with volatility metrics:
        - daily_volatility: Daily volatility
        - weekly_volatility: Weekly volatility
        - monthly_volatility: Monthly volatility
        - annualized_volatility: Annualized volatility

    Examples
    --------
    >>> volatilities = crypto_volatility_analysis(["BTC-USD", "ETH-USD"], "2020-01-01", "2023-01-01")
    >>> "daily_volatility" in volatilities.columns
    True
    """
    # Download data for all cryptos
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    # Calculate returns
    returns = calculate_returns(crypto_data)

    # Calculate volatilities
    volatility_metrics = []
    for ticker in crypto_tickers:
        ticker_returns = returns[ticker].dropna()
        daily_vol = ticker_returns.std()
        weekly_vol = daily_vol * np.sqrt(5)  # 5 trading days per week
        monthly_vol = daily_vol * np.sqrt(21)  # ~21 trading days per month
        annualized_vol = daily_vol * np.sqrt(NUM_TRADING_DAYS)

        volatility_metrics.append(
            {
                "ticker": ticker,
                "daily_volatility": daily_vol,
                "weekly_volatility": weekly_vol,
                "monthly_volatility": monthly_vol,
                "annualized_volatility": annualized_vol,
            }
        )

    return pd.DataFrame(volatility_metrics).set_index("ticker")


def compare_crypto_stocks(
    crypto_tickers: List[str],
    stock_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    risk_free_rate: float = 0.05,
    show_plot: bool = False,
) -> pd.DataFrame:
    """Compare cryptocurrency and traditional stock performance metrics.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    stock_tickers : List[str]
        List of stock tickers (e.g., ["AAPL", "MSFT"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data
    risk_free_rate : float, optional
        Risk-free rate for Sharpe ratio calculation, by default 0.05
    show_plot : bool, optional
        Whether to display comparison plot, by default False

    Returns
    -------
    pd.DataFrame
        DataFrame with comparison metrics:
        - average_return: Average annualized return
        - volatility: Annualized volatility
        - sharpe_ratio: Sharpe ratio
        - asset_type: "Crypto" or "Stock"

    Examples
    --------
    >>> comparison = compare_crypto_stocks(["BTC-USD"], ["AAPL"], "2020-01-01", "2023-01-01")
    >>> "sharpe_ratio" in comparison.columns
    True
    """
    # Download data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)
    stock_data = download_stock_data(stock_tickers, start_date, end_date)

    # Calculate returns
    crypto_returns = calculate_returns(crypto_data)
    stock_returns = calculate_returns(stock_data)

    comparison_metrics = []

    # Analyze cryptos
    for ticker in crypto_tickers:
        returns = crypto_returns[ticker].dropna()
        avg_return = returns.mean() * NUM_TRADING_DAYS
        volatility = returns.std() * np.sqrt(NUM_TRADING_DAYS)
        sharpe = (avg_return - risk_free_rate) / volatility if volatility > 0 else 0

        comparison_metrics.append(
            {
                "ticker": ticker,
                "average_return": avg_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe,
                "asset_type": "Crypto",
            }
        )

    # Analyze stocks
    for ticker in stock_tickers:
        returns = stock_returns[ticker].dropna()
        avg_return = returns.mean() * NUM_TRADING_DAYS
        volatility = returns.std() * np.sqrt(NUM_TRADING_DAYS)
        sharpe = (avg_return - risk_free_rate) / volatility if volatility > 0 else 0

        comparison_metrics.append(
            {
                "ticker": ticker,
                "average_return": avg_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe,
                "asset_type": "Stock",
            }
        )

    comparison_df = pd.DataFrame(comparison_metrics).set_index("ticker")

    if show_plot:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Volatility vs Return scatter
        crypto_data = comparison_df[comparison_df["asset_type"] == "Crypto"]
        stock_data = comparison_df[comparison_df["asset_type"] == "Stock"]

        axes[0].scatter(
            crypto_data["volatility"],
            crypto_data["average_return"],
            label="Crypto",
            s=100,
            alpha=0.7,
            color="orange",
        )
        axes[0].scatter(
            stock_data["volatility"],
            stock_data["average_return"],
            label="Stocks",
            s=100,
            alpha=0.7,
            color="blue",
        )
        axes[0].set_xlabel("Volatility (Annualized)")
        axes[0].set_ylabel("Average Return (Annualized)")
        axes[0].set_title("Risk-Return Comparison")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Sharpe Ratio comparison
        asset_types = ["Crypto", "Stock"]
        sharpe_means = [
            comparison_df[comparison_df["asset_type"] == at]["sharpe_ratio"].mean()
            for at in asset_types
        ]
        axes[1].bar(asset_types, sharpe_means, color=["orange", "blue"], alpha=0.7)
        axes[1].set_ylabel("Average Sharpe Ratio")
        axes[1].set_title("Average Sharpe Ratio Comparison")
        axes[1].grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        plt.show()

    return comparison_df
