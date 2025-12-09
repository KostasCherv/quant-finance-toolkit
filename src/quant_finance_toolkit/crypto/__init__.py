"""Crypto-specific financial models and utilities.

This module provides cryptocurrency-specific implementations of quantitative finance models:
- Price modeling and simulation using stochastic processes
- Volatility analysis and comparison
- Portfolio optimization for crypto assets
- Risk management (VaR) for crypto portfolios
- Visualization tools for crypto data analysis
"""

from .models import (
    compare_crypto_stocks,
    crypto_price_simulation,
    crypto_volatility_analysis,
)
from .portfolio import crypto_correlation_matrix, optimize_crypto_portfolio
from .risk import crypto_portfolio_var, crypto_var_analysis
from .visualization import (
    plot_crypto_correlation_heatmap,
    plot_crypto_prices,
    plot_crypto_returns,
    plot_crypto_volatility_comparison,
)

__all__ = [
    # Models
    "crypto_price_simulation",
    "crypto_volatility_analysis",
    "compare_crypto_stocks",
    # Portfolio
    "optimize_crypto_portfolio",
    "crypto_correlation_matrix",
    # Risk
    "crypto_var_analysis",
    "crypto_portfolio_var",
    # Visualization
    "plot_crypto_prices",
    "plot_crypto_returns",
    "plot_crypto_correlation_heatmap",
    "plot_crypto_volatility_comparison",
]
