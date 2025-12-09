"""Cryptocurrency Analysis Page.

Interactive cryptocurrency analysis including price comparison, volatility analysis,
correlation analysis, and portfolio optimization.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from quant_finance_toolkit.crypto import (
    crypto_correlation_matrix,
    crypto_volatility_analysis,
    optimize_crypto_portfolio,
)
from quant_finance_toolkit.portfolio.markowitz import (
    calculate_returns,
    generate_portfolios,
    statistics,
)
from quant_finance_toolkit.utils.interactive import (
    plot_interactive_correlation_heatmap,
    plot_interactive_crypto_prices,
    plot_interactive_efficient_frontier,
    plot_interactive_volatility_comparison,
)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.streamlit_helpers import (
    format_percentage,
    load_crypto_data,
    validate_date_range,
    validate_tickers,
)

st.set_page_config(page_title="Cryptocurrency Analysis", page_icon="₿", layout="wide")

st.title("₿ Cryptocurrency Analysis")
st.markdown(
    "Analyze cryptocurrency prices, volatility, correlations, and optimize crypto portfolios. "
    "Compare performance across multiple digital assets."
)

# Sidebar inputs
st.sidebar.header("Analysis Configuration")

# Crypto tickers
top_cryptos = [
    "BTC-USD",
    "ETH-USD",
    "BNB-USD",
    "SOL-USD",
    "ADA-USD",
    "XRP-USD",
    "DOGE-USD",
    "DOT-USD",
]

selected_cryptos = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    options=top_cryptos,
    default=["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD"],
    help="Select cryptocurrencies to analyze",
)

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date", value=pd.Timestamp("2020-01-01").date(), key="crypto_start"
    )
with col2:
    end_date = st.date_input(
        "End Date", value=pd.Timestamp("2024-01-01").date(), key="crypto_end"
    )

# Number of portfolios for optimization
num_portfolios = st.sidebar.slider(
    "Number of Portfolios (for optimization)",
    min_value=1000,
    max_value=50000,
    value=10000,
    step=1000,
    help="Used for portfolio optimization tab",
)

# Validate inputs
is_valid_tickers, ticker_error = validate_tickers(selected_cryptos)
is_valid_dates = validate_date_range(start_date, end_date)

if not is_valid_tickers:
    st.error(ticker_error)
    st.stop()

if not is_valid_dates:
    st.error("Start date must be before end date.")
    st.stop()

# Load data
with st.spinner("Loading cryptocurrency data..."):
    try:
        crypto_data = load_crypto_data(selected_cryptos, start_date, end_date)
        st.success(f"✅ Loaded data for {len(selected_cryptos)} cryptocurrencies")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Price Comparison",
        "📊 Volatility Analysis",
        "🔗 Correlation",
        "💼 Portfolio Optimization",
    ]
)

# Tab 1: Price Comparison
with tab1:
    st.subheader("Cryptocurrency Price Comparison")
    st.markdown(
        "Compare normalized price performance across selected cryptocurrencies."
    )

    normalize = st.checkbox(
        "Normalize Prices (Base = 100)",
        value=True,
        help="Normalize prices to start at 100 for easier comparison",
    )

    fig_prices = plot_interactive_crypto_prices(
        crypto_tickers=selected_cryptos,
        start_date=start_date,
        end_date=end_date,
        normalize=normalize,
        title="Interactive Cryptocurrency Price Comparison",
        show_plot=False,
    )

    st.plotly_chart(fig_prices, use_container_width=True)

    with st.expander("ℹ️ About Price Comparison"):
        st.markdown(
            """
            **Normalized Prices**: When normalized, all prices start at 100, making it easier to
            compare percentage performance across different cryptocurrencies regardless of their
            absolute price levels.

            **Use the interactive features:**
            - Hover over lines to see exact dates and prices
            - Use date range selector buttons (1M, 6M, YTD, 1Y, All)
            - Drag the range slider to zoom into specific time periods
            """
        )

# Tab 2: Volatility Analysis
with tab2:
    st.subheader("Volatility Analysis")
    st.markdown("Compare volatility metrics across cryptocurrencies.")

    with st.spinner("Calculating volatility metrics..."):
        volatility_df = crypto_volatility_analysis(
            selected_cryptos, start_date, end_date
        )

    # Display volatility table
    st.markdown("#### Volatility Metrics")
    st.dataframe(volatility_df, use_container_width=True)

    # Interactive volatility comparison
    metric_options = volatility_df.columns.tolist()
    selected_metric = st.selectbox(
        "Select Metric to Visualize", options=metric_options, index=0
    )

    fig_vol = plot_interactive_volatility_comparison(
        volatility_data=volatility_df,
        metric=selected_metric,
        title=f"Interactive {selected_metric.replace('_', ' ').title()} Comparison",
        show_plot=False,
    )

    st.plotly_chart(fig_vol, use_container_width=True)

    with st.expander("ℹ️ About Volatility Metrics"):
        st.markdown(
            """
            **Volatility** measures the degree of variation in price over time.

            **Metrics Explained:**
            - **Annualized Volatility**: Standard deviation of returns, annualized (365 days for crypto)
            - **Daily Volatility**: Standard deviation of daily returns
            - **Max Drawdown**: Maximum peak-to-trough decline
            - **Average Daily Return**: Mean of daily returns

            Higher volatility indicates greater price fluctuations and risk.
            """
        )

# Tab 3: Correlation
with tab3:
    st.subheader("Correlation Analysis")
    st.markdown("Analyze correlation between cryptocurrency returns.")

    with st.spinner("Calculating correlation matrix..."):
        corr_matrix = crypto_correlation_matrix(selected_cryptos, start_date, end_date)

    # Display correlation table
    st.markdown("#### Correlation Matrix")
    st.dataframe(corr_matrix, use_container_width=True)

    # Interactive heatmap
    fig_heatmap = plot_interactive_correlation_heatmap(
        correlation_matrix=corr_matrix,
        title="Interactive Cryptocurrency Correlation Heatmap",
        show_plot=False,
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Correlation insights
    st.markdown("#### Correlation Insights")
    avg_correlation = corr_matrix.values[corr_matrix.values != 1.0].mean()
    st.info(f"Average correlation between cryptocurrencies: **{avg_correlation:.3f}**")

    if avg_correlation > 0.7:
        st.warning(
            "⚠️ High correlation detected. Cryptocurrencies tend to move together, "
            "which may limit diversification benefits."
        )
    elif avg_correlation < 0.3:
        st.success(
            "✅ Low correlation detected. Good diversification potential across selected cryptocurrencies."
        )

    with st.expander("ℹ️ About Correlation"):
        st.markdown(
            """
            **Correlation** measures how closely two assets move together.

            - **+1.0**: Perfect positive correlation (move in same direction)
            - **0.0**: No correlation (independent movements)
            - **-1.0**: Perfect negative correlation (move in opposite directions)

            **For Portfolio Diversification:**
            - Lower correlation = better diversification
            - High correlation = limited diversification benefits
            - Cryptocurrencies typically show high correlation during market stress
            """
        )

# Tab 4: Portfolio Optimization
with tab4:
    st.subheader("Cryptocurrency Portfolio Optimization")
    st.markdown("Optimize a cryptocurrency portfolio using Markowitz optimization.")

    if len(selected_cryptos) < 2:
        st.warning(
            "⚠️ Please select at least 2 cryptocurrencies for portfolio optimization."
        )
    else:
        with st.spinner("Optimizing cryptocurrency portfolio..."):
            # Calculate returns
            crypto_returns = calculate_returns(crypto_data)

            # Generate portfolios
            p_weights, p_means, p_risks = generate_portfolios(
                crypto_returns, num_portfolios=num_portfolios
            )

            # Optimize portfolio
            opt_result = optimize_crypto_portfolio(
                selected_cryptos, start_date, end_date, num_portfolios=num_portfolios
            )

            # Extract optimal weights as array (matching ticker order)
            optimal_weights_array = np.array(
                [opt_result["optimized_weights"][ticker] for ticker in selected_cryptos]
            )

            # Get optimal stats
            optimal_stats = statistics(optimal_weights_array, crypto_returns)

        # Display efficient frontier
        fig_portfolio = plot_interactive_efficient_frontier(
            portfolio_returns=p_means,
            portfolio_volatility=p_risks,
            optimal_stats=(optimal_stats[0], optimal_stats[1]),
            optimal_weights=optimal_weights_array,
            asset_names=selected_cryptos,
            title="Interactive Crypto Portfolio Efficient Frontier",
            show_plot=False,
        )

        st.plotly_chart(fig_portfolio, use_container_width=True)

        # Portfolio statistics
        st.markdown("---")
        st.subheader("Optimal Portfolio Statistics")

        col1, col2, col3 = st.columns(3)

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

        # Optimal weights
        st.markdown("---")
        st.subheader("Optimal Portfolio Weights")

        weights_df = pd.DataFrame(
            {
                "Cryptocurrency": selected_cryptos,
                "Weight": optimal_weights_array,
                "Weight (%)": [format_percentage(w) for w in optimal_weights_array],
            }
        ).sort_values("Weight", ascending=False)

        st.dataframe(weights_df, use_container_width=True, hide_index=True)

        # Download option
        csv = weights_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Crypto Portfolio Weights (CSV)",
            data=csv,
            file_name="crypto_portfolio_weights.csv",
            mime="text/csv",
        )

        with st.expander("ℹ️ About Crypto Portfolio Optimization"):
            st.markdown(
                """
                **Cryptocurrency Portfolio Optimization** uses the same Markowitz framework as
                traditional portfolio optimization, but accounts for the 24/7 trading nature of
                cryptocurrencies (365 trading days vs 252 for stocks).

                **Considerations:**
                - Cryptocurrencies are highly volatile
                - High correlation during market stress
                - 24/7 trading means no market close gaps
                - Higher risk, potentially higher returns

                **Note**: Past performance does not guarantee future results. Always do your own research.
                """
            )
