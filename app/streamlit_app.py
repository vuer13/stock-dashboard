import streamlit as st
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.main import (
    implied_volatility,
    simulate_terminal_prices,
    simulate_terminal_prices_sobol,
    compute_payoffs,
    discount_payoffs,
    ci_95,
    estimate_delta,
    estimate_vega
)

from core.visualization import (
    plot_dist,
    payoff_vs_price,
    convergence_plot,
    delta_compared_stock
)

st.set_page_config(page_title = "Option Pricer", layout = "centered")

st.title("Monte Carlo European Option Pricer")
st.markdown("This tool uses Monte Carlo simulation to estimate the price of European option.")
st.markdown("Adjust the simulation inputs on the side and run the simulations!")

# SIDEBAR
st.sidebar.header("Simulation Inputs")

S0 = st.sidebar.slider("Initial Stock Price (S₀)", 10.0, 300.0, 100.0, step = 1.0)
K = st.sidebar.slider("Strike Price (K)", 10.0, 300.0, 105.0, step = 1.0)
T = st.sidebar.slider("Time to Expiry (Years)", 0.1, 5.0, 1.0, step = 0.1)
r_percent = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 10.0, 5.0, step = 0.1)
r = r_percent / 100 

option_type = st.sidebar.radio("Option Type", ["call", "put"])
market_price = st.sidebar.number_input("Observed Market Price", min_value = 0.0, value = 7.2, step = 0.1)
N = st.sidebar.select_slider("Number of Simulations", options=[1000, 5000, 10000, 50000, 100000, 250000, 500000], value = 10000)
use_sobol = st.sidebar.checkbox("Use Sobol Sampling?", value = False)

st.sidebar.markdown("-----")

with st.sidebar.expander("What do these inputs mean?"):
    st.markdown(""" 
                ### Input Glossary
                - **S₀** — Current stock price (the value of the asset right now).
                - **K** — Strike price (price agreed for buying/selling the asset).
                - **T** — Time to maturity (in years).
                - **r** — Risk-free interest rate (used to discount future value).
                - **Market Price** — Actual observed price of the option in the market.
                - **Simulations** — Number of Monte Carlo paths to run.
                - **Sobol Sampling** — Use quasi-random numbers for faster convergence.
                """)

run = st.button("Run Simulation")

if run:
    st.subheader("Results")
    
    try:
        sigma = implied_volatility(S0, K, T, r, market_price, option_type)
        if np.isnan(sigma):
            raise ValueError("Volatility returned NaN")
    except Exception as e:
        st.error("Implied Volatility could not be calculated")
        st.stop()

    if use_sobol:
        ST = simulate_terminal_prices_sobol(S0, r, sigma, T, N)
    else:
        ST = simulate_terminal_prices(S0, r, sigma, T, N)
        
    payoffs = compute_payoffs(ST, K, option_type)
    price = discount_payoffs(payoffs, r, T)
    ci_low, ci_high = ci_95(payoffs, r, T)
    
    delta = estimate_delta(S0, K, T, r, sigma, N, option_type, use_sobol)
    vega = estimate_vega(S0, K, T, r, sigma, N, option_type, use_sobol)
    
    st.markdown(f"- Implied Volatility: {sigma:.4f}")
    st.markdown(f"- Option Price: {price:.2f}")
    st.markdown(f"- 95% Confidence Interval: [{ci_low:.4f}, {ci_high:.4f}]")
    st.markdown(f"- Delta: {delta:.4f}")
    st.markdown(f"- Vega: {vega:.4f}")
    
    st.subheader("Visualizations")
    
    dist_path = plot_dist(ST, payoffs, option_type)
    st.image(dist_path, caption = "Simulated Terminal Prices & Payoffs")
    
    payoff_path = payoff_vs_price(ST, payoffs, option_type)
    st.image(payoff_path, caption="Payoff vs Terminal Price")
    
    conv_path = convergence_plot(S0, K, r, sigma, T, option_type, use_sobol)
    st.image(conv_path, caption = "Convergence of Option Price")
    
    delta_path = delta_compared_stock(K, T, r, sigma, N, option_type, use_sobol)
    st.image(delta_path, caption = "Delta vs Stock Price")
    
    st.markdown("-----")
    
    with st.expander("What does everything mean?"):
        st.markdown(""" 
                    ### Output Explained
                    - **Implied Volatility (σ)** — The volatility that makes the Black-Scholes price match the observed market price.
                    - **Option Price** — Your simulated fair value using Monte Carlo.
                    - **Confidence Interval** — Range for the true option price with 95% confidence that it falls in this range.
                    - **Delta** — How much the option price changes when the stock price changes.
                    - **Vega** — How much the option price changes with a change in volatility.

                    ### Plot Descriptions
                    - **Terminal Price Histogram** — Distribution of final stock prices from simulations.
                    - **Payoff Histogram** — Distribution of the option payoffs at expiry.
                    - **Payoff vs Terminal Price** — Shows how payoff changes with the ending stock price.
                    - **Delta vs Stock Price** — How Delta behaves across different stock prices.
                    - **Convergence Plot** — Shows how simulation accuracy improves with more runs.
                    """)

    