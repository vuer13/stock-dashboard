# Monte Carlo European Option Price

The project implements the Monte Carlo simulation for pricing European-style call and put options. It combines stochastic modeling with statistical inference to estimate option prices, confidence intervals and sensitivity measures. The UI is built with Streamlit for users to fully interact and explore pricing behaviours under various market conditions.

## Monte Carlo Simulation
The price of a European option is the expected discounted value of its payoff as expiration. The Monte Carlo method simulates many of potential asset price paths and computes the coresponding payoffs under a risk-neutral measure.

$S_T = S_0 \cdot \exp\left[\left(r - \frac{1}{2} \sigma^2\right) T + \sigma \sqrt{T} \cdot Z\right]$

where $Z~N$(0, 1) are standard normal variables. 

Both Anththetic variates and Sobol quasi-random sampling are supported for users to see the variance and convergence.

## Payoff Computation
Call and put payoffs are computed as:
- Call: max($S_T - K$, 0)
- Put: max($K - S_T$, 0)
These were averaged and discounted: Price = $e^{-rT} \cdot$ E[Payoff]

## Implied Volatility
This inverts the BSM formula using Brent's method, solving the implied volatility that matches the observed market price

## Greeks
These values estimate key sensitivities
- Delta: Sensitivity to $S_0$
- Vega: Sensitivity to $\sigma$

# Application Features
This project includes a Streamlit-based web interface to support user interaction and real-time visualization

Features:
- Adjustable parameters
- Toggle for Sobol Sampling
- Output: Implied Volatility, option price, 95% confidence interval, delta, vega
- Plot generation:
    - Simulated Terminal Price and Payoff Histogram
    - Payoff vs Terminal Price
    - Convergence of price with increasing simulation size
    - Delta vs stock price