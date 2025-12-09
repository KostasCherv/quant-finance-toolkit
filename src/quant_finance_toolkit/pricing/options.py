"""Option pricing models using Black-Scholes and Monte Carlo methods."""

from typing import Union

import numpy as np
from numpy import exp, log, sqrt
from scipy import stats


def call_option_price(
    S: float, E: float, T: float, rf: float, sigma: float
) -> float:
    """Calculate European call option price using Black-Scholes formula.

    Parameters
    ----------
    S : float
        Current stock price
    E : float
        Exercise (strike) price
    T : float
        Time to expiration in years
    rf : float
        Risk-free interest rate (as decimal)
    sigma : float
        Volatility (annualized standard deviation of returns)

    Returns
    -------
    float
        Call option price

    Examples
    --------
    >>> call_option_price(100, 100, 1, 0.05, 0.2)
    10.450583572185565
    """
    d1 = (log(S / E) + (rf + sigma * sigma / 2.0) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * stats.norm.cdf(d1) - E * exp(-rf * T) * stats.norm.cdf(d2)


def put_option_price(
    S: float, E: float, T: float, rf: float, sigma: float
) -> float:
    """Calculate European put option price using Black-Scholes formula.

    Parameters
    ----------
    S : float
        Current stock price
    E : float
        Exercise (strike) price
    T : float
        Time to expiration in years
    rf : float
        Risk-free interest rate (as decimal)
    sigma : float
        Volatility (annualized standard deviation of returns)

    Returns
    -------
    float
        Put option price

    Examples
    --------
    >>> put_option_price(100, 100, 1, 0.05, 0.2)
    5.573526022256971
    """
    d1 = (log(S / E) + (rf + sigma * sigma / 2.0) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return -S * stats.norm.cdf(-d1) + E * exp(-rf * T) * stats.norm.cdf(-d2)


class OptionPriceMonteCarlo:
    """Monte Carlo simulation for European option pricing.

    Parameters
    ----------
    S0 : float
        Initial stock price
    E : float
        Exercise (strike) price
    T : float
        Time to expiration in years
    rf : float
        Risk-free interest rate (as decimal)
    sigma : float
        Volatility (annualized standard deviation of returns)
    iterations : int, optional
        Number of Monte Carlo simulations, by default 10000

    Examples
    --------
    >>> model = OptionPriceMonteCarlo(100, 100, 1, 0.05, 0.2, 10000)
    >>> call_price = model.call_option_price()
    >>> put_price = model.put_option_price()
    """

    def __init__(
        self,
        S0: float,
        E: float,
        T: float,
        rf: float,
        sigma: float,
        iterations: int = 10000,
    ) -> None:
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations

    def call_option_price(self) -> float:
        """Calculate call option price using Monte Carlo simulation.

        Returns
        -------
        float
            Estimated call option price
        """
        option_data = np.zeros([self.iterations, 2])

        # Generate random numbers for Wiener process
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Calculate stock price at expiration using GBM
        stock_price = self.S0 * exp(
            (self.rf - 0.5 * self.sigma**2) * self.T
            + self.sigma * sqrt(self.T) * rand
        )

        # Payoff: max(0, S - E)
        option_data[:, 1] = stock_price - self.E

        # Average payoff
        average_option_price = np.sum(np.amax(option_data, axis=1)) / float(
            self.iterations
        )

        # Discount to present value
        present_value = average_option_price * exp(-self.rf * self.T)

        return present_value

    def put_option_price(self) -> float:
        """Calculate put option price using Monte Carlo simulation.

        Returns
        -------
        float
            Estimated put option price
        """
        option_data = np.zeros([self.iterations, 2])

        # Generate random numbers for Wiener process
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Calculate stock price at expiration using GBM
        stock_price = self.S0 * exp(
            (self.rf - 0.5 * self.sigma**2) * self.T
            + self.sigma * sqrt(self.T) * rand
        )

        # Payoff: max(0, E - S)
        option_data[:, 1] = self.E - stock_price

        # Average payoff
        average_option_price = np.sum(np.amax(option_data, axis=1)) / float(
            self.iterations
        )

        # Discount to present value
        present_value = average_option_price * exp(-self.rf * self.T)

        return present_value
