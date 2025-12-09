"""Vasicek interest rate model and bond pricing."""

from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import pandas as pd


def vasicek_model(
    r0: float, kappa: float, theta: float, sigma: float, T: float = 1.0, N: int = 10000
) -> Tuple[np.ndarray, list]:
    """Simulate interest rates using the Vasicek model.

    The Vasicek model is a mean-reverting stochastic process:
    dr = kappa*(theta - r)*dt + sigma*dW

    Parameters
    ----------
    r0 : float
        Initial interest rate
    kappa : float
        Mean reversion speed
    theta : float
        Long-term mean interest rate
    sigma : float
        Volatility
    T : float, optional
        Time horizon in years, by default 1.0
    N : int, optional
        Number of time steps, by default 10000

    Returns
    -------
    Tuple[np.ndarray, list]
        Tuple of (time array, interest rate path)

    Examples
    --------
    >>> t, rates = vasicek_model(1.3, 0.9, 1.4, 0.05, T=1.0, N=100)
    >>> len(rates) == len(t)
    True
    """
    dt = T / float(N)
    t = np.linspace(0, T, N + 1)
    rates = [r0]
    for _ in range(N):
        dr = kappa * (theta - rates[-1]) * dt + sigma * np.sqrt(dt) * npr.normal()
        rates.append(rates[-1] + dr)
    return t, rates


def monte_carlo_bond_pricing(
    x: float,
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    T: float = 1.0,
    num_simulations: int = 1000,
    num_points: int = 200,
) -> float:
    """Price a bond using Monte Carlo simulation with Vasicek interest rate model.

    Parameters
    ----------
    x : float
        Face value of the bond
    r0 : float
        Initial interest rate
    kappa : float
        Mean reversion speed
    theta : float
        Long-term mean interest rate
    sigma : float
        Volatility
    T : float, optional
        Time to maturity in years, by default 1.0
    num_simulations : int, optional
        Number of Monte Carlo simulations, by default 1000
    num_points : int, optional
        Number of time points per simulation, by default 200

    Returns
    -------
    float
        Estimated bond price

    Examples
    --------
    >>> price = monte_carlo_bond_pricing(1000, 0.5, 0.3, 0.9, 0.03)
    >>> price > 0
    True
    """
    dt = T / float(num_points)
    results = []

    for _ in range(num_simulations):
        rates = [r0]
        for _ in range(num_points):
            dr = (
                kappa * (theta - rates[-1]) * dt
                + sigma * np.sqrt(dt) * np.random.normal()
            )
            rates.append(rates[-1] + dr)
        results.append(rates)

    simulation_data = pd.DataFrame(results).T

    # Calculate integral of interest rates
    integral_sum = simulation_data.sum() * dt
    # Discount factor: exp(-integral of rates)
    present_integral_value = np.exp(-integral_sum)

    # Average across all simulations
    bond_price = x * np.mean(present_integral_value)

    return bond_price
