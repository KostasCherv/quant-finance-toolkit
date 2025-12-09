"""Stochastic processes for financial modeling."""

from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr


def wiener_process(dt: float = 0.1, x0: float = 0, n: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a Wiener process (Brownian motion).

    Parameters
    ----------
    dt : float, optional
        Time step size, by default 0.1
    x0 : float, optional
        Initial value, by default 0
    n : int, optional
        Number of steps, by default 1000

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tuple of (time array, Wiener process values)

    Examples
    --------
    >>> t, w = wiener_process(dt=0.1, n=100)
    >>> len(t) == len(w)
    True
    """
    w = np.zeros(n + 1)
    t = np.linspace(x0, n, n + 1)

    w[1 : n + 1] = np.cumsum(npr.normal(0, np.sqrt(dt), n))

    return t, w


def simulate_gbm(
    s0: float, T: float = 2, N: int = 1000, mu: float = 0.1, sigma: float = 0.05
) -> Tuple[np.ndarray, np.ndarray]:
    """Simulate Geometric Brownian Motion (GBM) for stock prices.

    GBM follows the stochastic differential equation:
    dS = mu*S*dt + sigma*S*dW

    Parameters
    ----------
    s0 : float
        Initial stock price
    T : float, optional
        Time horizon in years, by default 2
    N : int, optional
        Number of time steps, by default 1000
    mu : float, optional
        Drift (expected return), by default 0.1
    sigma : float, optional
        Volatility, by default 0.05

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tuple of (time array, stock price array)

    Examples
    --------
    >>> t, s = simulate_gbm(s0=100, T=1, N=100)
    >>> s[0] == 100
    True
    """
    dt = T / N
    t = np.linspace(0, T, N)

    # Standard normal random variables N(0, 1)
    W = np.random.standard_normal(size=N)
    # N(0, dt) = sqrt(dt) * N(0, 1)
    W = np.cumsum(W) * np.sqrt(dt)

    X = (mu - 0.5 * sigma**2) * t + sigma * W
    S = s0 * np.exp(X)

    return t, S


def generate_ornstein_uhlenbeck(
    dt: float = 0.1, theta: float = 1.2, mu: float = 0.5, sigma: float = 0.3, n: int = 10000
) -> np.ndarray:
    """Generate Ornstein-Uhlenbeck process.

    The Ornstein-Uhlenbeck process is a mean-reverting stochastic process:
    dX = theta*(mu - X)*dt + sigma*dW

    Parameters
    ----------
    dt : float, optional
        Time step size, by default 0.1
    theta : float, optional
        Mean reversion speed, by default 1.2
    mu : float, optional
        Long-term mean, by default 0.5
    sigma : float, optional
        Volatility, by default 0.3
    n : int, optional
        Number of steps, by default 10000

    Returns
    -------
    np.ndarray
        Array of process values

    Examples
    --------
    >>> x = generate_ornstein_uhlenbeck(n=100)
    >>> len(x) == 100
    True
    """
    x = np.zeros(n)

    for t in range(1, n):
        x[t] = (
            x[t - 1]
            + theta * (mu - x[t - 1]) * dt
            + sigma * npr.normal(0, np.sqrt(dt))
        )
    return x
