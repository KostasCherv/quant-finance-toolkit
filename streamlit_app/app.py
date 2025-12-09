"""Main Streamlit application entry point.

Quantitative Finance Toolkit - Interactive Web Application
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Quant Finance Toolkit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #262730;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .feature-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .feature-box h3 {
        color: #1f77b4;
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    .feature-box p {
        color: #262730;
        line-height: 1.6;
        margin-bottom: 0;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main header
st.markdown(
    '<h1 class="main-header">📊 Quantitative Finance Toolkit</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">Interactive web application for portfolio optimization, cryptocurrency analysis, and risk management</p>',
    unsafe_allow_html=True,
)

# Sidebar info
st.sidebar.title("📊 Quant Finance Toolkit")
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This toolkit provides professional quantitative finance tools for portfolio optimization, "
    "cryptocurrency analysis, and risk management."
)

st.sidebar.markdown("### Navigation")
st.sidebar.markdown(
    """
    Use the pages menu above to navigate:
    - **Portfolio Optimizer** - Optimize stock portfolios
    - **Crypto Analysis** - Analyze cryptocurrencies
    - **Risk Calculator** - Calculate VaR
    """
)

# Home page content
st.markdown("## Welcome to the Quantitative Finance Toolkit")

st.markdown(
    """
    This interactive web application provides access to powerful quantitative finance tools
    for portfolio optimization, cryptocurrency analysis, and risk management.
    """
)

# Features overview
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-box">
            <h3>📈 Portfolio Optimizer</h3>
            <p>Optimize your stock portfolio using Markowitz mean-variance optimization.
            Generate efficient frontiers and find optimal asset allocations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-box">
            <h3>₿ Cryptocurrency Analysis</h3>
            <p>Analyze cryptocurrency prices, volatility, correlations, and optimize crypto portfolios.
            Compare performance across multiple digital assets.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-box">
            <h3>⚠️ Risk Calculator</h3>
            <p>Calculate Value at Risk (VaR) for individual assets, portfolios, and cryptocurrencies.
            Use analytical or Monte Carlo methods.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Quick start
st.markdown("## 🚀 Quick Start")

st.markdown(
    """
    1. **Portfolio Optimizer**: Select stocks, choose a date range, and optimize your portfolio
    2. **Cryptocurrency Analysis**: Analyze top cryptocurrencies with interactive visualizations
    3. **Risk Calculator**: Calculate VaR for your positions with customizable parameters
    """
)

st.markdown("---")

# Key features
st.markdown("## ✨ Key Features")

features = [
    "✅ Interactive Plotly visualizations with hover tooltips and zoom",
    "✅ Real-time data fetching from Yahoo Finance",
    "✅ Efficient frontier analysis with optimal portfolio identification",
    "✅ Cryptocurrency volatility and correlation analysis",
    "✅ Value at Risk (VaR) calculations (analytical and Monte Carlo)",
    "✅ Professional, responsive design",
    "✅ Data caching for improved performance",
]

for feature in features:
    st.markdown(feature)

st.markdown("---")

# Getting started
st.markdown("## 📖 Getting Started")

st.markdown(
    """
    Use the navigation sidebar to access different tools. Each page provides:
    - **Input controls** in the sidebar for parameters
    - **Interactive visualizations** in the main area
    - **Download options** for results and data
    """
)

st.info(
    "💡 **Tip**: Use the pages menu in the sidebar above to navigate to different tools. "
    "Start with the Portfolio Optimizer to see how the toolkit works. "
    "Select 3-5 stocks and a date range to generate an efficient frontier."
)
