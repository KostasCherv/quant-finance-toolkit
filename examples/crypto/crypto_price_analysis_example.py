"""Example: Cryptocurrency price analysis and modeling.

This example demonstrates:
- Downloading and plotting top 5 cryptocurrency prices
- Running GBM simulations for price forecasting
- Analyzing volatility across cryptocurrencies
- Comparing crypto vs traditional stocks
"""

from quant_finance_toolkit.crypto import (
    compare_crypto_stocks,
    crypto_price_simulation,
    crypto_volatility_analysis,
)
from quant_finance_toolkit.crypto.visualization import (
    plot_crypto_prices,
    plot_crypto_returns,
    plot_crypto_volatility_comparison,
)

# Top 5 cryptocurrencies
TOP_5_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD"]

# Date range for analysis
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"

print("=" * 70)
print("Cryptocurrency Price Analysis Example")
print("=" * 70)
print(f"Cryptocurrencies: {', '.join(TOP_5_CRYPTOS)}")
print(f"Date Range: {START_DATE} to {END_DATE}")
print()

try:
    # 1. Plot normalized price history
    print("1. Plotting normalized price history...")
    plot_crypto_prices(
        TOP_5_CRYPTOS, START_DATE, END_DATE, normalize=True, show_plot=True
    )
    print("   ✓ Price comparison plot generated")
    print()

    # 2. Plot daily returns
    print("2. Plotting daily returns...")
    plot_crypto_returns(TOP_5_CRYPTOS, START_DATE, END_DATE, show_plot=True)
    print("   ✓ Returns plot generated")
    print()

    # 3. Volatility analysis
    print("3. Analyzing volatility across cryptocurrencies...")
    volatility_df = crypto_volatility_analysis(TOP_5_CRYPTOS, START_DATE, END_DATE)
    print("\nVolatility Metrics:")
    print(volatility_df.round(4))
    print()

    # Plot volatility comparison
    plot_crypto_volatility_comparison(
        volatility_df, metric="annualized_volatility", show_plot=True
    )
    print("   ✓ Volatility comparison plot generated")
    print()

    # 4. Price simulation for BTC
    print("4. Running GBM price simulation for BTC-USD...")
    simulation_results, stats = crypto_price_simulation(
        "BTC-USD", START_DATE, END_DATE, T=1.0, num_simulations=1000, show_plot=True
    )
    print("\nSimulation Statistics:")
    print(f"  Current Price: ${stats['current_price']:,.2f}")
    print(f"  Historical Annualized Return: {stats['historical_mu']:.2%}")
    print(f"  Historical Annualized Volatility: {stats['historical_sigma']:.2%}")
    print(f"  Mean Forecasted Price (1 year): ${stats['mean_final_price']:,.2f}")
    print(f"  Price Range: ${stats['min_price']:,.2f} - ${stats['max_price']:,.2f}")
    print()

    # 5. Compare crypto vs stocks
    print("5. Comparing cryptocurrencies vs traditional stocks...")
    stock_tickers = ["AAPL", "MSFT", "GOOGL"]
    comparison = compare_crypto_stocks(
        TOP_5_CRYPTOS, stock_tickers, START_DATE, END_DATE, show_plot=True
    )
    print("\nPerformance Comparison:")
    print(comparison.round(4))
    print()

    print("=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    print("\nKey Insights:")
    print("- Cryptocurrencies generally show higher volatility than traditional stocks")
    print("- Crypto returns can be more extreme (both positive and negative)")
    print("- Correlation between cryptos is typically high")
    print("- GBM simulations can help forecast potential price ranges")

except Exception as e:
    print(f"Error: {e}")
    print("Make sure you have an internet connection and the tickers are valid.")
