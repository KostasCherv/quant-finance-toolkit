"""Value at Risk (VaR) calculations using analytical and Monte Carlo methods."""

import numpy as np
from scipy.stats import norm


def value_at_risk_n(
    position: float, c: float, mu: float, sigma: float, n: int = 1
) -> float:
    """Calculate Value at Risk (VaR) for n days using analytical method.

    VaR represents the maximum expected loss over a given time period
    at a given confidence level.

    Parameters
    ----------
    position : float
        Portfolio value or position size
    c : float
        Confidence level (e.g., 0.95 for 95%, 0.99 for 99%)
    mu : float
        Expected return (daily)
    sigma : float
        Standard deviation of returns (daily)
    n : int, optional
        Number of days, by default 1

    Returns
    -------
    float
        Value at Risk

    Examples
    --------
    >>> var = value_at_risk_n(1000000, 0.99, 0.001, 0.02, n=1)
    >>> var < 0  # VaR is typically negative (loss)
    True
    """
    var = position * (mu * n - norm.ppf(1 - c) * sigma * np.sqrt(n))
    return var


class ValueAtRiskMonteCarlo:
    """Monte Carlo simulation for Value at Risk calculation.

    Parameters
    ----------
    S : float
        Initial portfolio value
    mu : float
        Expected return (daily)
    sigma : float
        Standard deviation of returns (daily)
    c : float
        Confidence level (e.g., 0.95 for 95%, 0.99 for 99%)
    n : int
        Number of days
    iterations : int, optional
        Number of Monte Carlo simulations, by default 100000

    Examples
    --------
    >>> model = ValueAtRiskMonteCarlo(1000000, 0.001, 0.02, 0.99, 1, 100000)
    >>> var = model.simulation()
    >>> var > 0  # VaR as positive loss amount
    True
    """

    def __init__(
        self,
        S: float,
        mu: float,
        sigma: float,
        c: float,
        n: int,
        iterations: int = 100000,
    ) -> None:
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.c = c
        self.n = n
        self.iterations = iterations

    def simulation(self) -> float:
        """Run Monte Carlo simulation to calculate VaR.

        Returns
        -------
        float
            Value at Risk (as positive loss amount)
        """
        # Generate random returns
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Calculate portfolio values after n days using GBM
        portfolio_values = self.S * np.exp(
            (self.mu - 0.5 * self.sigma**2) * self.n + self.sigma * np.sqrt(self.n) * rand
        )

        # Sort portfolio values
        portfolio_values = np.sort(portfolio_values)

        # Find percentile (1-c) quantile
        percentile = np.percentile(portfolio_values, (1 - self.c) * 100)

        # VaR is the loss from initial value
        return self.S - percentile
