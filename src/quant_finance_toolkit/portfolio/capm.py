"""Capital Asset Pricing Model (CAPM) implementation."""

from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# Market risk-free rate
RISK_FREE_RATE = 0.05

# Months in year for annualization
MONTHS_IN_YEAR = 12


class CAPM:
    """Capital Asset Pricing Model for calculating beta and expected returns.

    CAPM relates the expected return of an asset to its beta (sensitivity to market)
    and the risk-free rate: E[R] = Rf + beta * (E[Rm] - Rf)

    Parameters
    ----------
    stocks : List[str]
        List of stock tickers [stock, market_index]
    start_date : str
        Start date for data (format: "YYYY-MM-DD")
    end_date : str
        End date for data (format: "YYYY-MM-DD")
    risk_free_rate : float, optional
        Risk-free rate, by default 0.05

    Examples
    --------
    >>> capm = CAPM(["IBM", "^GSPC"], "2009-12-01", "2017-01-01")
    >>> capm.initialize()
    >>> beta = capm.calculate_beta()
    """

    def __init__(
        self,
        stocks: List[str],
        start_date: str,
        end_date: str,
        risk_free_rate: float = RISK_FREE_RATE,
    ) -> None:
        if len(stocks) != 2:
            raise ValueError("stocks must contain exactly 2 tickers: [stock, market_index]")

        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.risk_free_rate = risk_free_rate
        self.data: Optional[pd.DataFrame] = None

    def download_data(self) -> pd.DataFrame:
        """Download stock price data from Yahoo Finance.

        Returns
        -------
        pd.DataFrame
            DataFrame with Close prices
        """
        # Download all stocks at once
        ticker_data = yf.download(self.stocks, start=self.start_date, end=self.end_date)

        # Extract Close prices - handle both single and multiple ticker cases
        if len(self.stocks) == 1:
            df = ticker_data[["Close"]].copy()
            df.columns = self.stocks
        else:
            # For multiple tickers, Close is a column in the MultiIndex
            df = ticker_data["Close"].copy()

        return df

    def initialize(self) -> None:
        """Initialize and prepare data for CAPM calculations."""
        stock_data = self.download_data()
        stock_data = stock_data.resample("M").last()

        self.data = pd.DataFrame(
            {
                "s_adjclose": stock_data[self.stocks[0]],
                "m_adjclose": stock_data[self.stocks[1]],
            }
        )
        self.data[["s_returns", "m_returns"]] = np.log(
            self.data[["s_adjclose", "m_adjclose"]]
            / self.data[["s_adjclose", "m_adjclose"]].shift(1)
        )

        self.data = self.data[1:]

    def calculate_beta(self) -> float:
        """Calculate beta using covariance method.

        Beta = Cov(stock, market) / Var(market)

        Returns
        -------
        float
            Beta coefficient

        Raises
        ------
        ValueError
            If data has not been initialized
        """
        if self.data is None:
            raise ValueError("Must call initialize() before calculate_beta()")

        covariance_matrix = np.cov(self.data["s_returns"], self.data["m_returns"])
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        print(f"Beta: {beta:.4f}")
        return beta

    def regression(self, show_plot: bool = True) -> Tuple[float, float, float]:
        """Perform linear regression to find alpha and beta, calculate expected return.

        Parameters
        ----------
        show_plot : bool, optional
            Whether to display the regression plot, by default True

        Returns
        -------
        Tuple[float, float, float]
            Tuple of (beta, alpha, expected_return)

        Raises
        ------
        ValueError
            If data has not been initialized
        """
        if self.data is None:
            raise ValueError("Must call initialize() before regression()")

        beta, alpha = np.polyfit(self.data["m_returns"], self.data["s_returns"], deg=1)
        print(f"Beta: {beta:.4f}")
        print(f"Alpha: {alpha:.4f}")

        expected_return = self.risk_free_rate + beta * (
            self.data["m_returns"].mean() * MONTHS_IN_YEAR - self.risk_free_rate
        )
        print(f"Expected Return: {expected_return:.4f}")

        if show_plot:
            self.plot_regression(alpha, beta)

        return beta, alpha, expected_return

    def plot_regression(self, alpha: float, beta: float) -> None:
        """Plot CAPM regression line.

        Parameters
        ----------
        alpha : float
            Intercept (alpha)
        beta : float
            Slope (beta)
        """
        if self.data is None:
            raise ValueError("Must call initialize() before plot_regression()")

        fig, axis = plt.subplots(1, figsize=(12, 8))
        axis.scatter(
            self.data["m_returns"], self.data["s_returns"], label="Data Points", alpha=0.6
        )
        axis.plot(
            self.data["m_returns"],
            beta * self.data["m_returns"] + alpha,
            color="red",
            label="CAPM Line",
            linewidth=2,
        )
        plt.title("Capital Asset Pricing Model - Finding Alpha and Beta", fontsize=14)
        plt.xlabel("Market return $R_m$", fontsize=12)
        plt.ylabel("Stock return $R_s$", fontsize=12)
        plt.text(
            0.05,
            0.95,
            r"$R_s = \beta \cdot R_m + \alpha$",
            fontsize=14,
            transform=axis.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
