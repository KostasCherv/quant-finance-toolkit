from math import exp


def future_discrete_value(x, r, n):
    return x * (1 + r) ** n


def present_discrete_value(x, r, n):
    return x / (1 + r) ** n


def future_continuous_value(x, r, t):
    return x * exp(r * t)


def present_continuous_value(x, r, t):
    return x * exp(-r * t)


if __name__ == "__main__":
    x = 100
    r = 0.05
    n = 5
    print("future_discrete_value: ", future_discrete_value(x, r, n))
    print("present_discrete_value: ", present_discrete_value(x, r, n))
    print("future_continuous_value: ", future_continuous_value(x, r, n))
    print("present_continuous_value: ", present_continuous_value(x, r, n))
