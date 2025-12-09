"""Crypto risk analysis and Value at Risk calculations."""

from typing import Dict, List, Union

import numpy as np
import pandas as pd

from ..data.fetchers import download_crypto_data
from ..portfolio.markowitz import calculate_returns
from ..risk.var import ValueAtRiskMonteCarlo, value_at_risk_n

# Cryptocurrencies trade 24/7, so use 365 days per year
NUM_TRADING_DAYS = 365


def crypto_var_analysis(
    crypto_ticker: str,
    position: float,
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    confidence_level: float = 0.99,
    days: int = 1,
    use_monte_carlo: bool = True,
    mc_iterations: int = 100000,
) -> Dict:
    """Calculate Value at Risk for a cryptocurrency position.

    Parameters
    ----------
    crypto_ticker : str
        Crypto ticker (e.g., "BTC-USD")
    position : float
        Position value in USD
    start_date : Union[str, pd.Timestamp]
        Start date for historical data
    end_date : Union[str, pd.Timestamp]
        End date for historical data
    confidence_level : float, optional
        Confidence level (e.g., 0.95 for 95%, 0.99 for 99%), by default 0.99
    days : int, optional
        Time horizon in days, by default 1
    use_monte_carlo : bool, optional
        Whether to also calculate Monte Carlo VaR, by default True
    mc_iterations : int, optional
        Number of Monte Carlo iterations, by default 100000

    Returns
    -------
    Dict
        Dictionary containing:
        - analytical_var: Analytical VaR
        - monte_carlo_var: Monte Carlo VaR (if calculated)
        - mean_return: Mean daily return
        - volatility: Daily volatility
        - annualized_volatility: Annualized volatility

    Examples
    --------
    >>> var_result = crypto_var_analysis("BTC-USD", 100000, "2020-01-01", "2023-01-01")
    >>> "analytical_var" in var_result
    True
    """
    # Download historical data
    crypto_data = download_crypto_data(crypto_ticker, start_date, end_date)
    prices = crypto_data[crypto_ticker].dropna()

    # Calculate returns
    returns = np.log(prices / prices.shift(1)).dropna()

    # Calculate statistics
    mean_return = returns.mean()
    volatility = returns.std()
    annualized_vol = volatility * np.sqrt(NUM_TRADING_DAYS)

    # Analytical VaR
    analytical_var = value_at_risk_n(
        position=position,
        c=confidence_level,
        mu=mean_return,
        sigma=volatility,
        n=days,
    )

    result = {
        "analytical_var": abs(analytical_var),  # Return as positive loss
        "mean_return": mean_return,
        "volatility": volatility,
        "annualized_volatility": annualized_vol,
        "confidence_level": confidence_level,
        "time_horizon_days": days,
    }

    # Monte Carlo VaR
    if use_monte_carlo:
        mc_var_model = ValueAtRiskMonteCarlo(
            S=position,
            mu=mean_return,
            sigma=volatility,
            c=confidence_level,
            n=days,
            iterations=mc_iterations,
        )
        monte_carlo_var = mc_var_model.simulation()
        result["monte_carlo_var"] = monte_carlo_var
        result["var_difference"] = abs(analytical_var) - monte_carlo_var

    return result


def crypto_portfolio_var(
    crypto_tickers: List[str],
    weights: List[float],
    position: float,
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    confidence_level: float = 0.99,
    days: int = 1,
) -> Dict:
    """Calculate portfolio-level Value at Risk for a crypto portfolio.

    Accounts for correlations between cryptocurrencies.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    weights : List[float]
        Portfolio weights (must sum to 1)
    position : float
        Total portfolio value in USD
    start_date : Union[str, pd.Timestamp]
        Start date for historical data
    end_date : Union[str, pd.Timestamp]
        End date for historical data
    confidence_level : float, optional
        Confidence level (e.g., 0.95 for 95%, 0.99 for 99%), by default 0.99
    days : int, optional
        Time horizon in days, by default 1

    Returns
    -------
    Dict
        Dictionary containing:
        - portfolio_var: Portfolio VaR
        - individual_vars: VaR for each crypto
        - portfolio_volatility: Portfolio volatility
        - correlation_matrix: Correlation matrix of returns

    Examples
    --------
    >>> portfolio_var = crypto_portfolio_var(
    ...     ["BTC-USD", "ETH-USD"], [0.6, 0.4], 100000, "2020-01-01", "2023-01-01"
    ... )
    >>> "portfolio_var" in portfolio_var
    True
    """
    if len(crypto_tickers) != len(weights):
        raise ValueError("Number of tickers must match number of weights")
    if abs(sum(weights) - 1.0) > 1e-6:
        raise ValueError("Weights must sum to 1.0")

    # Download data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    # Calculate returns
    returns = calculate_returns(crypto_data)

    # Calculate individual positions
    individual_positions = [w * position for w in weights]

    # Calculate individual VaRs
    individual_vars = {}
    for i, ticker in enumerate(crypto_tickers):
        ticker_returns = returns[ticker].dropna()
        mean_ret = ticker_returns.mean()
        vol = ticker_returns.std()
        var = value_at_risk_n(
            position=individual_positions[i],
            c=confidence_level,
            mu=mean_ret,
            sigma=vol,
            n=days,
        )
        individual_vars[ticker] = abs(var)

    # Calculate portfolio statistics
    weights_array = np.array(weights)
    portfolio_mean = np.sum(returns.mean() * weights_array) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(
        np.dot(weights_array.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights_array))
    )

    # Portfolio VaR (using portfolio volatility)
    portfolio_mean_daily = portfolio_mean / NUM_TRADING_DAYS
    portfolio_vol_daily = portfolio_volatility / np.sqrt(NUM_TRADING_DAYS)

    portfolio_var = value_at_risk_n(
        position=position,
        c=confidence_level,
        mu=portfolio_mean_daily,
        sigma=portfolio_vol_daily,
        n=days,
    )

    # Correlation matrix
    correlation_matrix = returns.corr()

    return {
        "portfolio_var": abs(portfolio_var),
        "individual_vars": individual_vars,
        "portfolio_volatility": portfolio_volatility,
        "portfolio_mean_return": portfolio_mean,
        "correlation_matrix": correlation_matrix,
        "confidence_level": confidence_level,
        "time_horizon_days": days,
    }
