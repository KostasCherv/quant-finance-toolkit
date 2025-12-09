import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


NUM_OF_SIMULATIONS = 1000
NUM_OF_POINTS = 200


def monte_carlo_simulation(x, r0, kappa, theta, sigma, T=1.0):
    dt = T / float(NUM_OF_POINTS)
    results = []

    for _ in range(NUM_OF_SIMULATIONS):
        rates = [r0]
        for _ in range(NUM_OF_POINTS):
            dr = (
                kappa * (theta - rates[-1]) * dt
                + sigma * np.sqrt(dt) * np.random.normal()
            )
            rates.append(rates[-1] + dr)
        results.append(rates)

    simulation_data = pd.DataFrame(results).T

    integral_sum = simulation_data.sum() * dt
    present_integral_value = np.exp(-integral_sum)

    # mean
    bond_price = x * np.mean(present_integral_value)

    print(f"Bond Price: {bond_price}")


if __name__ == "__main__":
    monte_carlo_simulation(1000, 0.5, 0.3, 0.9, 0.03)
