import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
import datetime as dt


def download_data(stock, start_date, end_date):
    data = {}
    ticker = yf.Ticker(stock)
    data[stock] = ticker.history(start=start_date, end=end_date)["Close"]
    return pd.DataFrame(data)


class ValueAtRiskMonteCarlo:

    def __init__(self, S, mu, sigma, c, n, iterations):
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.c = c
        self.n = n
        self.iterations = iterations

    def simulation(self):
        rand = np.random.normal(0, 1, [1, self.iterations])
        stock_prices = self.S * np.exp(
            (self.mu - 0.5 * self.sigma**2) * self.n
            + self.sigma * np.sqrt(self.n) * rand
        )
        # sort the stock prices
        stock_prices = np.sort(stock_prices)
        # percentile
        percentile = np.percentile(stock_prices, (1 - self.c) * 100)

        return self.S - percentile


if __name__ == "__main__":
    stock = "C"
    start_date = dt.datetime(2014, 1, 1)
    end_date = dt.datetime(2017, 10, 15)
    stock_data = download_data(stock, start_date, end_date)
    print(stock_data)
    S = 1e6
    returns = np.log(stock_data[stock] / stock_data[stock].shift(1))
    returns = returns[1:]
    mu = np.mean(returns)
    sigma = np.std(returns)
    c = 0.99
    n = 1
    iterations = 100000

    model = ValueAtRiskMonteCarlo(S, mu, sigma, c, n, iterations)

    print(model.simulation())
