"""Example: Option pricing using Black-Scholes and Monte Carlo methods."""

from quant_finance_toolkit import OptionPriceMonteCarlo, call_option_price, put_option_price

# Parameters
S = 100  # Current stock price
E = 100  # Strike price
T = 1  # Time to expiration (years)
rf = 0.05  # Risk-free rate
sigma = 0.2  # Volatility

print("=" * 50)
print("Option Pricing Example")
print("=" * 50)
print(f"Stock Price: ${S}")
print(f"Strike Price: ${E}")
print(f"Time to Expiration: {T} year(s)")
print(f"Risk-free Rate: {rf*100}%")
print(f"Volatility: {sigma*100}%")
print()

# Black-Scholes pricing
print("Black-Scholes Pricing:")
call_bs = call_option_price(S, E, T, rf, sigma)
put_bs = put_option_price(S, E, T, rf, sigma)
print(f"Call Option Price: ${call_bs:.2f}")
print(f"Put Option Price: ${put_bs:.2f}")
print()

# Monte Carlo pricing
print("Monte Carlo Pricing (10,000 simulations):")
mc_model = OptionPriceMonteCarlo(S, E, T, rf, sigma, iterations=10000)
call_mc = mc_model.call_option_price()
put_mc = mc_model.put_option_price()
print(f"Call Option Price: ${call_mc:.2f}")
print(f"Put Option Price: ${put_mc:.2f}")
print()

# Compare results
print("Comparison:")
print(f"Call Price Difference: ${abs(call_bs - call_mc):.2f}")
print(f"Put Price Difference: ${abs(put_bs - put_mc):.2f}")
