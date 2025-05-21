from scipy.stats import norm, qmc
from scipy.optimize import brentq
import numpy as np

def bs_price(S, K, T, r, sigma, option_type = 'call'):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * t)/(sigma/np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(t)

    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    else:
        return K * np.exp(-r * t) * norm.cdf(d2) - S * norm.cdf(d1)

def implied_volatility(S, K, T, r, option_price, option_type = 'call'):
    try:
        return brentq(lambda sigma: bs_price(S, K, T, r, sigma, option_type) - option_price, 1e-6, 5)
    except ValueError:
        return np.nan

def simulate_terminal_prices(S0, r, sigma, T, N):
    """
    S0: Initial Stock Price
    r: Risk-free interest rate
    sigma: Volatility
    T: Time to mature (in years)
    N: # of simulations
    """

    Z = np.random.randn(N // 2)
    Z = np.concatenate([Z, -Z])
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z) # all simulated future prices based on Z from before

    return ST

def simulate_terminal_prices_sobol(S0, r, sigma, T, N):
    """
    Generates realistic and more uniform distributed stock paths
    """

    sampler = qmc.Sobol(d = 1, scramble = True)
    U = sampler.random(n = N)
    Z = norm.ppf(U).flatten()
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z) 

    return ST

def compute_payoffs(ST, K, option_type):
    """
    ST: array of terminal prices
    """
    if option_type == 'call':
        return np.maximum(ST - K, 0)
    else:
        return np.maximum(K - ST, 0)

def discount_payoffs(payoffs, r, T):
    """
    payoffs: array of payoffs at expiration from before
    """
    return np.exp(-r * T) * np.mean(payoffs)

def ci_95(payoffs, r, T, z = 1.96):
    mean = np.mean(payoffs)
    std_err = np.std(payoffs) / np.sqrt(len(payoffs))

    lower_bound = mean - z * std_err
    upper_bound = mean + z * std_err

    # Discount values to get current value
    lower_discounted = np.exp(-r * T) * lower_bound
    upper_discounted = np.exp(-r * T) * upper_bound
    
    return lower_discounted, upper_discounted

def estimate_delta(S0, K, T, r, sigma, N, option_type, eps = 1e-2, use_sobol = False):
    """
    Option price change if stock changes
    """
    price_up = price_option(S0 + eps, K, T, r, sigma, N, option_type)
    price_down = price_option(S0 - eps, K, T, r, sigma, N, option_type)
    return (price_up - price_down) / (2 * eps)

def estimate_vega(S0, K, T, r, sigma, N, option_type, eps = 1e-2, use_sobol = False):
    """
    Option Price change if volatility changes
    """
    price_up = price_option(S0, K, T, r, sigma + eps, N, option_type)
    price_down = price_option(S0, K, T, r, sigma - eps, N, option_type)
    return (price_up - price_down) / (2 * eps)
    
def price_option(S0, K, T, r, sigma, N, option_type, use_sobol = False):
    """
    Returns option price
    """
    if use_sobol:
        ST = simulate_terminal_prices_sobol(S0, r, sigma, T, N)
    else:
        ST = simulate_terminal_prices(S0, r, sigma, T, N)
    payoffs = compute_payoffs(ST, K, option_type)
    return discount_payoffs(payoffs, r , T)