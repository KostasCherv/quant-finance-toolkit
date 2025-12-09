"""Quantitative Finance Toolkit.

A comprehensive toolkit for quantitative finance including:
- Bond and option pricing
- Portfolio optimization
- Risk management (VaR)
- Stochastic models (GBM, Vasicek, Ornstein-Uhlenbeck)
- Monte Carlo simulations
- Cryptocurrency analysis and modeling
"""

__version__ = "0.1.0"

# Pricing module
from .pricing import (
    CouponBond,
    OptionPriceMonteCarlo,
    ZeroCouponBond,
    call_option_price,
    future_continuous_value,
    future_discrete_value,
    present_continuous_value,
    present_discrete_value,
    put_option_price,
)

# Models module
from .models import (
    generate_ornstein_uhlenbeck,
    monte_carlo_bond_pricing,
    simulate_gbm,
    stock_price_monte_carlo,
    vasicek_model,
    wiener_process,
)

# Portfolio module
from .portfolio import (
    CAPM,
    calculate_returns,
    generate_portfolios,
    optimize_portfolio,
    print_optimized_portfolio,
    show_optimized_portfolio,
    show_portfolios,
)

# Risk module
from .risk import ValueAtRiskMonteCarlo, value_at_risk_n

# Data module
from .data import download_crypto_data, download_stock_data

# Crypto module (optional import to avoid circular dependencies)
try:
    from .crypto import (
        compare_crypto_stocks,
        crypto_correlation_matrix,
        crypto_portfolio_var,
        crypto_price_simulation,
        crypto_var_analysis,
        crypto_volatility_analysis,
        optimize_crypto_portfolio,
        plot_crypto_correlation_heatmap,
        plot_crypto_prices,
        plot_crypto_returns,
        plot_crypto_volatility_comparison,
    )

    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Utils module
from .utils import (
    plot_gbm,
    plot_interactive_correlation_heatmap,
    plot_interactive_crypto_prices,
    plot_interactive_efficient_frontier,
    plot_interactive_gbm_simulation,
    plot_interactive_volatility_comparison,
    plot_process,
    plot_wiener_process,
)

__all__ = [
    # Version
    "__version__",
    # Pricing
    "ZeroCouponBond",
    "CouponBond",
    "call_option_price",
    "put_option_price",
    "OptionPriceMonteCarlo",
    "future_discrete_value",
    "present_discrete_value",
    "future_continuous_value",
    "present_continuous_value",
    # Models
    "wiener_process",
    "simulate_gbm",
    "generate_ornstein_uhlenbeck",
    "vasicek_model",
    "monte_carlo_bond_pricing",
    "stock_price_monte_carlo",
    # Portfolio
    "CAPM",
    "calculate_returns",
    "generate_portfolios",
    "optimize_portfolio",
    "print_optimized_portfolio",
    "show_optimized_portfolio",
    "show_portfolios",
    # Risk
    "value_at_risk_n",
    "ValueAtRiskMonteCarlo",
    # Data
    "download_stock_data",
    "download_crypto_data",
    # Utils
    "plot_wiener_process",
    "plot_gbm",
    "plot_process",
    # Interactive Visualizations
    "plot_interactive_efficient_frontier",
    "plot_interactive_crypto_prices",
    "plot_interactive_correlation_heatmap",
    "plot_interactive_volatility_comparison",
    "plot_interactive_gbm_simulation",
]

# Conditionally add crypto exports if available
if CRYPTO_AVAILABLE:
    __all__.extend(
        [
            # Crypto Models
            "crypto_price_simulation",
            "crypto_volatility_analysis",
            "compare_crypto_stocks",
            # Crypto Portfolio
            "optimize_crypto_portfolio",
            "crypto_correlation_matrix",
            # Crypto Risk
            "crypto_var_analysis",
            "crypto_portfolio_var",
            # Crypto Visualization
            "plot_crypto_prices",
            "plot_crypto_returns",
            "plot_crypto_correlation_heatmap",
            "plot_crypto_volatility_comparison",
        ]
    )
