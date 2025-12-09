import numpy as np
import matplotlib.pyplot as plt
import numpy.random as npr


def wiener_process(dt=0.1, x0=0, n=1000):
    w = np.zeros(n + 1)
    t = np.linspace(x0, n, n + 1)

    w[1 : n + 1] = np.cumsum(npr.normal(1, np.sqrt(dt), n))

    return t, w


def plot_wiener_process(t, w):
    plt.plot(t, w)
    plt.xlabel("Time")
    plt.ylabel("Wiener Process")
    plt.title("Wiener Process")
    plt.show()


if __name__ == "__main__":
    t, w = wiener_process()
    plot_wiener_process(t, w)
