"""Markowitz portfolio optimization model."""

from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as optimization

NUM_TRADING_DAYS = 252


def calculate_returns(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate log returns from price data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame with price data (columns are assets)

    Returns
    -------
    pd.DataFrame
        DataFrame with log returns
    """
    log_return = np.log(data / data.shift(1))
    return log_return.dropna()


def show_statistics(returns: pd.DataFrame) -> None:
    """Print annualized return statistics.

    Parameters
    ----------
    returns : pd.DataFrame
        DataFrame with returns data
    """
    # Mean of annualized returns
    print("Annualized Returns:")
    print(returns.mean() * NUM_TRADING_DAYS)
    # Covariance of returns
    print("\nAnnualized Covariance Matrix:")
    print(returns.cov() * NUM_TRADING_DAYS)


def generate_portfolios(
    returns: pd.DataFrame, num_portfolios: int = 10000
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate random portfolios for efficient frontier analysis.

    Parameters
    ----------
    returns : pd.DataFrame
        DataFrame with returns data
    num_portfolios : int, optional
        Number of random portfolios to generate, by default 10000

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Tuple of (weights, portfolio_means, portfolio_risks)
    """
    num_assets = len(returns.columns)
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []

    for _ in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)  # Normalize to sum to 1
        portfolio_weights.append(weights)
        portfolio_means.append(
            np.sum((returns.mean() * weights) * NUM_TRADING_DAYS)
        )
        portfolio_risks.append(
            np.sqrt(
                np.dot(
                    weights.T,
                    np.dot(returns.cov() * NUM_TRADING_DAYS, weights),
                )
            )
        )

    return (
        np.array(portfolio_weights),
        np.array(portfolio_means),
        np.array(portfolio_risks),
    )


def show_portfolios(
    returns: np.ndarray, volatilities: np.ndarray, show_plot: bool = True
) -> None:
    """Plot efficient frontier with portfolio scatter.

    Parameters
    ----------
    returns : np.ndarray
        Array of portfolio expected returns
    volatilities : np.ndarray
        Array of portfolio volatilities
    show_plot : bool, optional
        Whether to display the plot, by default True
    """
    plt.figure(figsize=(10, 6))
    sharpe_ratios = returns / volatilities
    plt.scatter(volatilities, returns, c=sharpe_ratios, marker="o", cmap="viridis")
    plt.grid(True)
    plt.xlabel("Expected Risk (Volatility)")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.title("Efficient Frontier - Random Portfolios")
    if show_plot:
        plt.show()


def statistics(weights: np.ndarray, returns: pd.DataFrame) -> np.ndarray:
    """Calculate portfolio statistics (return, volatility, Sharpe ratio).

    Parameters
    ----------
    weights : np.ndarray
        Portfolio weights (must sum to 1)
    returns : pd.DataFrame
        DataFrame with returns data

    Returns
    -------
    np.ndarray
        Array of [portfolio_returns, portfolio_volatility, sharpe_ratio]
    """
    portfolio_returns = np.sum((returns.mean() * weights) * NUM_TRADING_DAYS)
    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights))
    )
    sharpe_ratio = portfolio_returns / portfolio_volatility

    return np.array([portfolio_returns, portfolio_volatility, sharpe_ratio])


def optimize_portfolio(
    returns: pd.DataFrame, initial_weights: Optional[np.ndarray] = None
) -> dict:
    """Optimize portfolio to maximize Sharpe ratio.

    Parameters
    ----------
    returns : pd.DataFrame
        DataFrame with returns data
    initial_weights : Optional[np.ndarray], optional
        Initial guess for weights, by default None (equal weights)

    Returns
    -------
    dict
        Optimization results from scipy.optimize.minimize
    """
    num_assets = len(returns.columns)

    if initial_weights is None:
        initial_weights = np.array([1.0 / num_assets] * num_assets)

    # Minimize negative Sharpe ratio (equivalent to maximizing Sharpe ratio)
    def min_function_sharpe(weights: np.ndarray) -> float:
        return -statistics(weights, returns)[2]

    # Constraint: sum of weights = 1
    constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
    # Bounds: each weight between 0 and 1
    bounds = tuple((0, 1) for _ in range(num_assets))

    optimized_results = optimization.minimize(
        min_function_sharpe,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    return optimized_results


def print_optimized_portfolio(optimum: dict, returns: pd.DataFrame) -> None:
    """Print optimized portfolio statistics.

    Parameters
    ----------
    optimum : dict
        Optimization results from optimize_portfolio
    returns : pd.DataFrame
        DataFrame with returns data
    """
    optimal_weights = optimum["x"].round(3)
    stats = statistics(optimal_weights, returns)

    print(f"Optimal Portfolio Weights: {optimal_weights}")
    print(f"Expected Return: {stats[0]:.4f}")
    print(f"Expected Volatility: {stats[1]:.4f}")
    print(f"Sharpe Ratio: {stats[2]:.4f}")


def show_optimized_portfolio(
    opt: dict,
    returns: pd.DataFrame,
    portfolio_returns: np.ndarray,
    portfolio_volatility: np.ndarray,
    show_plot: bool = True,
) -> None:
    """Plot efficient frontier with optimal portfolio highlighted.

    Parameters
    ----------
    opt : dict
        Optimization results from optimize_portfolio
    returns : pd.DataFrame
        DataFrame with returns data
    portfolio_returns : np.ndarray
        Array of portfolio expected returns
    portfolio_volatility : np.ndarray
        Array of portfolio volatilities
    show_plot : bool, optional
        Whether to display the plot, by default True
    """
    plt.figure(figsize=(10, 6))
    sharpe_ratios = portfolio_returns / portfolio_volatility
    plt.scatter(
        portfolio_volatility,
        portfolio_returns,
        c=sharpe_ratios,
        marker="o",
        cmap="viridis",
        alpha=0.6,
    )
    plt.grid(True)
    plt.xlabel("Expected Risk (Volatility)")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.title("Efficient Frontier with Optimal Portfolio")

    # Plot optimal portfolio
    optimal_stats = statistics(opt["x"].round(3), returns)
    plt.plot(
        optimal_stats[1],
        optimal_stats[0],
        "r*",
        markersize=20.0,
        label="Optimal Portfolio",
    )
    plt.legend()

    if show_plot:
        plt.show()
