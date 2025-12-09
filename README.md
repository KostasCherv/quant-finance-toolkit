# Quantitative Finance Toolkit

A comprehensive Python toolkit for quantitative finance, featuring pricing models, portfolio optimization, risk management, and stochastic modeling. Built with modern Python best practices and designed to support both traditional finance and cryptocurrency applications.

## Features

### Pricing Models
- **Bond Pricing**: Zero-coupon and coupon bonds with discrete and continuous compounding
- **Option Pricing**: Black-Scholes analytical pricing and Monte Carlo simulation
- **Time Value of Money**: Present and future value calculations

### Portfolio Optimization
- **Markowitz Model**: Efficient frontier analysis and portfolio optimization
- **CAPM**: Capital Asset Pricing Model for beta calculation and expected returns

### Risk Management
- **Value at Risk (VaR)**: Analytical and Monte Carlo methods
- **Risk Metrics**: Portfolio risk analysis and volatility calculations

### Stochastic Models
- **Geometric Brownian Motion (GBM)**: Stock price modeling
- **Vasicek Model**: Interest rate modeling and bond pricing
- **Ornstein-Uhlenbeck Process**: Mean-reverting stochastic processes
- **Monte Carlo Simulations**: Flexible simulation framework

### Data Utilities
- **Market Data**: Yahoo Finance integration for stock and crypto price data
- **Data Processing**: Returns calculation and statistical analysis

### Cryptocurrency Analysis
- **Crypto Price Modeling**: GBM simulations for cryptocurrency price forecasting
- **Volatility Analysis**: Compare volatility across multiple cryptocurrencies
- **Crypto Portfolio Optimization**: Markowitz optimization for crypto portfolios
- **Crypto Risk Management**: Value at Risk (VaR) for crypto positions and portfolios
- **Crypto vs Stocks Comparison**: Compare performance metrics between crypto and traditional assets
- **Visualization**: Price charts, correlation heatmaps, volatility comparisons

### Interactive Visualizations 🎨
- **Plotly Integration**: Professional interactive charts with hover tooltips, zoom, and export
- **Efficient Frontier**: Interactive risk-return analysis with optimal portfolio highlighting
- **Time Series**: Interactive cryptocurrency price comparisons with date range selectors
- **Correlation Heatmaps**: Interactive correlation matrices with detailed hover information
- **Monte Carlo Simulations**: Interactive GBM simulations with confidence bands
- **Volatility Comparisons**: Interactive bar charts with color-coded metrics

## Showcase

### Interactive Visualizations

The toolkit includes professional-grade interactive visualizations built with Plotly, featuring:

- **Hover Tooltips**: Detailed information on hover
- **Zoom & Pan**: Interactive exploration of data
- **Export Options**: Save as HTML, PNG, or SVG
- **Professional Styling**: Clean, modern design
- **Responsive Layouts**: Adapts to different screen sizes

#### Key Visualizations:

1. **Interactive Efficient Frontier**
   - Risk-return scatter plot with Sharpe ratio color-coding
   - Optimal portfolio highlighted with star marker
   - Hover to see exact return, volatility, and Sharpe ratio values

2. **Interactive Cryptocurrency Price Comparison**
   - Normalized price history with date range selector
   - Multiple cryptocurrencies on one chart
   - Range slider for easy time period selection

3. **Interactive Correlation Heatmap**
   - Color-coded correlation matrix
   - Hover to see correlation values between asset pairs
   - Professional red-blue color scheme

4. **Interactive Volatility Comparison**
   - Bar chart with color gradients
   - Hover tooltips with exact values
   - Easy comparison across multiple assets

5. **Interactive GBM Simulation**
   - Multiple simulation paths with confidence bands
   - Mean path and 95% confidence intervals
   - Interactive exploration of price forecasts

**Try the Visualization Gallery:**
```bash
uv run python examples/visualization_gallery.py
```

### Example Outputs

The toolkit generates publication-quality visualizations suitable for:
- Portfolio analysis reports
- Risk assessment presentations
- Academic research papers
- Investment strategy documentation
- Educational materials

