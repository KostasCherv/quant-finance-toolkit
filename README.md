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
- **Market Data**: Yahoo Finance integration for stock price data
- **Data Processing**: Returns calculation and statistical analysis

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
│       └── crypto/            # Crypto-specific models (future)
├── examples/
│   └── traditional_finance/   # Usage examples
├── tests/                     # Test suite
└── pyproject.toml            # Project configuration
```

## Examples

See the `examples/traditional_finance/` directory for complete working examples:
- `bond_pricing_example.py` - Bond pricing demonstrations
- `option_pricing_example.py` - Option pricing comparisons
- `portfolio_optimization_example.py` - Portfolio optimization workflow

Run examples:
```bash
uv run python examples/traditional_finance/bond_pricing_example.py
```

## Dependencies

- **numpy**: Numerical computations
- **pandas**: Data manipulation and analysis
- **matplotlib**: Visualization
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

- [ ] Cryptocurrency-specific models and examples
- [ ] Additional stochastic models (Heston, Hull-White)
- [ ] Backtesting framework
- [ ] Performance benchmarking tools
- [ ] Interactive web dashboard
- [ ] Comprehensive test suite
- [ ] Additional risk metrics (CVaR, Expected Shortfall)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Author

KostasCherv - kostasxerv@gmail.com

## Acknowledgments

This toolkit implements fundamental quantitative finance models commonly used in the industry and academia.
