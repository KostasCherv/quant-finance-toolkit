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


def value_at_risk_n(position, c, mu, sigma, n):
    var = position * (mu * n - norm.ppf(1 - c) * sigma * np.sqrt(n))
    return var


if __name__ == "__main__":
    stock = "AAPL"
    start_date = dt.datetime(2014, 1, 1)
    end_date = dt.datetime(2018, 1, 1)
    stock_data = download_data(stock, start_date, end_date)
    print(stock_data)

    # calculate the returns
    returns = np.log(stock_data[stock] / stock_data[stock].shift(1))
    returns = returns[1:]
    mu = np.mean(returns)
    sigma = np.std(returns)
    print(f"The mean is {mu} and the standard deviation is {sigma}")

    # calculate the value at risk
    position = 1e6
    c = 0.99
    var = value_at_risk_n(position, c, mu, sigma, 1)
    print("Value at risk is: $%0.2f" % var)

    # calculate the value at risk for 10 days
    n = 10
    var_n = value_at_risk_n(position, c, mu, sigma, n)
    print(f"Value at risk is after {n} days: $%0.2f" % var_n)
