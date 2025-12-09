"""Risk Calculator Page.

Calculate Value at Risk (VaR) for individual assets, portfolios, and cryptocurrencies
using analytical and Monte Carlo methods.
"""

import numpy as np
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from quant_finance_toolkit.crypto import crypto_portfolio_var, crypto_var_analysis
from quant_finance_toolkit.portfolio.markowitz import calculate_returns
from quant_finance_toolkit.risk import ValueAtRiskMonteCarlo, value_at_risk_n

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.streamlit_helpers import (
    format_currency,
    format_percentage,
    load_crypto_data,
    load_stock_data,
    validate_date_range,
)

st.set_page_config(page_title="Risk Calculator", page_icon="⚠️", layout="wide")

st.title("⚠️ Risk Calculator")
st.markdown(
    "Calculate Value at Risk (VaR) for your positions. VaR estimates the maximum expected loss "
    "over a specified time period at a given confidence level."
)

# Sidebar inputs
st.sidebar.header("Risk Calculation Configuration")

# Calculator type
calc_type = st.sidebar.selectbox(
    "Calculator Type",
    [
        "Single Asset VaR (Stock)",
        "Single Asset VaR (Crypto)",
        "Portfolio VaR (Stocks)",
        "Portfolio VaR (Crypto)",
    ],
    help="Choose the type of VaR calculation",
)

# Common inputs
position_value = st.sidebar.number_input(
    "Position Value ($)",
    min_value=1000.0,
    max_value=100000000.0,
    value=100000.0,
    step=10000.0,
    format="%.0f",
    help="Total value of the position",
)

confidence_level = st.sidebar.selectbox(
    "Confidence Level",
    [0.90, 0.95, 0.99],
    index=1,
    format_func=lambda x: f"{int(x*100)}%",
    help="Confidence level for VaR calculation (e.g., 95% means 5% chance of exceeding loss)",
)

time_horizon = st.sidebar.number_input(
    "Time Horizon (days)",
    min_value=1,
    max_value=252,
    value=1,
    step=1,
    help="Number of days for VaR calculation",
)

# Date range for historical data
st.sidebar.markdown("### Historical Data Range")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date", value=pd.Timestamp("2020-01-01").date(), key="risk_start"
    )
with col2:
    end_date = st.date_input(
        "End Date", value=pd.Timestamp("2024-01-01").date(), key="risk_end"
    )

# Validate dates
is_valid_dates = validate_date_range(start_date, end_date)
if not is_valid_dates:
    st.error("Start date must be before end date.")
    st.stop()

# Asset selection based on calculator type
if "Stock" in calc_type:
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
    ]
    if "Single" in calc_type:
        selected_assets = [
            st.sidebar.selectbox(
                "Select Stock", options=common_stocks, key="single_stock"
            )
        ]
    else:
        selected_assets = st.sidebar.multiselect(
            "Select Stocks",
            options=common_stocks,
            default=["AAPL", "MSFT", "GOOGL"],
            key="portfolio_stocks",
        )
        if len(selected_assets) < 2:
            st.warning("⚠️ Please select at least 2 stocks for portfolio VaR.")
            st.stop()
elif "Crypto" in calc_type:
    top_cryptos = [
        "BTC-USD",
        "ETH-USD",
        "BNB-USD",
        "SOL-USD",
        "ADA-USD",
        "XRP-USD",
        "DOGE-USD",
    ]
    if "Single" in calc_type:
        selected_assets = [
            st.sidebar.selectbox(
                "Select Cryptocurrency", options=top_cryptos, key="single_crypto"
            )
        ]
    else:
        selected_assets = st.sidebar.multiselect(
            "Select Cryptocurrencies",
            options=top_cryptos,
            default=["BTC-USD", "ETH-USD", "BNB-USD"],
            key="portfolio_cryptos",
        )
        if len(selected_assets) < 2:
            st.warning("⚠️ Please select at least 2 cryptocurrencies for portfolio VaR.")
            st.stop()

# Load data and calculate VaR
if len(selected_assets) == 0:
    st.warning("Please select at least one asset.")
    st.stop()

