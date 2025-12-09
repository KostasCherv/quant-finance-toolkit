import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization

NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000
stocks = ["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"]

start_date = "2012-01-01"
end_date = "2017-01-01"


def download_data():
    stock_data = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)["Close"]

    return pd.DataFrame(stock_data)


def show_data(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["AAPL"], label="AAPL")
    plt.plot(data.index, data["WMT"], label="WMT")
    plt.plot(data.index, data["TSLA"], label="TSLA")
    plt.plot(data.index, data["GE"], label="GE")
    plt.plot(data.index, data["AMZN"], label="AMZN")
    plt.plot(data.index, data["DB"], label="DB")
    plt.legend()
    plt.show()


def calculate_returns(data):
    log_return = np.log(data / data.shift(1))
    return log_return.dropna()


def show_statistics(returns):
    #  mean of annualized returns
    print(returns.mean() * NUM_TRADING_DAYS)
    #  covariance of returns
    print(returns.cov() * NUM_TRADING_DAYS)


def show_mean_variance_plot(returns, weights):
    portfolio_returns = np.sum((returns.mean() * weights) * NUM_TRADING_DAYS)
    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights))
    )
    print("Portfolio Returns: ", portfolio_returns)
    print("Portfolio Volatility: ", portfolio_volatility)


def generate_portfolios(returns):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []
    for _ in range(NUM_PORTFOLIOS):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
        portfolio_weights.append(weights)
        portfolio_means.append(np.sum((returns.mean() * weights) * NUM_TRADING_DAYS))
        portfolio_risks.append(
            np.sqrt(
                np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights))
            )
        )
    return (
        np.array(portfolio_weights),
        np.array(portfolio_means),
        np.array(portfolio_risks),
    )


def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns / volatilities, marker="o")
    plt.grid(True)
    plt.xlabel("Expected Risk")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.show()


def statistics(weights, returns):
    portfolio_returns = np.sum((returns.mean() * weights) * NUM_TRADING_DAYS)
    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights))
    )
    sharpe_ratio = portfolio_returns / portfolio_volatility

    return np.array([portfolio_returns, portfolio_volatility, sharpe_ratio])


# minimize the negative sharpe ratio
def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]


# the sum of weights should be 1 (constraint)
# f(x) = 0 is the function to minimize
def optimize_portfolio(weights, returns):
    constraints = {"type": "eq", "fun": lambda weights: np.sum(weights) - 1}
    bounds = tuple[tuple[int, int], ...]((0, 1) for _ in range(len(stocks)))

    optimized_results = optimization.minimize(
        min_function_sharpe,
        weights[0],
        args=returns,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )
    return optimized_results


def print_optimized_portfolio(optimum, returns):
    print(f"Optimal Portfolio Weights: {optimum['x'].round(3)}")
    print(
        f"Expected return, volatility, and sharpe ratio: {statistics(optimum['x'].round(3), returns)}"
    )


def show_optimized_portfolio(opt, returns, portfolio_returns, portfolio_volatility):
    plt.figure(figsize=(10, 6))
    plt.scatter(
        portfolio_volatility,
        portfolio_returns,
        c=portfolio_returns / portfolio_volatility,
        marker="o",
    )
    plt.grid(True)
    plt.xlabel("Expected Risk")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.plot(
        statistics(opt["x"].round(3), returns)[1],
        statistics(opt["x"].round(3), returns)[0],
        "g*",
        markersize=15.0,
    )
    plt.show()


if __name__ == "__main__":
    data = download_data()
    returns = calculate_returns(data)

    p_weights, p_means, p_risks = generate_portfolios(returns)
    show_portfolios(p_means, p_risks)
    optimized_weights = optimize_portfolio(p_weights, returns)
    print_optimized_portfolio(optimized_weights, returns)
    show_optimized_portfolio(optimized_weights, returns, p_means, p_risks)
