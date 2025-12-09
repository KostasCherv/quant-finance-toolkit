"""Monte Carlo simulation for stock price modeling."""

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def stock_price_monte_carlo(
    S0: float,
    mu: float,
    sigma: float,
    N: int = 1000,
    num_simulations: int = 1000,
    plot: bool = True,
) -> pd.DataFrame:
    """Simulate stock prices using Monte Carlo method with Geometric Brownian Motion.

    Parameters
    ----------
    S0 : float
        Initial stock price
    mu : float
        Expected return (drift)
    sigma : float
        Volatility
    N : int, optional
        Number of time steps, by default 1000
    num_simulations : int, optional
        Number of Monte Carlo simulations, by default 1000
    plot : bool, optional
        Whether to plot the results, by default True

    Returns
    -------
    pd.DataFrame
        DataFrame with simulation results, including mean price path

    Examples
    --------
    >>> results = stock_price_monte_carlo(50, 0.0002, 0.01, N=100, num_simulations=100, plot=False)
    >>> 'mean' in results.columns
    True
    """
    results = []

    for _ in range(num_simulations):
        prices = [S0]
        for _ in range(N):
            prices.append(
                prices[-1]
                * np.exp((mu - 0.5 * sigma**2) + sigma * np.random.standard_normal())
            )
        results.append(prices)

    simulation_data = pd.DataFrame(results)
    simulation_data = simulation_data.T

    simulation_data["mean"] = simulation_data.mean(axis=1)

    if plot:
        plot_stock_price(simulation_data)

    return simulation_data


def plot_stock_price(simulation_data: pd.DataFrame) -> None:
    """Plot Monte Carlo stock price simulation results.

    Parameters
    ----------
    simulation_data : pd.DataFrame
        DataFrame containing simulation results with 'mean' column
    """
    plt.plot(simulation_data["mean"])
    plt.xlabel("Time Step")
    plt.ylabel("Stock Price")
    plt.title("Stock Price Monte Carlo Simulation")
    plt.legend(["Mean Price Path"])
    plt.grid(True)
    plt.show()