with st.spinner("Loading data and calculating VaR..."):
    try:
        if "Stock" in calc_type:
            data = load_stock_data(selected_assets, start_date, end_date)
            is_crypto = False
        else:
            data = load_crypto_data(selected_assets, start_date, end_date)
            is_crypto = True

        returns = calculate_returns(data)

        # Calculate statistics
        if len(selected_assets) == 1:
            # Single asset VaR
            asset = selected_assets[0]
            daily_returns = returns[asset].dropna()
            mu = daily_returns.mean()
            sigma = daily_returns.std()

            # Analytical VaR
            var_analytical = value_at_risk_n(
                position_value, confidence_level, mu, sigma, time_horizon
            )

            # Monte Carlo VaR
            mc_model = ValueAtRiskMonteCarlo(
                S=position_value,
                mu=mu,
                sigma=sigma,
                c=confidence_level,
                n=time_horizon,
                iterations=100000,
            )
            var_mc = mc_model.simulation()

            # Display results
            st.markdown("---")
            st.subheader(f"VaR Results for {asset}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Analytical VaR")
                st.metric("Value at Risk", format_currency(abs(var_analytical)))
                st.caption(f"Expected daily return: {format_percentage(mu)}")
                st.caption(f"Daily volatility: {format_percentage(sigma)}")

            with col2:
                st.markdown("#### Monte Carlo VaR")
                st.metric("Value at Risk", format_currency(var_mc))
                st.caption("Based on 100,000 simulations")
                st.caption(f"Using Geometric Brownian Motion")

            # Comparison
            st.markdown("---")
            st.subheader("VaR Comparison")

            comparison_df = pd.DataFrame(
                {
                    "Method": ["Analytical", "Monte Carlo"],
                    "VaR": [abs(var_analytical), var_mc],
                    "VaR (%)": [
                        format_percentage(abs(var_analytical) / position_value),
                        format_percentage(var_mc / position_value),
                    ],
                }
            )

            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

            # Interpretation
            st.info(
                f"""
                **Interpretation**: There is a {(1-confidence_level)*100:.0f}% chance that your position of {format_currency(position_value)}
                will lose more than {format_currency(max(abs(var_analytical), var_mc))} over the next {time_horizon} day(s).
                """
            )

        else:
            # Portfolio VaR
            if is_crypto:
                # Use crypto-specific portfolio VaR (equal weights)
                num_assets = len(selected_assets)
                equal_weights = [1.0 / num_assets] * num_assets
                portfolio_result = crypto_portfolio_var(
                    selected_assets,
                    equal_weights,
                    position_value,
                    start_date,
                    end_date,
                    confidence_level,
                    time_horizon,
                )

                st.markdown("---")
                st.subheader("Portfolio VaR Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Portfolio VaR",
                        format_currency(portfolio_result["portfolio_var"]),
                    )
                    st.caption(f"Confidence: {confidence_level*100:.0f}%")

                with col2:
                    st.metric("Time Horizon", f"{time_horizon} day(s)")
                    st.caption("Portfolio value")

                with col3:
                    st.metric(
                        "VaR as % of Portfolio",
                        format_percentage(
                            portfolio_result["portfolio_var"] / position_value
                        ),
                    )
                    st.caption("Relative risk")

                # Individual asset VaR
                st.markdown("---")
                st.subheader("Individual Asset VaR")

                individual_var = []
                for asset in selected_assets:
                    var_result = crypto_var_analysis(
                        asset,
                        position_value / len(selected_assets),
                        start_date,
                        end_date,
                        confidence_level,
                    )
                    individual_var.append(
                        {
                            "Asset": asset,
                            "Position": format_currency(
                                position_value / len(selected_assets)
                            ),
                            "VaR": format_currency(var_result["analytical_var"]),
                            "VaR %": format_percentage(
                                var_result["analytical_var"]
                                / (position_value / len(selected_assets))
                            ),
                        }
                    )

                individual_df = pd.DataFrame(individual_var)
                st.dataframe(individual_df, use_container_width=True, hide_index=True)

                # Diversification benefit
                st.markdown("---")
                st.subheader("Diversification Analysis")

                sum_individual_var = sum(
                    [
                        var_result["analytical_var"]
                        for var_result in [
                            crypto_var_analysis(
                                asset,
                                position_value / len(selected_assets),
                                start_date,
                                end_date,
                                confidence_level,
                            )
                            for asset in selected_assets
                        ]
                    ]
                )

                diversification_benefit = (
                    sum_individual_var - portfolio_result["portfolio_var"]
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Sum of Individual VaR", format_currency(sum_individual_var)
                    )

                with col2:
                    st.metric(
                        "Portfolio VaR",
                        format_currency(portfolio_result["portfolio_var"]),
                    )

                st.success(
                    f"✅ Diversification Benefit: {format_currency(diversification_benefit)} "
                    f"({format_percentage(diversification_benefit / sum_individual_var)})"
                )

            else:
                # Stock portfolio VaR
                # Calculate portfolio returns (equal weights for simplicity)
                portfolio_returns = returns.mean(axis=1)
                mu_portfolio = portfolio_returns.mean()
                sigma_portfolio = portfolio_returns.std()

                # Portfolio VaR
                var_portfolio = value_at_risk_n(
                    position_value,
                    confidence_level,
                    mu_portfolio,
                    sigma_portfolio,
                    time_horizon,
                )

                st.markdown("---")
                st.subheader("Portfolio VaR Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Portfolio VaR", format_currency(abs(var_portfolio)))
                    st.caption(f"Expected return: {format_percentage(mu_portfolio)}")

                with col2:
                    st.metric(
                        "Portfolio Volatility", format_percentage(sigma_portfolio)
                    )
                    st.caption("Daily standard deviation")

                with col3:
                    st.metric(
                        "VaR as % of Portfolio",
                        format_percentage(abs(var_portfolio) / position_value),
                    )
                    st.caption("Relative risk")

                # Individual asset VaR
                st.markdown("---")
                st.subheader("Individual Asset VaR")

                individual_var = []
                for asset in selected_assets:
                    asset_returns = returns[asset].dropna()
                    mu_asset = asset_returns.mean()
                    sigma_asset = asset_returns.std()
                    var_asset = value_at_risk_n(
                        position_value / len(selected_assets),
                        confidence_level,
                        mu_asset,
                        sigma_asset,
                        time_horizon,
                    )

                    individual_var.append(
                        {
                            "Asset": asset,
                            "Position": format_currency(
                                position_value / len(selected_assets)
                            ),
                            "VaR": format_currency(abs(var_asset)),
                            "VaR %": format_percentage(
                                abs(var_asset) / (position_value / len(selected_assets))
                            ),
                        }
                    )

                individual_df = pd.DataFrame(individual_var)
                st.dataframe(individual_df, use_container_width=True, hide_index=True)

                # Diversification benefit
                st.markdown("---")
                st.subheader("Diversification Analysis")

                sum_individual_var = sum(
                    [
                        abs(var_asset)
                        for var_asset in [
                            value_at_risk_n(
                                position_value / len(selected_assets),
                                confidence_level,
                                returns[asset].dropna().mean(),
                                returns[asset].dropna().std(),
                                time_horizon,
                            )
                            for asset in selected_assets
                        ]
                    ]
                )

                diversification_benefit = sum_individual_var - abs(var_portfolio)

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Sum of Individual VaR", format_currency(sum_individual_var)
                    )

                with col2:
                    st.metric("Portfolio VaR", format_currency(abs(var_portfolio)))

                st.success(
                    f"✅ Diversification Benefit: {format_currency(diversification_benefit)} "
                    f"({format_percentage(diversification_benefit / sum_individual_var)})"
                )

        st.success("✅ VaR calculation completed successfully!")

    except Exception as e:
        st.error(f"Error calculating VaR: {str(e)}")
        st.exception(e)

# Information section
with st.expander("ℹ️ About Value at Risk (VaR)"):
    st.markdown(
        """
        **Value at Risk (VaR)** is a statistical measure that quantifies the risk of loss for investments.

        **Key Concepts:**
        - **VaR** estimates the maximum expected loss over a specified time period at a given confidence level
        - **Confidence Level**: 95% VaR means there's a 5% chance of exceeding the loss
        - **Time Horizon**: The period over which the risk is measured (e.g., 1 day, 10 days)

        **Methods:**
        - **Analytical VaR**: Uses statistical formulas assuming normal distribution
        - **Monte Carlo VaR**: Simulates thousands of possible scenarios using Geometric Brownian Motion

        **Limitations:**
        - Assumes normal distribution (may not hold during market stress)
        - Does not predict extreme tail events beyond the confidence level
        - Past performance may not predict future results

        **Use Cases:**
        - Risk management and position sizing
        - Regulatory compliance
        - Portfolio risk assessment
        - Stress testing
        """
    )
