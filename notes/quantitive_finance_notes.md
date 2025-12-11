---
title: "Course: Quantitative Finance & Algorithmic Trading in Python | Udemy"
description: >-
  Stock Market, Bonds, Markowitz-Portfolio Theory, CAPM, Black-Scholes Model,
  Value at Risk and Monte-Carlo Simulations
author: Udemy
source: >-
  https://www.udemy.com/course/quantitative-finance-algorithmic-trading-in-python/
created: "2025-12-01"
tags:
  - hover-notes
  - udemy
---

# Quantitative Finance Course Notes

## 1. Time Value of Money

### Core Concept
Money today is worth more than money in the future because:
- **Investment opportunity**: Money can be invested (bonds, stocks) to earn returns
- **Inflation**: Purchasing power decreases over time
- **Risk premium**: Lenders require compensation for time and risk

### Discrete Model

**Future Value:**
```
FV = PV × (1 + r)^n
```
- `FV` = Future Value
- `PV` = Present Value  
- `r` = interest rate (per period)
- `n` = number of periods

**Present Value:**
```
PV = FV / (1 + r)^n
```
Present value discounts future cash flows back to today.

### Continuous Model

Uses differential equations to model continuous compounding.

**Differential Equation:**
```
dx(t)/dt = r × x(t)
```

**Solution:**
```
FV = PV × e^(r×t)
PV = FV × e^(-r×t)
```

Where `e` is the base of natural logarithm and `t` is time in years.

### Python Implementation

```python
from math import exp

# Discrete Model
def future_discrete_value(x, r, n):
    return x * (1 + r)**n

def present_discrete_value(x, r, n):
    return x * (1 + r)**-n

# Continuous Model
def future_continuous_value(x, r, t):
    return x * exp(r * t)

def present_continuous_value(x, r, t):
    return x * exp(-r * t)
```

---

## 2. Financial Assets

### Stocks

**Definition**: Stocks represent ownership shares in a company.

**Key Characteristics:**
- Stock prices `S(t)` follow a **random walk** pattern
- Prices fluctuate based on supply and demand
- **Volatility** measures risk (standard deviation of returns)
- Investors can earn returns through:
  - **Capital appreciation**: Selling at higher price
  - **Dividends**: Quarterly/semi-annual payments

**Why Stock Prices Fluctuate:**
- Market sentiment and news
- Company performance
- Economic conditions
- Supply and demand dynamics

### Commodities

**Definition**: Raw products (gold, oil, natural gas).

**Characteristics:**
- Prices behave like random walks
- **Futures contracts**: Used by producers to hedge against price volatility
- Example: Airlines use oil futures to protect against rising fuel costs
- **Inflation hedge**: Commodity prices typically rise with inflation

**Investment Strategies:**
- Direct commodity investment
- Invest in companies dependent on commodities (e.g., gold mines)

### Currencies and Forex

**Exchange Rate**: Rate at which one currency can be exchanged for another.

**Key Factors Affecting Exchange Rates:**
1. **Interest Rates**: Higher rates attract foreign investment, strengthening currency
2. **Money Supply**: Excessive printing causes inflation, weakening currency
3. **Economic Growth**: Strong economies attract investment
4. **Financial Stability**: Stable countries attract capital

**Forex Market:**
- Largest financial market globally
- 24/7 trading
- High liquidity
- Exchange rates follow random walk patterns

**Arbitrage Opportunities:**
- Rare mispricings can create riskless profit opportunities
- Detected using graph algorithms (Bellman-Ford) to find negative cycles
- Requires high-frequency trading due to rapid correction

### Long vs Short Positions

**Long Position:**
- Own the security
- Profit when price increases
- Maximum loss: 100% of investment
- Strategy: Buy low, sell high

**Short Position:**
- Sell borrowed security
- Profit when price decreases
- Maximum loss: Unlimited (no upper bound on price increase)
- Strategy: Sell high, buy back low
- Much riskier than long positions

**Market Conditions:**
- **Bull Market**: Rising prices → Use long positions
- **Bear Market**: Falling prices → Use short positions

---

## 3. Bonds

### Overview

**Definition**: Debt investment where investor loans money to entity (company/government) for defined period.

