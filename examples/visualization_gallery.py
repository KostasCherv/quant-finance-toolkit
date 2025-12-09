"""Visualization Gallery - Interactive Plotly Demonstrations.

This example showcases all interactive visualizations available in the toolkit.
Each visualization demonstrates professional-quality plots with hover tooltips,
zoom, pan, and export capabilities.

Run this script to see:
- Interactive Efficient Frontier with optimal portfolio
- Interactive Cryptocurrency Price Comparisons
- Interactive Correlation Heatmaps
- Interactive Volatility Comparisons
- Interactive GBM Simulations with confidence bands
"""

from quant_finance_toolkit.crypto import (
    crypto_correlation_matrix,
    crypto_volatility_analysis,
    optimize_crypto_portfolio,
)
from quant_finance_toolkit.crypto.models import crypto_price_simulation
from quant_finance_toolkit.data import download_crypto_data, download_stock_data
from quant_finance_toolkit.models.stochastic import simulate_gbm
from quant_finance_toolkit.portfolio.markowitz import (
    calculate_returns,
    generate_portfolios,
    optimize_portfolio,
    statistics,
)
from quant_finance_toolkit.utils.interactive import (
    plot_interactive_correlation_heatmap,
    plot_interactive_crypto_prices,
    plot_interactive_efficient_frontier,
    plot_interactive_gbm_simulation,
    plot_interactive_volatility_comparison,
)

# Configuration
TOP_5_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD"]
STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"

print("=" * 80)
print("Quantitative Finance Toolkit - Interactive Visualization Gallery")
print("=" * 80)
print("\nThis gallery demonstrates interactive Plotly visualizations with:")
print("  • Hover tooltips for detailed information")
print("  • Zoom and pan capabilities")
print("  • Export options (PNG, HTML)")
print("  • Professional styling and color schemes")
print("\n" + "=" * 80 + "\n")

try:
    # ========================================================================
    # 1. INTERACTIVE EFFICIENT FRONTIER
    # ========================================================================
    print("1. Generating Interactive Efficient Frontier...")
    print("   Demonstrates: Portfolio optimization, risk-return trade-offs")
    print()

    # Download stock data
    stock_data = download_stock_data(STOCKS, START_DATE, END_DATE)
    returns = calculate_returns(stock_data)

    # Generate portfolios
    p_weights, p_means, p_risks = generate_portfolios(returns, num_portfolios=10000)

    # Optimize portfolio
    opt = optimize_portfolio(returns)
    optimal_stats = statistics(opt["x"], returns)

    # Create interactive plot
    fig_ef = plot_interactive_efficient_frontier(
        portfolio_returns=p_means,
        portfolio_volatility=p_risks,
        optimal_stats=(optimal_stats[0], optimal_stats[1]),
        optimal_weights=opt["x"],
        asset_names=STOCKS,
        title="Interactive Efficient Frontier - Stock Portfolio",
        show_plot=True,
    )
    print("   ✓ Interactive efficient frontier generated")
    print("   → Hover over points to see return, volatility, and Sharpe ratio")
    print("   → Red star indicates optimal portfolio")
    print()

    # ========================================================================
    # 2. INTERACTIVE CRYPTOCURRENCY PRICE COMPARISON
    # ========================================================================
    print("2. Generating Interactive Cryptocurrency Price Comparison...")
    print("   Demonstrates: Time series visualization, normalized comparisons")
    print()

    fig_crypto = plot_interactive_crypto_prices(
        crypto_tickers=TOP_5_CRYPTOS,
        start_date=START_DATE,
        end_date=END_DATE,
        normalize=True,
        title="Interactive Cryptocurrency Price Comparison (Normalized)",
        show_plot=True,
    )
    print("   ✓ Interactive crypto price comparison generated")
    print("   → Use date range selector for different time periods")
    print("   → Hover to see exact dates and prices")
    print("   → Drag on range slider to zoom")
    print()

    # ========================================================================
    # 3. INTERACTIVE CORRELATION HEATMAP
    # ========================================================================
    print("3. Generating Interactive Correlation Heatmap...")
    print("   Demonstrates: Correlation analysis, heatmap visualization")
    print()

    # Get correlation matrix
    crypto_data = download_crypto_data(TOP_5_CRYPTOS, START_DATE, END_DATE)
    crypto_returns = calculate_returns(crypto_data)
    corr_matrix = crypto_correlation_matrix(TOP_5_CRYPTOS, START_DATE, END_DATE)

    fig_heatmap = plot_interactive_correlation_heatmap(
        correlation_matrix=corr_matrix,
        title="Interactive Cryptocurrency Correlation Heatmap",
        show_plot=True,
    )
    print("   ✓ Interactive correlation heatmap generated")
    print("   → Hover to see correlation values between pairs")
    print("   → Red indicates positive correlation, blue indicates negative")
    print()

    # ========================================================================
    # 4. INTERACTIVE VOLATILITY COMPARISON
    # ========================================================================
    print("4. Generating Interactive Volatility Comparison...")
    print("   Demonstrates: Volatility metrics, comparative analysis")
    print()

    volatility_df = crypto_volatility_analysis(TOP_5_CRYPTOS, START_DATE, END_DATE)

    fig_vol = plot_interactive_volatility_comparison(
        volatility_data=volatility_df,
        metric="annualized_volatility",
        title="Interactive Cryptocurrency Volatility Comparison",
        show_plot=True,
    )
    print("   ✓ Interactive volatility comparison generated")
    print("   → Hover to see exact volatility values")
    print("   → Colors indicate relative volatility levels")
    print()

    # ========================================================================
    # 5. INTERACTIVE GBM SIMULATION
    # ========================================================================
    print("5. Generating Interactive GBM Simulation...")
    print("   Demonstrates: Monte Carlo simulation, confidence intervals")
    print()

    # Run crypto price simulation
    sim_results, stats = crypto_price_simulation(
        "BTC-USD", START_DATE, END_DATE, T=1.0, num_simulations=1000, show_plot=False
    )

    # Extract time and price paths
    time = sim_results.index.values
    price_paths = sim_results.values.T  # Transpose to [num_simulations, time_steps]

    fig_gbm = plot_interactive_gbm_simulation(
        time=time,
        price_paths=price_paths,
        title="Interactive GBM Simulation - BTC Price Forecast",
        show_plot=True,
    )
    print("   ✓ Interactive GBM simulation generated")
    print("   → Multiple simulation paths shown in light blue")
    print("   → Red line shows mean path")
    print("   → Dashed lines show 95% confidence interval")
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("=" * 80)
    print("Visualization Gallery Complete!")
    print("=" * 80)
    print("\nAll interactive visualizations have been generated.")
    print("\nKey Features Demonstrated:")
    print("  ✓ Professional styling with Plotly")
    print("  ✓ Interactive hover tooltips with detailed information")
    print("  ✓ Zoom and pan capabilities")
    print("  ✓ Export options (use toolbar)")
    print("  ✓ Responsive design")
    print("  ✓ Color-coded visualizations")
    print("\nThese visualizations can be exported as:")
    print("  • HTML files (interactive)")
    print("  • PNG images (static)")
    print("  • SVG images (vector)")
    print("\n" + "=" * 80)

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure you have:")
    print("  • Internet connection for data download")
    print("  • Valid ticker symbols")
    print("  • Plotly installed: uv sync")
    import traceback

    traceback.print_exc()
