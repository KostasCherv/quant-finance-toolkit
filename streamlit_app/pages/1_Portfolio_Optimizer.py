"""Portfolio Optimizer Page.

Interactive portfolio optimization using Markowitz mean-variance optimization.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from quant_finance_toolkit.portfolio.markowitz import (
    calculate_returns,
    generate_portfolios,
    optimize_portfolio,
    statistics,
)
from quant_finance_toolkit.utils.interactive import plot_interactive_efficient_frontier

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.streamlit_helpers import (
    format_percentage,
    load_stock_data,
    validate_date_range,
    validate_tickers,
)

st.set_page_config(page_title="Portfolio Optimizer", page_icon="📈", layout="wide")

st.title("📈 Portfolio Optimizer")
st.markdown(
    "Optimize your stock portfolio using Markowitz mean-variance optimization. "
    "Generate efficient frontiers and find optimal asset allocations."
)

# Sidebar inputs
st.sidebar.header("Portfolio Configuration")

# Common stock tickers
common_stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "TSLA",
    "META",
    "NVDA",
    "JPM",
    "V",
    "JNJ",
    "WMT",
    "PG",
    "MA",
    "UNH",
    "HD",
    "DIS",
    "BAC",
    "ADBE",
    "NFLX",
    "CRM",
]

selected_tickers = st.sidebar.multiselect(
    "Select Stocks",
    options=common_stocks,
    default=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
    help="Select at least 2 stocks for portfolio optimization",
)

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=pd.Timestamp("2020-01-01").date())
with col2:
    end_date = st.date_input("End Date", value=pd.Timestamp("2024-01-01").date())

# Number of portfolios
num_portfolios = st.sidebar.slider(
    "Number of Portfolios",
    min_value=1000,
    max_value=50000,
    value=10000,
    step=1000,
    help="More portfolios = smoother efficient frontier but slower computation",
)

# Risk-free rate
risk_free_rate = (
    st.sidebar.number_input(
        "Risk-Free Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.1,
        help="Annual risk-free rate (e.g., 5.0 for 5%)",
    )
    / 100
)

# Validate inputs
is_valid_tickers, ticker_error = validate_tickers(selected_tickers)
is_valid_dates = validate_date_range(start_date, end_date)

if not is_valid_tickers:
    st.error(ticker_error)
    st.stop()

if not is_valid_dates:
    st.error("Start date must be before end date.")
    st.stop()

# Load data
with st.spinner("Loading stock data..."):
    try:
        stock_data = load_stock_data(selected_tickers, start_date, end_date)
        st.success(f"✅ Loaded data for {len(selected_tickers)} stocks")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Calculate returns
returns = calculate_returns(stock_data)

# Generate portfolios
with st.spinner("Generating portfolios..."):
    p_weights, p_means, p_risks = generate_portfolios(
        returns, num_portfolios=num_portfolios
    )

# Optimize portfolio
with st.spinner("Optimizing portfolio..."):
    opt = optimize_portfolio(returns)
    optimal_stats = statistics(opt["x"], returns)

# Display results
st.markdown("---")

# Main visualization
st.subheader("Efficient Frontier")
st.markdown(
    "The efficient frontier shows all possible portfolios. "
    "The red star indicates the optimal portfolio (maximum Sharpe ratio)."
)

# Create interactive plot
fig = plot_interactive_efficient_frontier(
    portfolio_returns=p_means,
    portfolio_volatility=p_risks,
    optimal_stats=(optimal_stats[0], optimal_stats[1]),
    optimal_weights=opt["x"],
    asset_names=selected_tickers,
    title="Interactive Efficient Frontier",
    show_plot=False,
)

st.plotly_chart(fig, use_container_width=True)

# Portfolio statistics
st.markdown("---")
st.subheader("Optimal Portfolio Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Expected Return", format_percentage(optimal_stats[0]))

with col2:
    st.metric("Expected Volatility", format_percentage(optimal_stats[1]))

with col3:
    sharpe_ratio = (
        optimal_stats[2]
        if len(optimal_stats) > 2
        else optimal_stats[0] / optimal_stats[1]
    )
    st.metric("Sharpe Ratio", f"{sharpe_ratio:.3f}")

with col4:
    st.metric("Number of Assets", len(selected_tickers))

# Optimal weights
st.markdown("---")
st.subheader("Optimal Portfolio Weights")

weights_df = pd.DataFrame(
    {
        "Stock": selected_tickers,
        "Weight": opt["x"],
        "Weight (%)": [format_percentage(w) for w in opt["x"]],
    }
).sort_values("Weight", ascending=False)

st.dataframe(weights_df, use_container_width=True, hide_index=True)

# Download option
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    # Convert to CSV for download
    csv = weights_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Portfolio Weights (CSV)",
        data=csv,
        file_name="optimal_portfolio_weights.csv",
        mime="text/csv",
    )

with col2:
    # Portfolio statistics as JSON
    import json

    stats_dict = {
        "expected_return": float(optimal_stats[0]),
        "expected_volatility": float(optimal_stats[1]),
        "sharpe_ratio": float(sharpe_ratio),
        "weights": {
            ticker: float(weight) for ticker, weight in zip(selected_tickers, opt["x"])
        },
    }
    json_str = json.dumps(stats_dict, indent=2)
    st.download_button(
        label="📥 Download Portfolio Stats (JSON)",
        data=json_str,
        file_name="portfolio_statistics.json",
        mime="application/json",
    )

# Additional information
with st.expander("ℹ️ About Portfolio Optimization"):
    st.markdown(
        """
        **Markowitz Mean-Variance Optimization** is a mathematical framework for constructing
        portfolios that maximize expected return for a given level of risk, or minimize risk
        for a given level of expected return.

        **Key Concepts:**
        - **Efficient Frontier**: The set of optimal portfolios that offer the highest expected
          return for a given level of risk
        - **Optimal Portfolio**: The portfolio on the efficient frontier with the highest
          Sharpe ratio (risk-adjusted return)
        - **Sharpe Ratio**: Measures risk-adjusted return, calculated as (Return - Risk-Free Rate) / Volatility

        **How to Use:**
        1. Select multiple stocks (at least 2)
        2. Choose a date range for historical data
        3. Adjust the number of portfolios for smoother curves
        4. Set the risk-free rate (typically current treasury bond yield)
        5. Review the optimal portfolio weights and statistics
        """
    )
