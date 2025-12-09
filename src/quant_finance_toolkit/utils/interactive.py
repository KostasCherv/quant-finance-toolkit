"""Interactive visualization utilities using Plotly.

This module provides interactive versions of key visualizations using Plotly
for enhanced user experience with zoom, pan, hover tooltips, and export capabilities.
"""

from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Professional color palette
COLOR_PALETTE = [
    "#1f77b4",  # Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Olive
    "#17becf",  # Cyan
]


def plot_interactive_efficient_frontier(
    portfolio_returns: np.ndarray,
    portfolio_volatility: np.ndarray,
    optimal_stats: Optional[Tuple[float, float]] = None,
    optimal_weights: Optional[np.ndarray] = None,
    asset_names: Optional[List[str]] = None,
    title: str = "Interactive Efficient Frontier",
    show_plot: bool = True,
) -> go.Figure:
    """Create interactive efficient frontier plot with hover tooltips.

    Parameters
    ----------
    portfolio_returns : np.ndarray
        Array of portfolio expected returns
    portfolio_volatility : np.ndarray
        Array of portfolio volatilities
    optimal_stats : Optional[Tuple[float, float]], optional
        Tuple of (return, volatility) for optimal portfolio, by default None
    optimal_weights : Optional[np.ndarray], optional
        Optimal portfolio weights, by default None
    asset_names : Optional[List[str]], optional
        Names of assets for tooltip display, by default None
    title : str, optional
        Plot title, by default "Interactive Efficient Frontier"
    show_plot : bool, optional
        Whether to display the plot, by default True

    Returns
    -------
    go.Figure
        Plotly figure object

    Examples
    --------
    >>> import numpy as np
    >>> returns = np.random.randn(1000) * 0.1 + 0.15
    >>> volatility = np.random.randn(1000) * 0.05 + 0.20
    >>> fig = plot_interactive_efficient_frontier(returns, volatility, show_plot=False)
    """
    sharpe_ratios = portfolio_returns / portfolio_volatility

    # Create hover text
    hover_text = [
        f"Return: {ret:.2%}<br>" f"Volatility: {vol:.2%}<br>" f"Sharpe Ratio: {sr:.3f}"
        for ret, vol, sr in zip(portfolio_returns, portfolio_volatility, sharpe_ratios)
    ]

    fig = go.Figure()

    # Add efficient frontier scatter
    fig.add_trace(
        go.Scatter(
            x=portfolio_volatility,
            y=portfolio_returns,
            mode="markers",
            marker=dict(
                size=6,
                color=sharpe_ratios,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Sharpe Ratio"),
                line=dict(width=0.5, color="white"),
            ),
            text=hover_text,
            hovertemplate="<b>Portfolio</b><br>%{text}<extra></extra>",
            name="Efficient Frontier",
        )
    )

    # Add optimal portfolio if provided
    if optimal_stats is not None:
        opt_return, opt_vol = optimal_stats
        opt_sharpe = opt_return / opt_vol if opt_vol > 0 else 0

        # Create tooltip for optimal portfolio
        opt_text = f"<b>Optimal Portfolio</b><br>"
        opt_text += f"Return: {opt_return:.2%}<br>"
        opt_text += f"Volatility: {opt_vol:.2%}<br>"
        opt_text += f"Sharpe Ratio: {opt_sharpe:.3f}<br>"

        if optimal_weights is not None and asset_names is not None:
            opt_text += "<br><b>Weights:</b><br>"
            for name, weight in zip(asset_names, optimal_weights):
                opt_text += f"{name}: {weight:.1%}<br>"

        fig.add_trace(
            go.Scatter(
                x=[opt_vol],
                y=[opt_return],
                mode="markers",
                marker=dict(
                    size=20,
                    symbol="star",
                    color="red",
                    line=dict(width=2, color="darkred"),
                ),
                text=opt_text,
                hovertemplate="%{text}<extra></extra>",
                name="Optimal Portfolio",
            )
        )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20)),
        xaxis_title="Expected Risk (Volatility)",
        yaxis_title="Expected Return",
        hovermode="closest",
        template="plotly_white",
        width=900,
        height=600,
        showlegend=True,
    )

    if show_plot:
        fig.show()

    return fig


