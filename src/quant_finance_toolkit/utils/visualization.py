"""Visualization utilities for financial models."""

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_wiener_process(
    t: np.ndarray, w: np.ndarray, title: str = "Wiener Process", show_plot: bool = True
) -> None:
    """Plot Wiener process (Brownian motion).

    Parameters
    ----------
    t : np.ndarray
        Time array
    w : np.ndarray
        Wiener process values
    title : str, optional
        Plot title, by default "Wiener Process"
    show_plot : bool, optional
        Whether to display the plot, by default True
    """
    plt.figure(figsize=(10, 6))
    plt.plot(t, w)
    plt.xlabel("Time")
    plt.ylabel("Wiener Process")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    if show_plot:
        plt.show()


def plot_gbm(
    t: np.ndarray,
    s: np.ndarray,
    title: str = "GBM Simulation",
    show_plot: bool = True,
) -> None:
    """Plot Geometric Brownian Motion simulation.

    Parameters
    ----------
    t : np.ndarray
        Time array
    s : np.ndarray
        Stock price array
    title : str, optional
        Plot title, by default "GBM Simulation"
    show_plot : bool, optional
        Whether to display the plot, by default True
    """
    plt.figure(figsize=(10, 6))
    plt.plot(t, s)
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    if show_plot:
        plt.show()


def plot_process(
    x: np.ndarray,
    title: str = "Ornstein-Uhlenbeck Process",
    xlabel: str = "Time",
    ylabel: str = "Process",
    show_plot: bool = True,
) -> None:
    """Plot a stochastic process.

    Parameters
    ----------
    x : np.ndarray
        Process values
    title : str, optional
        Plot title, by default "Ornstein-Uhlenbeck Process"
    xlabel : str, optional
        X-axis label, by default "Time"
    ylabel : str, optional
        Y-axis label, by default "Process"
    show_plot : bool, optional
        Whether to display the plot, by default True
    """
    plt.figure(figsize=(10, 6))
    plt.plot(x)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    if show_plot:
        plt.show()
