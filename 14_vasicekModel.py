import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr


def vasicek_model(r0, kappa, theta, sigma, T=1.0, N=10000):
    dt = T / float(N)
    t = np.linspace(0, T, N + 1)
    rates = [r0]
    for _ in range(N):
        dr = kappa * (theta - rates[-1]) * dt + sigma * np.sqrt(dt) * npr.normal()
        rates.append(rates[-1] + dr)
    return t, rates


def plot_model(t, rates):
    plt.plot(t, rates)
    plt.xlabel("Time")
    plt.ylabel("Interest Rate")
    plt.title("Vasicek Model")
    plt.show()


if __name__ == "__main__":
    t, rates = vasicek_model(1.3, 0.9, 1.4, 0.05)
    plot_model(t, rates)