## Installation

This project uses [UV](https://github.com/astral-sh/uv) for fast and reliable dependency management.

### Prerequisites
- Python 3.10 or higher
- UV package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd quant-finance-toolkit
```

2. Install dependencies using UV:
```bash
uv sync
```

3. Activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

## Quick Start

### Bond Pricing

```python
from quant_finance_toolkit import ZeroCouponBond, CouponBond

# Zero-coupon bond
bond = ZeroCouponBond(principal=1000, maturity=2, interest_rate=4)
price = bond.calculate_price()
print(f"Bond Price: ${price:.2f}")

# Coupon bond
coupon_bond = CouponBond(principal=1000, rate=10, maturity=3, interest_rate=4)
price = coupon_bond.calculate_price()
print(f"Bond Price: ${price:.2f}")
```

### Option Pricing

```python
from quant_finance_toolkit import call_option_price, OptionPriceMonteCarlo

# Black-Scholes
call_price = call_option_price(S=100, E=100, T=1, rf=0.05, sigma=0.2)
print(f"Call Option Price: ${call_price:.2f}")

# Monte Carlo
mc_model = OptionPriceMonteCarlo(S0=100, E=100, T=1, rf=0.05, sigma=0.2, iterations=10000)
call_price_mc = mc_model.call_option_price()
print(f"Monte Carlo Call Price: ${call_price_mc:.2f}")
```

### Portfolio Optimization

```python
from quant_finance_toolkit import (
    download_stock_data,
    calculate_returns,
    generate_portfolios,
    optimize_portfolio,
)

# Download data
stocks = ["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"]
data = download_stock_data(stocks, "2012-01-01", "2017-01-01")

# Calculate returns
returns = calculate_returns(data)

# Generate portfolios and optimize
p_weights, p_means, p_risks = generate_portfolios(returns, num_portfolios=10000)
optimized = optimize_portfolio(returns)
```

### Value at Risk

```python
from quant_finance_toolkit import value_at_risk_n, ValueAtRiskMonteCarlo

# Analytical VaR
var = value_at_risk_n(position=1000000, c=0.99, mu=0.001, sigma=0.02, n=1)
print(f"VaR (1 day, 99%): ${var:.2f}")

# Monte Carlo VaR
mc_var = ValueAtRiskMonteCarlo(
    S=1000000, mu=0.001, sigma=0.02, c=0.99, n=1, iterations=100000
)
var_mc = mc_var.simulation()
print(f"Monte Carlo VaR: ${var_mc:.2f}")
```

### Cryptocurrency Analysis

```python
from quant_finance_toolkit import (
    download_crypto_data,
    crypto_price_simulation,
    crypto_volatility_analysis,
    optimize_crypto_portfolio,
    crypto_var_analysis,
    plot_crypto_prices,
)

# Download crypto data
cryptos = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD"]
data = download_crypto_data(cryptos, "2020-01-01", "2024-01-01")

# Plot normalized prices
plot_crypto_prices(cryptos, "2020-01-01", "2024-01-01", normalize=True)

# Price simulation
sim_results, stats = crypto_price_simulation(
    "BTC-USD", "2020-01-01", "2024-01-01", T=1.0, num_simulations=1000
)

# Volatility analysis
volatility_df = crypto_volatility_analysis(cryptos, "2020-01-01", "2024-01-01")

# Portfolio optimization
portfolio_result = optimize_crypto_portfolio(
    cryptos, "2020-01-01", "2024-01-01", num_portfolios=10000
)

# VaR analysis
var_result = crypto_var_analysis(
    "BTC-USD", position=100000, start_date="2020-01-01", 
    end_date="2024-01-01", confidence_level=0.99
)
```

### Interactive Visualizations

```python
from quant_finance_toolkit import (
    plot_interactive_efficient_frontier,
    plot_interactive_crypto_prices,
    plot_interactive_correlation_heatmap,
    plot_interactive_volatility_comparison,
    plot_interactive_gbm_simulation,
)

# Interactive efficient frontier
fig = plot_interactive_efficient_frontier(
    portfolio_returns, portfolio_volatility,
    optimal_stats=(optimal_return, optimal_vol),
    optimal_weights=optimal_weights,
    asset_names=["AAPL", "MSFT", "GOOGL"]
)

# Interactive crypto price comparison
fig = plot_interactive_crypto_prices(
    ["BTC-USD", "ETH-USD"], "2020-01-01", "2024-01-01", normalize=True
)

# Interactive correlation heatmap
fig = plot_interactive_correlation_heatmap(correlation_matrix)

# Interactive volatility comparison
fig = plot_interactive_volatility_comparison(volatility_df)

# Interactive GBM simulation
fig = plot_interactive_gbm_simulation(time, price_paths)
```

## Project Structure

```
quant-finance-toolkit/
├── src/
│   └── quant_finance_toolkit/
│       ├── pricing/          # Bond and option pricing
│       ├── models/           # Stochastic models
│       ├── portfolio/        # Portfolio optimization
│       ├── risk/             # Risk management
│       ├── data/              # Data fetching utilities
│       ├── utils/             # Visualization utilities
│       └── crypto/            # Crypto-specific models and analysis
│           ├── models.py      # Price simulation, volatility analysis
│           ├── portfolio.py   # Portfolio optimization
│           ├── risk.py        # VaR calculations
│           └── visualization.py  # Plotting utilities
├── examples/
│   ├── traditional_finance/   # Traditional finance examples
│   └── crypto/                # Cryptocurrency examples
├── tests/                     # Test suite
└── pyproject.toml            # Project configuration
```

## Examples

### Traditional Finance

See the `examples/traditional_finance/` directory for complete working examples:
- `bond_pricing_example.py` - Bond pricing demonstrations
- `option_pricing_example.py` - Option pricing comparisons
- `portfolio_optimization_example.py` - Portfolio optimization workflow

### Cryptocurrency

See the `examples/crypto/` directory for cryptocurrency analysis examples:
- `crypto_price_analysis_example.py` - Price modeling, volatility analysis, crypto vs stocks comparison
- `crypto_portfolio_example.py` - Portfolio optimization with efficient frontier and correlation heatmap
- `crypto_risk_example.py` - VaR analysis for individual cryptos and portfolios

### Visualization Gallery

See `examples/visualization_gallery.py` for a comprehensive showcase of all interactive visualizations:
- Interactive efficient frontier with optimal portfolio
- Interactive cryptocurrency price comparisons
- Interactive correlation heatmaps
- Interactive volatility comparisons
- Interactive GBM simulations with confidence bands

Run examples:
```bash
# Traditional finance
uv run python examples/traditional_finance/bond_pricing_example.py

# Cryptocurrency
uv run python examples/crypto/crypto_price_analysis_example.py
uv run python examples/crypto/crypto_portfolio_example.py
uv run python examples/crypto/crypto_risk_example.py

# Interactive visualization gallery
uv run python examples/visualization_gallery.py
```

## Dependencies

- **numpy**: Numerical computations
- **pandas**: Data manipulation and analysis
- **matplotlib**: Static visualization
- **plotly**: Interactive visualization (new!)
- **scipy**: Scientific computing and optimization
- **yfinance**: Market data fetching

## Development

### Installing Development Dependencies

```bash
uv sync --extra dev
```

### Code Quality

The project follows Python best practices:
- Type hints throughout
- Comprehensive docstrings
- Modular architecture
- Clean separation of concerns

## Future Roadmap

- [x] Cryptocurrency-specific models and examples
- [ ] Additional stochastic models (Heston, Hull-White)
- [ ] Backtesting framework
- [ ] Performance benchmarking tools
- [ ] Interactive web dashboard
- [ ] Comprehensive test suite
- [ ] Additional risk metrics (CVaR, Expected Shortfall)
- [ ] Crypto derivatives pricing
- [ ] Real-time crypto data streaming

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Author

KostasCherv - kostasxerv@gmail.com

## Acknowledgments

This toolkit implements fundamental quantitative finance models commonly used in the industry and academia.
