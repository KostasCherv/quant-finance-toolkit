"""Example: Cryptocurrency portfolio optimization.

This example demonstrates:
- Optimizing a crypto portfolio using Markowitz model
- Generating efficient frontier
- Analyzing correlations between cryptocurrencies
- Finding optimal portfolio weights
"""

from quant_finance_toolkit.crypto import (
    crypto_correlation_matrix,
    optimize_crypto_portfolio,
)
from quant_finance_toolkit.crypto.visualization import plot_crypto_correlation_heatmap

# Top 5 cryptocurrencies
TOP_5_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD"]

# Date range for analysis
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"

print("=" * 70)
print("Cryptocurrency Portfolio Optimization Example")
print("=" * 70)
print(f"Cryptocurrencies: {', '.join(TOP_5_CRYPTOS)}")
print(f"Date Range: {START_DATE} to {END_DATE}")
print()

try:
    # 1. Correlation analysis
    print("1. Analyzing correlations between cryptocurrencies...")
    correlation_matrix = crypto_correlation_matrix(
        TOP_5_CRYPTOS, START_DATE, END_DATE, show_plot=True
    )
    print("\nCorrelation Matrix:")
    print(correlation_matrix.round(3))
    print()

    # Plot correlation heatmap
    plot_crypto_correlation_heatmap(correlation_matrix, show_plot=True)
    print("   ✓ Correlation heatmap generated")
    print()

    # 2. Portfolio optimization
    print("2. Optimizing cryptocurrency portfolio...")
    print("   Generating 10,000 random portfolios...")
    result = optimize_crypto_portfolio(
        TOP_5_CRYPTOS, START_DATE, END_DATE, num_portfolios=10000, show_plot=True
    )
    print("   ✓ Optimization complete")
    print()

    # Display results
    print("Optimal Portfolio Weights:")
    for ticker, weight in result["optimized_weights"].items():
        print(f"  {ticker}: {weight:.2%}")

    print("\nPortfolio Statistics:")
    stats = result["portfolio_stats"]
    print(f"  Expected Return (Annualized): {stats['expected_return']:.2%}")
    print(f"  Expected Volatility (Annualized): {stats['volatility']:.2%}")
    print(f"  Sharpe Ratio: {stats['sharpe_ratio']:.3f}")
    print()

    # 3. Efficient frontier visualization
    print("3. Generating efficient frontier plot...")
    from quant_finance_toolkit.portfolio.markowitz import show_optimized_portfolio

    show_optimized_portfolio(
        result["optimization_result"],
        result["returns"],
        result["all_portfolios"]["returns"],
        result["all_portfolios"]["risks"],
        show_plot=True,
    )
    print("   ✓ Efficient frontier plot generated")
    print()

    print("=" * 70)
    print("Portfolio Optimization Complete!")
    print("=" * 70)
    print("\nKey Insights:")
    print("- Optimal portfolio weights maximize Sharpe ratio")
    print("- Diversification reduces portfolio risk")
    print("- High correlations between cryptos limit diversification benefits")
    print("- Efficient frontier shows risk-return trade-offs")

except Exception as e:
    print(f"Error: {e}")
    print("Make sure you have an internet connection and the tickers are valid.")