def plot_interactive_crypto_prices(
    crypto_tickers: List[str],
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
    normalize: bool = True,
    title: Optional[str] = None,
    show_plot: bool = True,
) -> go.Figure:
    """Create interactive cryptocurrency price comparison plot.

    Parameters
    ----------
    crypto_tickers : List[str]
        List of crypto tickers (e.g., ["BTC-USD", "ETH-USD"])
    start_date : Union[str, pd.Timestamp]
        Start date for data
    end_date : Union[str, pd.Timestamp]
        End date for data
    normalize : bool, optional
        If True, normalize prices to start at 100, by default True
    title : Optional[str], optional
        Custom plot title, by default None
    show_plot : bool, optional
        Whether to display the plot, by default True

    Returns
    -------
    go.Figure
        Plotly figure object

    Examples
    --------
    >>> fig = plot_interactive_crypto_prices(
    ...     ["BTC-USD", "ETH-USD"], "2020-01-01", "2023-01-01", show_plot=False
    ... )
    """
    from ..data.fetchers import download_crypto_data

    # Download data
    crypto_data = download_crypto_data(crypto_tickers, start_date, end_date)

    fig = go.Figure()

    for i, ticker in enumerate(crypto_tickers):
        prices = crypto_data[ticker].dropna()
        if len(prices) == 0:
            continue

        if normalize:
            normalized = (prices / prices.iloc[0]) * 100
            y_values = normalized.values
            y_label = "Normalized Price (Base = 100)"
            plot_title = title or "Cryptocurrency Price Comparison (Normalized)"
        else:
            y_values = prices.values
            y_label = "Price (USD)"
            plot_title = title or "Cryptocurrency Price History"

        # Create hover text with date and price
        hover_text = [
            (
                f"<b>{ticker}</b><br>" f"Date: {date}<br>" f"Price: ${price:,.2f}"
                if not normalize
                else f"Normalized: {price:.2f}"
            )
            for date, price in zip(prices.index, y_values)
        ]

        fig.add_trace(
            go.Scatter(
                x=prices.index,
                y=y_values,
                mode="lines",
                name=ticker,
                line=dict(width=2.5, color=COLOR_PALETTE[i % len(COLOR_PALETTE)]),
                hovertemplate="%{text}<extra></extra>",
                text=hover_text,
            )
        )

    fig.update_layout(
        title=dict(text=plot_title, x=0.5, font=dict(size=20)),
        xaxis_title="Date",
        yaxis_title=y_label,
        hovermode="x unified",
        template="plotly_white",
        width=1000,
        height=600,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
    )

    if show_plot:
        fig.show()

    return fig


def plot_interactive_correlation_heatmap(
    correlation_matrix: pd.DataFrame,
    title: str = "Interactive Correlation Heatmap",
    show_plot: bool = True,
) -> go.Figure:
    """Create interactive correlation heatmap with hover tooltips.

    Parameters
    ----------
    correlation_matrix : pd.DataFrame
        Correlation matrix
    title : str, optional
        Plot title, by default "Interactive Correlation Heatmap"
    show_plot : bool, optional
        Whether to display the plot, by default True

    Returns
    -------
    go.Figure
        Plotly figure object

    Examples
    --------
    >>> import pandas as pd
    >>> corr = pd.DataFrame([[1.0, 0.8], [0.8, 1.0]],
    ...                     index=["BTC-USD", "ETH-USD"],
    ...                     columns=["BTC-USD", "ETH-USD"])
    >>> fig = plot_interactive_correlation_heatmap(corr, show_plot=False)
    """
    tickers = correlation_matrix.index.tolist()
    corr_values = correlation_matrix.values

    # Create hover text matrix
    hover_text = [
        [
            f"<b>{tickers[i]} vs {tickers[j]}</b><br>Correlation: {corr_values[i, j]:.3f}"
            for j in range(len(tickers))
        ]
        for i in range(len(tickers))
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=corr_values,
            x=tickers,
            y=tickers,
            colorscale="RdBu",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=hover_text,
            texttemplate="%{z:.2f}",
            textfont={"size": 12, "color": "white"},
            hovertemplate="%{text}<extra></extra>",
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20)),
        width=700,
        height=700,
        template="plotly_white",
        xaxis=dict(side="bottom"),
    )

    if show_plot:
        fig.show()

    return fig


