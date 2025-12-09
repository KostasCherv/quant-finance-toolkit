from scipy import stats
from numpy import log, sqrt, exp


def call_option_price(S, E, T, rf, sigma):
    d1 = (log(S / E) + (rf + sigma * sigma / 2.0) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * stats.norm.cdf(d1) - E * exp(-rf * T) * stats.norm.cdf(d2)


def put_option_price(S, E, T, rf, sigma):
    d1 = (log(S / E) + (rf + sigma * sigma / 2.0) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return -S * stats.norm.cdf(-d1) + E * exp(-rf * T) * stats.norm.cdf(-d2)


if __name__ == "__main__":
    S = 100
    E = 100
    T = 1
    rf = 0.05
    sigma = 0.2
    print(call_option_price(S, E, T, rf, sigma))
    print(put_option_price(S, E, T, rf, sigma))