**Types:**
1. **Zero-Coupon Bonds**: No periodic payments, only principal at maturity
2. **Coupon Bonds**: Regular interest payments + principal at maturity

### Zero-Coupon Bonds

**Key Parameters:**
- **Principal (Face Value)**: Amount repaid at maturity (e.g., $1000)
- **Premium (Interest Rate)**: Rate paid for the loan
- **Maturity Date**: When bond expires and principal is repaid

**Pricing:**
- Price today = Present value of principal
- Uses discounting: `Price = Principal / (1 + r)^n` (discrete)
- Or: `Price = Principal × e^(-r×t)` (continuous)

### Coupon Bonds

**Structure:**
- Regular coupon payments (interest) at fixed intervals
- Principal repaid at maturity
- Cash flows: `[Coupon, Coupon, ..., Coupon + Principal]`

**Pricing:**
Sum of present values of all cash flows:
```
Price = Σ(Coupon / (1+r)^t) + Principal / (1+r)^n
```

### Yield to Maturity (YTM)

**Definition**: The total return expected if bond is held until maturity.

**Calculation:**
- Internal rate of return (IRR) that equates bond price to present value of cash flows
- Solved numerically (no closed-form solution)

**Yield Curve:**
- Graph showing yields for bonds of different maturities
- Typically upward sloping (longer maturities = higher yields)
- Inverted yield curve can signal economic recession

### Bond Price and Interest Rate Relationship

**Inverse Relationship:**
- When market interest rates ↑ → Bond prices ↓
- When market interest rates ↓ → Bond prices ↑

**Why?** Existing bonds with fixed coupon rates become less attractive when new bonds offer higher rates.

### Macaulay Duration

**Definition**: Weighted average time until cash flows are received.

**Purpose:**
- Measures bond's sensitivity to interest rate changes
- Higher duration = greater price volatility
- Used for immunization strategies

### Bond Risks

1. **Interest Rate Risk**: Price changes with market rates
2. **Credit Risk**: Issuer may default
3. **Inflation Risk**: Purchasing power erosion
4. **Liquidity Risk**: Difficulty selling before maturity

---

## 4. Statistics and Numerical Measures

### Expected Value (Mean)

**Definition**: Weighted average of possible outcomes.

```
E[x] = Σ(x_i × p_i)
```

Where `x_i` are outcomes and `p_i` are probabilities.

### Variance and Standard Deviation

**Variance:**
```
σ² = E[(x - μ)²]
```

**Standard Deviation:**
```
σ = √σ²
```

Measures dispersion around the mean. Higher variance = higher risk.

### Covariance

**Definition**: Measure of how two variables move together.

```
Cov(x,y) = E[(x - μ_x)(y - μ_y)]
```

- **Positive covariance**: Variables move in same direction
- **Negative covariance**: Variables move in opposite directions
- **Zero covariance**: No linear relationship

### Correlation

**Definition**: Normalized covariance (dimensionless, range [-1, 1]).

```
ρ(x,y) = Cov(x,y) / (σ_x × σ_y)
```

- **ρ = 1**: Perfect positive correlation
- **ρ = -1**: Perfect negative correlation  
- **ρ = 0**: No correlation

**Portfolio Implication**: Lower correlation between assets reduces portfolio risk through diversification.

---

## 5. Modern Portfolio Theory (Markowitz Model)

### Core Principle

**Diversification**: Combining multiple assets reduces portfolio risk without necessarily reducing returns.

**Key Insight**: Uncorrelated asset movements cancel each other out, reducing overall volatility.

### Assumptions

1. Returns are normally distributed
2. Investors are risk-averse (require higher return for higher risk)
3. Only long positions allowed (no short selling)
4. Based on historical data (past performance predicts future)

### Portfolio Mathematics

**Notation:**
- `w_i`: Weight of asset `i` in portfolio (Σw_i = 1)
- `r_i`: Return of asset `i`
- `μ_i`: Expected return of asset `i` (mean of historical returns)

**Portfolio Expected Return:**
```
μ_p = Σ(w_i × μ_i) = w^T × μ
```

**Portfolio Variance:**
```
σ_p² = ΣΣ(w_i × w_j × σ_ij) = w^T × Σ × w
```

Where `Σ` is the covariance matrix.