def plot_interactive_volatility_comparison(
    volatility_data: pd.DataFrame,
    metric: str = "annualized_volatility",
    title: Optional[str] = None,
    show_plot: bool = True,
) -> go.Figure:
    """Create interactive bar chart comparing volatility metrics.

    Parameters
    ----------
    volatility_data : pd.DataFrame
        DataFrame with volatility metrics
    metric : str, optional
        Which volatility metric to plot, by default "annualized_volatility"
    title : Optional[str], optional
        Custom plot title, by default None
    show_plot : bool, optional
        Whether to display the plot, by default True

    Returns
    -------
    go.Figure
        Plotly figure object

    Examples
    --------
    >>> import pandas as pd
    >>> vol_data = pd.DataFrame(
    ...     {"annualized_volatility": [0.8, 1.2]},
    ...     index=["BTC-USD", "ETH-USD"]
    ... )
    >>> fig = plot_interactive_volatility_comparison(vol_data, show_plot=False)
    """
    if metric not in volatility_data.columns:
        raise ValueError(f"Metric '{metric}' not found in volatility_data")

    tickers = volatility_data.index.tolist()
    values = volatility_data[metric].values

    # Create hover text
    hover_text = [
        f"<b>{ticker}</b><br>{metric.replace('_', ' ').title()}: {val:.3f}"
        for ticker, val in zip(tickers, values)
    ]

    # Color bars based on values (gradient)
    colors = [
        f"hsl({240 - int(val * 60)}, 70%, {50 + int(val * 20)}%)" for val in values
    ]

    fig = go.Figure(
        data=go.Bar(
            x=tickers,
            y=values,
            marker=dict(
                color=colors,
                line=dict(color="rgba(0,0,0,0.5)", width=1),
            ),
            text=[f"{v:.3f}" for v in values],
            textposition="outside",
            hovertemplate="%{text}<extra></extra>",
            textfont=dict(size=11),
        )
    )

    plot_title = title or f"Volatility Comparison ({metric.replace('_', ' ').title()})"

    fig.update_layout(
        title=dict(text=plot_title, x=0.5, font=dict(size=20)),
        xaxis_title="Asset",
        yaxis_title=metric.replace("_", " ").title(),
        template="plotly_white",
        width=900,
        height=600,
        hovermode="x unified",
    )

    if show_plot:
        fig.show()

    return fig


def plot_interactive_gbm_simulation(
    time: np.ndarray,
    price_paths: np.ndarray,
    title: str = "Interactive GBM Simulation",
    show_plot: bool = True,
) -> go.Figure:
    """Create interactive GBM simulation plot with multiple paths.

    Parameters
    ----------
    time : np.ndarray
        Time array
    price_paths : np.ndarray
        Array of price paths (shape: [num_paths, time_steps])
    title : str, optional
        Plot title, by default "Interactive GBM Simulation"
    show_plot : bool, optional
        Whether to display the plot, by default True

    Returns
    -------
    go.Figure
        Plotly figure object

    Examples
    --------
    >>> import numpy as np
    >>> time = np.linspace(0, 1, 252)
    >>> paths = np.random.randn(10, 252).cumsum(axis=1) + 100
    >>> fig = plot_interactive_gbm_simulation(time, paths, show_plot=False)
    """
    fig = go.Figure()

    num_paths = price_paths.shape[0]

    # Plot individual paths with transparency
    for i in range(min(num_paths, 50)):  # Limit to 50 paths for performance
        fig.add_trace(
            go.Scatter(
                x=time,
                y=price_paths[i, :],
                mode="lines",
                line=dict(width=1, color="rgba(31, 119, 180, 0.3)"),
                showlegend=False,
                hovertemplate="Time: %{x:.2f}<br>Price: %{y:.2f}<extra></extra>",
            )
        )

    # Plot mean path
    mean_path = np.mean(price_paths, axis=0)
    std_path = np.std(price_paths, axis=0)

    fig.add_trace(
        go.Scatter(
            x=time,
            y=mean_path,
            mode="lines",
            name="Mean Path",
            line=dict(width=3, color="red"),
            hovertemplate="Time: %{x:.2f}<br>Mean Price: %{y:.2f}<extra></extra>",
        )
    )

    # Add confidence bands
    fig.add_trace(
        go.Scatter(
            x=time,
            y=mean_path + 1.96 * std_path,
            mode="lines",
            name="95% Upper Bound",
            line=dict(width=1, color="rgba(255,0,0,0.3)", dash="dash"),
            showlegend=True,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time,
            y=mean_path - 1.96 * std_path,
            mode="lines",
            name="95% Lower Bound",
            line=dict(width=1, color="rgba(255,0,0,0.3)", dash="dash"),
            fill="tonexty",
            fillcolor="rgba(255,0,0,0.1)",
            showlegend=True,
        )
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=20)),
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_white",
        width=1000,
        height=600,
        hovermode="x unified",
    )

    if show_plot:
        fig.show()

    return fig
