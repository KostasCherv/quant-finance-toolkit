"""Example: Portfolio optimization using Markowitz model.

Note: This example requires internet connection to download stock data.
"""

from quant_finance_toolkit import (
    calculate_returns,
    download_stock_data,
    generate_portfolios,
    optimize_portfolio,
    print_optimized_portfolio,
    show_optimized_portfolio,
    show_portfolios,
)

# Portfolio stocks
stocks = ["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"]
start_date = "2012-01-01"
end_date = "2017-01-01"

print("=" * 50)
print("Portfolio Optimization Example")
print("=" * 50)
print(f"Stocks: {', '.join(stocks)}")
print(f"Date Range: {start_date} to {end_date}")
print()

# Download data
print("Downloading stock data...")
try:
    data = download_stock_data(stocks, start_date, end_date)
    print(f"Downloaded data for {len(data)} days")
    print()

    # Calculate returns
    returns = calculate_returns(data)
    print(f"Calculated returns for {len(returns)} periods")
    print()

    # Generate random portfolios
    print("Generating 10,000 random portfolios...")
    p_weights, p_means, p_risks = generate_portfolios(returns, num_portfolios=10000)
    print("Done!")
    print()

    # Show efficient frontier
    print("Efficient Frontier (random portfolios):")
    show_portfolios(p_means, p_risks, show_plot=False)  # Set to True to see plot
    print()

    # Optimize portfolio
    print("Optimizing portfolio (maximizing Sharpe ratio)...")
    optimized_weights = optimize_portfolio(returns)
    print_optimized_portfolio(optimized_weights, returns)
    print()

    # Show optimized portfolio on efficient frontier
    print("Efficient Frontier with Optimal Portfolio:")
    show_optimized_portfolio(
        optimized_weights, returns, p_means, p_risks, show_plot=False
    )  # Set to True to see plot

except Exception as e:
    print(f"Error: {e}")
    print("Make sure you have an internet connection and the tickers are valid.")