**Covariance Matrix:**
- Diagonal: Variances (σ_ii = σ_i²)
- Off-diagonal: Covariances (σ_ij)

### Efficient Frontier

**Definition**: Set of portfolios offering:
- Highest return for given risk level, OR
- Lowest risk for given return level

**Efficient Portfolio**: Cannot improve return without increasing risk, or reduce risk without decreasing return.

### Portfolio Optimization

**Objective**: Find optimal weights `w*` that:
- Maximize Sharpe ratio (risk-adjusted return)
- Or minimize risk for target return
- Subject to: Σw_i = 1, w_i ≥ 0

**Methods:**
- Quadratic programming
- Numerical optimization (scipy.optimize)

### Returns Calculation

**Simple Returns:**
```
r(t) = (S(t+1) - S(t)) / S(t)
```

**Log Returns:**
```
r(t) = ln(S(t+1) / S(t))
```

Log returns are commonly used because:
- Additive over time periods
- Better for normalization in ML
- Symmetric (handles large moves better)

---

## 6. Sharpe Ratio

### Definition

**Sharpe Ratio** measures risk-adjusted return:

```
Sharpe Ratio = (μ_p - r_f) / σ_p
```

Where:
- `μ_p` = Portfolio expected return
- `r_f` = Risk-free rate
- `σ_p` = Portfolio standard deviation (risk)

### Interpretation

- **Higher Sharpe Ratio** = Better risk-adjusted performance
- Compares excess return per unit of risk
- Allows comparison across different portfolios

### Capital Allocation Line (CAL)

**Definition**: Line showing risk-return combinations from combining risky portfolio with risk-free asset.

**Formula:**
```
E[R] = r_f + (μ_p - r_f) / σ_p × σ
```

**Slope** = Sharpe Ratio

**Optimal Portfolio**: Tangent portfolio on efficient frontier (highest Sharpe ratio).

---

## 7. Capital Asset Pricing Model (CAPM)

### Core Concept

**CAPM** relates expected return to systematic risk (market risk).

**Key Insight**: Unsystematic risk can be diversified away. Only systematic risk matters.

### CAPM Formula

```
E[r_i] = r_f + β_i × (E[r_m] - r_f)
```

Where:
- `E[r_i]` = Expected return of asset `i`
- `r_f` = Risk-free rate
- `β_i` = Beta (sensitivity to market)
- `E[r_m]` = Expected market return
- `(E[r_m] - r_f)` = Market risk premium

### Beta (β)

**Definition**: Measure of systematic risk relative to market.

**Calculation:**
```
β_i = Cov(r_i, r_m) / Var(r_m)
```

**Interpretation:**
- **β = 1**: Moves with market
- **β > 1**: More volatile than market (aggressive)
- **β < 1**: Less volatile than market (defensive)
- **β < 0**: Moves opposite to market (rare)

**Portfolio Beta:**
```
β_p = Σ(w_i × β_i)
```

### Alpha (α)

**Definition**: Excess return above CAPM prediction.

```
α = Actual Return - CAPM Predicted Return
```

- **α > 0**: Outperforming market (good)
- **α < 0**: Underperforming market (bad)
- **α = 0**: Performing as expected

### Linear Regression and CAPM

CAPM can be estimated using linear regression:

```
r_i - r_f = α + β × (r_m - r_f) + ε
```

**R-squared (R²)**: Proportion of variance explained by market.
- High R² → Stock moves closely with market
- Low R² → Stock has significant idiosyncratic risk

---

## 8. Derivatives

### Overview

**Definition**: Financial instruments whose value derives from underlying asset.

**Types:**
1. **Options**: Right (not obligation) to buy/sell
2. **Forwards/Futures**: Obligation to buy/sell at future date
3. **Swaps**: Exchange of cash flows

### Options

**Call Option**: Right to **buy** underlying asset at strike price `E` by expiration `T`.

**Put Option**: Right to **sell** underlying asset at strike price `E` by expiration `T`.

**Exercise Styles:**
- **European**: Can only exercise at expiration
- **American**: Can exercise anytime before expiration

**Payoffs:**
- **Call**: `max(S(T) - E, 0)`
- **Put**: `max(E - S(T), 0)`

