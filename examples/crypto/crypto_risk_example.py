"""Example: Cryptocurrency Value at Risk (VaR) analysis.

This example demonstrates:
- Calculating VaR for individual cryptocurrencies
- Portfolio-level VaR calculation
- Comparing analytical vs Monte Carlo VaR methods
- Risk metrics for crypto positions
"""

from quant_finance_toolkit.crypto import crypto_portfolio_var, crypto_var_analysis

# Top 5 cryptocurrencies
TOP_5_CRYPTOS = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD"]

# Date range for analysis
START_DATE = "2020-01-01"
END_DATE = "2024-01-01"

# Position sizes
POSITION_SIZE = 100000  # $100,000 per crypto
CONFIDENCE_LEVEL = 0.99  # 99% confidence
TIME_HORIZON_DAYS = 1  # 1-day VaR

print("=" * 70)
print("Cryptocurrency Value at Risk (VaR) Analysis Example")
print("=" * 70)
print(f"Cryptocurrencies: {', '.join(TOP_5_CRYPTOS)}")
print(f"Date Range: {START_DATE} to {END_DATE}")
print(f"Position Size: ${POSITION_SIZE:,} per crypto")
print(f"Confidence Level: {CONFIDENCE_LEVEL*100}%")
print(f"Time Horizon: {TIME_HORIZON_DAYS} day(s)")
print()

try:
    # 1. Individual crypto VaR
    print("1. Calculating VaR for individual cryptocurrencies...")
    print()
    individual_vars = {}

    for crypto in TOP_5_CRYPTOS:
        print(f"   Analyzing {crypto}...")
        var_result = crypto_var_analysis(
            crypto,
            POSITION_SIZE,
            START_DATE,
            END_DATE,
            confidence_level=CONFIDENCE_LEVEL,
            days=TIME_HORIZON_DAYS,
            use_monte_carlo=True,
            mc_iterations=100000,
        )

        individual_vars[crypto] = var_result

        print(f"     Analytical VaR: ${var_result['analytical_var']:,.2f}")
        print(f"     Monte Carlo VaR: ${var_result['monte_carlo_var']:,.2f}")
        print(f"     Difference: ${var_result['var_difference']:,.2f}")
        print(f"     Annualized Volatility: {var_result['annualized_volatility']:.2%}")
        print()

    # Summary table
    print("Individual VaR Summary:")
    print("-" * 70)
    print(f"{'Crypto':<12} {'Analytical VaR':<18} {'MC VaR':<18} {'Volatility':<15}")
    print("-" * 70)
    for crypto, var_result in individual_vars.items():
        print(
            f"{crypto:<12} ${var_result['analytical_var']:>12,.2f}  "
            f"${var_result['monte_carlo_var']:>12,.2f}  "
            f"{var_result['annualized_volatility']:>12.2%}"
        )
    print()

    # 2. Portfolio VaR
    print("2. Calculating portfolio-level VaR...")
    print("   Using equal weights (20% each)...")
    print()

    equal_weights = [0.2] * len(TOP_5_CRYPTOS)
    total_portfolio_value = POSITION_SIZE * len(TOP_5_CRYPTOS)

    portfolio_var_result = crypto_portfolio_var(
        TOP_5_CRYPTOS,
        equal_weights,
        total_portfolio_value,
        START_DATE,
        END_DATE,
        confidence_level=CONFIDENCE_LEVEL,
        days=TIME_HORIZON_DAYS,
    )

    print("Portfolio VaR Results:")
    print(f"  Total Portfolio Value: ${total_portfolio_value:,}")
    print(f"  Portfolio VaR: ${portfolio_var_result['portfolio_var']:,.2f}")
    print(f"  Portfolio Volatility: {portfolio_var_result['portfolio_volatility']:.2%}")
    print(
        f"  Portfolio Expected Return: {portfolio_var_result['portfolio_mean_return']:.2%}"
    )
    print()

    # Compare individual vs portfolio
    print("3. Comparing individual vs portfolio risk...")
    sum_individual_vars = sum([v["analytical_var"] for v in individual_vars.values()])
    portfolio_var = portfolio_var_result["portfolio_var"]

    print(f"  Sum of Individual VaRs: ${sum_individual_vars:,.2f}")
    print(f"  Portfolio VaR: ${portfolio_var:,.2f}")
    print(f"  Diversification Benefit: ${sum_individual_vars - portfolio_var:,.2f}")
    print(f"  Diversification Ratio: {(sum_individual_vars / portfolio_var):.2f}x")
    print()

    # Individual VaRs in portfolio
    print("Individual VaRs (if held separately):")
    for crypto, var_result in portfolio_var_result["individual_vars"].items():
        print(f"  {crypto}: ${var_result:,.2f}")
    print()

    print("=" * 70)
    print("VaR Analysis Complete!")
    print("=" * 70)
    print("\nKey Insights:")
    print("- Cryptocurrencies have high VaR due to high volatility")
    print("- Portfolio diversification reduces overall risk")
    print("- Analytical and Monte Carlo VaR methods give similar results")
    print("- Correlation between cryptos affects portfolio VaR")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
    print("Make sure you have an internet connection and the tickers are valid.")
