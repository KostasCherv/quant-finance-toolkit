# Geometric Random Walk Model / Geometric Brownian Motion
import matplotlib.pyplot as plt
import numpy as np


def simulate_gbm(s0, T=2, N=1000, mu=0.1, sigma=0.05):
    dt = T / N
    t = np.linspace(0, T, N)

    # standard normal random variables N(0, 1)
    W = np.random.standard_normal(size=N)
    # N(0, dt) = sqrt(dt) * N(0, 1)
    W = np.cumsum(W) * np.sqrt(dt)

    X = (mu - 0.5 * sigma**2) * t + sigma * W
    S = s0 * np.exp(X)

    return t, S


def plot_gbm(t, s):
    plt.plot(t, s)
    plt.xlabel("Time")
    plt.ylabel("Stock Price")
    plt.title("GBM Simulation")
    plt.show()


if __name__ == "__main__":
    s0 = 10
    t, s = simulate_gbm(s0)
    plot_gbm(t, s)