### Forwards and Futures

**Forward Contract**: Customized agreement to buy/sell asset at future date and price.

**Future Contract**: Standardized forward contract traded on exchange.

**Key Differences:**
- Futures are standardized, forwards are customized
- Futures have daily settlement (marking to market)
- Futures have lower counterparty risk

### Swaps

**Interest Rate Swap**: Exchange fixed-rate payments for floating-rate payments.

**Credit Default Swap (CDS)**: Insurance against bond default.

**Collateralized Debt Obligations (CDOs)**:
- Pool of debt instruments (mortgages, loans)
- Divided into tranches (senior, junior, risky)
- **Diversification crucial**: Must contain uncorrelated assets
- 2008 crisis caused by over-concentration in mortgages

---

## 9. Random Behavior and Stochastic Processes

### Random Walk

**Definition**: Path where each step is random and independent.

**Stock Price Behavior**: Stock prices follow random walk patterns, making future prices unpredictable.

### Wiener Process (Brownian Motion)

**Properties:**
1. **Independent increments**: Future changes independent of past
2. **Gaussian increments**: Changes normally distributed
3. **Mean 0, variance dt**: `W(t+dt) - W(t) ~ N(0, dt)`

**Mathematical Definition:**
```
dW(t) = ε × √dt
```
Where `ε ~ N(0,1)` is standard normal random variable.

### Geometric Brownian Motion (GBM)

**Model for Stock Prices:**
```
dS(t) = μ × S(t) × dt + σ × S(t) × dW(t)
```

Where:
- `μ` = Drift (expected return)
- `σ` = Volatility (standard deviation)
- `dW(t)` = Wiener process

**Solution:**
```
S(t) = S(0) × exp[(μ - σ²/2)t + σ × W(t)]
```

**Properties:**
- Stock prices cannot be negative (log-normal distribution)
- Returns are normally distributed
- Volatility scales with √t

### Stochastic Calculus

**Ito's Lemma**: For function `F(S,t)` of stock price `S(t)`:

```
dF = (∂F/∂t + μS × ∂F/∂S + ½σ²S² × ∂²F/∂S²)dt + σS × ∂F/∂S × dW
```

**Key Tool**: Used to derive Black-Scholes equation.

---

## 10. Black-Scholes Model

### Overview

**Published**: 1973 by Fisher Black, Robert Merton, and Myron Scholes

**Purpose**: Calculate fair price of European options.

**Key Insight**: Can eliminate risk by combining option with underlying stock (delta-hedging).

### Assumptions

1. Stock follows geometric Brownian motion
2. No dividends during option life
3. Risk-free rate is constant
4. No transaction costs
5. Continuous trading
6. No arbitrage opportunities

### Delta-Hedging

**Strategy**: Create riskless portfolio by:
- Long position in option: `V(S,t)`
- Short position in stock: `-Δ × S`

**Delta (Δ)**: `Δ = ∂V/∂S` (sensitivity to stock price)

**Result**: Eliminates stochastic (random) component, leaving only deterministic part.

### Black-Scholes Differential Equation

```
∂V/∂t + ½σ²S² × ∂²V/∂S² + rS × ∂V/∂S - rV = 0
```

**Boundary Conditions:**
- **Call**: `V(S,T) = max(S - E, 0)`
- **Put**: `V(S,T) = max(E - S, 0)`

### Black-Scholes Formula

**Call Option Price:**
```
C = S × N(d1) - E × e^(-rT) × N(d2)
```

**Put Option Price:**
```
P = E × e^(-rT) × N(-d2) - S × N(-d1)
```

**Parameters:**
```
d1 = [ln(S/E) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T
```

Where:
- `S` = Current stock price
- `E` = Strike price
- `r` = Risk-free rate
- `T` = Time to expiration
- `σ` = Volatility
- `N(·)` = Standard normal cumulative distribution

### The Greeks

**Delta (Δ)**: Sensitivity to stock price
- Call: `Δ = N(d1)` (0 to 1)
- Put: `Δ = N(d1) - 1` (-1 to 0)

**Gamma (Γ)**: Rate of change of delta
- `Γ = N'(d1) / (S × σ√T)`

