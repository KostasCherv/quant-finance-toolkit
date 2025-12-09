import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

NUM_OF_SIMULATIONS = 1000


def stock_monte_carlo(S0, mu, sigma, N=1000):
    results = []

    for _ in range(NUM_OF_SIMULATIONS):
        prices = [S0]
        for _ in range(N):
            prices.append(
                prices[-1]
                * np.exp((mu - 0.5 * sigma**2) + sigma * np.random.standard_normal())
            )
        results.append(prices)
    simulation_data = pd.DataFrame(results)
    simulation_data = simulation_data.T

    simulation_data["mean"] = simulation_data.mean(axis=1)
    plot_stock_price(simulation_data)


def plot_stock_price(simulation_data):
    plt.plot(simulation_data["mean"])
    plt.xlabel("Simulation")
    plt.ylabel("Stock Price")
    plt.title("Stock Price Monte Carlo Simulation")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    S = 50
    mu = 0.0002
    sigma = 0.01
    N = 1000
    stock_monte_carlo(S, mu, sigma, N)