**Theta (Θ)**: Time decay
- `Θ = -∂V/∂t` (negative = value decreases with time)

**Vega (ν)**: Sensitivity to volatility
- `ν = S × N'(d1) × √T`

**Rho (ρ)**: Sensitivity to interest rate
- `ρ = E × T × e^(-rT) × N(d2)` (for calls)

---

## 11. Monte Carlo Simulations

### Overview

**Purpose**: Estimate values by simulating many random scenarios.

**Applications:**
- Option pricing
- Stock price forecasting
- Value at Risk (VaR)
- Bond pricing with stochastic interest rates

### Stock Price Simulation

**GBM Simulation:**
```
S(t) = S(0) × exp[(μ - σ²/2)t + σ√t × N(0,1)]
```

**Steps:**
1. Generate random normal variables
2. Calculate stock price for each scenario
3. Average results to get expected value

### Option Pricing with Monte Carlo

**For Call Option:**
1. Simulate many stock price paths to expiration
2. Calculate payoff: `max(S(T) - E, 0)`
3. Discount to present: `Payoff × e^(-rT)`
4. Average all discounted payoffs

**Advantages:**
- Works for complex payoffs
- No closed-form solution needed
- Can handle path-dependent options

**Disadvantages:**
- Computationally intensive
- Requires many simulations for accuracy

---

## 12. Value at Risk (VaR)

### Definition

**VaR**: Maximum potential loss over given time period with specified confidence level.

**Example**: "99% VaR of $5,000" means:
- 99% chance loss will not exceed $5,000
- 1% chance loss could be greater

### Variance Method (Parametric)

**Assumption**: Returns are normally distributed.

**Formula:**
```
VaR = Position × [μ × δt - σ × √(δt) × z]
```

For small `δt` (daily):
```
VaR = -Position × σ × √(δt) × z
```

Where:
- `z` = z-score for confidence level
  - 95%: z = 1.64
  - 99%: z = 2.33

**Multi-day VaR:**
```
σ_N = σ_daily × √N
μ_N = μ_daily × N
```

### Monte Carlo Method

**Steps:**
1. Simulate many stock price paths (e.g., 10,000)
2. Calculate returns for each path
3. Sort returns
4. Take percentile corresponding to confidence level

**Advantages:**
- No normality assumption
- Works for complex portfolios
- Can model non-linear relationships

### Empirical Method

**Approach**: Use historical data directly.

**Steps:**
1. Collect historical returns
2. Sort returns
3. Take percentile corresponding to confidence level

**Advantages:**
- No distribution assumptions
- Uses actual historical behavior

**Disadvantages:**
- Assumes past predicts future
- Requires sufficient historical data

### Portfolio VaR

**Considerations:**
- Correlation between assets reduces portfolio VaR
- Diversification benefit: Portfolio VaR < Sum of individual VaRs
- Requires covariance matrix

---

## 13. Interest Rate Modeling

### Challenge

Interest rates `r(t)` fluctuate continuously and are affected by:
- Political decisions
- Government interventions
- Economic conditions

### Vasicek Model

**Published**: 1977 by Oldřich Vašíček

**Model**: Interest rates follow mean-reverting Ornstein-Uhlenbeck process:

```
dr(t) = κ(θ - r(t))dt + σ × dW(t)
```

Where:
- `κ` = Speed of mean reversion
- `θ` = Long-term mean (equilibrium rate)
- `σ` = Volatility
- `dW(t)` = Wiener process

**Properties:**
- Mean-reverting (pulls toward `θ`)
- Can go negative (limitation)
- Stationary process

### Ornstein-Uhlenbeck Process

**General Form:**
```
dx(t) = θ(μ - x(t))dt + σ × dW(t)
```

**Applications:**
- Interest rate modeling (Vasicek)
- Currency exchange rates
- Pairs trading strategies

**Pairs Trading:**
- Identify correlated assets (e.g., Coca-Cola and Pepsi)
- When spread deviates from mean, expect reversion
- Open positions expecting return to mean

### Bond Pricing with Stochastic Rates

**Challenge**: Bond price depends on future interest rates, which are uncertain.

**Solution**: Monte Carlo simulation
1. Simulate many interest rate paths using Vasicek model
2. Calculate present value of bond cash flows for each path
3. Average results to get expected bond price

---

## 14. Investment Strategies

### Fundamental Analysis

**Approach**: Study company fundamentals to determine intrinsic value.

**Factors Analyzed:**
- Balance sheet (assets, liabilities)
- Income statement (revenues, expenses)
- Cash flow statement
- Management quality
- Industry position

**Metrics:**
- **P/E Ratio**: Price-to-earnings (lower = better value)
- **EPS**: Earnings per share

**Strategy**: Buy when market price < intrinsic value (undervalued).

**Limitations:**
- Requires deep company knowledge
- Market may not recognize value quickly
- Intrinsic value is subjective

### Technical Analysis

**Approach**: Analyze historical price patterns to predict future movements.

**Key Principle**: "History repeats itself" - patterns in past data will recur.

**Methods:**
- Chart patterns
- Technical indicators (moving averages, RSI, etc.)
- Machine learning (pattern recognition)

**Assumption**: All information is in the price/volume data.

**Criticism**: Efficient Market Hypothesis suggests patterns are random.

### Quantitative Analysis

**Approach**: Model financial quantities as random processes using mathematics.

**Tools:**
- Statistics
- Probability theory
- Stochastic calculus
- Numerical methods

**Applications:**
- Option pricing
- Portfolio optimization
- Risk management
- Algorithmic trading

### Long-Term Investing (Value Investing)

**Philosophy**: Buy and hold undervalued companies for long term.

**Key Figures**: Benjamin Graham, Warren Buffett

**Principles:**
- Focus on company fundamentals, not short-term price movements
- Buy when price < intrinsic value
- Hold for long term (years, not days)
- Ignore market noise and crowd behavior

**Difference from Quantitative Finance:**
- No mathematical models
- No short-term trading
- Focus on business value, not price patterns

---

## 15. Efficient Market Hypothesis (EMH)

### Core Statement

**"It is impossible to beat the market consistently."**

**Reasoning**: Stock prices always reflect all available information, so:
- No undervalued stocks exist
- Price movements are random (random walk)
- Historical data cannot predict future

### Implications

1. **Stock prices are fair**: Always at intrinsic value
2. **Random walk**: Price changes are unpredictable
3. **Low autocorrelation**: Returns have minimal serial correlation
4. **No arbitrage**: Mispricings are instantly corrected

### Criticisms

**Counterexamples:**
- **Fidelity Investments** (Peter Lynch): 29% annual return (1977-1990)
- **Renaissance Technologies** (James Simons): 34% annual return
- **Warren Buffett**: 22% annual return

**Challenges:**
- ARIMA and GARCH models can sometimes predict
- Behavioral finance shows market inefficiencies
- Some strategies consistently outperform

**Conclusion**: EMH is a useful theoretical framework but markets are not perfectly efficient in practice.

---

## Key Takeaways

### Fundamental Principles

1. **Time Value of Money**: Money today > money tomorrow
2. **Risk-Return Tradeoff**: Higher risk requires higher expected return
3. **Diversification**: Reduces unsystematic risk
4. **Random Behavior**: Financial markets exhibit stochastic properties
5. **No Arbitrage**: Riskless profits are quickly eliminated

### Mathematical Tools

- **Statistics**: Mean, variance, covariance, correlation
- **Optimization**: Portfolio construction, efficient frontier
- **Stochastic Calculus**: Modeling random processes (Ito's lemma)
- **Monte Carlo**: Numerical simulation for complex problems
- **Differential Equations**: Black-Scholes, interest rate models

### Practical Applications

- **Portfolio Management**: Markowitz optimization, CAPM
- **Risk Management**: VaR, stress testing
- **Option Pricing**: Black-Scholes, Monte Carlo
- **Bond Pricing**: Yield calculations, duration analysis
- **Algorithmic Trading**: Quantitative strategies, pairs trading

### Important Models

1. **Geometric Brownian Motion**: Stock price modeling
2. **Black-Scholes**: Option pricing
3. **Markowitz**: Portfolio optimization
4. **CAPM**: Risk-return relationship
5. **Vasicek**: Interest rate modeling

---

*This document consolidates and organizes key concepts from the Quantitative Finance course, removing duplicates and improving clarity while maintaining essential information.*
