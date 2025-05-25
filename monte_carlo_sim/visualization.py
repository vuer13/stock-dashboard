import matplotlib.pyplot as plt
import numpy as np

from monte_carlo_sim.monte_carlo import price_option, estimate_delta

def plot_dist(ST, payoffs, option_type):
    """
    Histogram of simulated stock prices and option payoffs
    """
    plt.figure(figsize = (12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(ST, bins = 50, alpha = 0.7)
    plt.title("Simulated Terminal Stock Prices")
    plt.xlabel("S_T")
    plt.ylabel("Frequency")
    
    plt.subplot(1, 2, 2)
    plt.hist(payoffs, bins = 50, alpha = 0.7, color = 'blue')
    plt.title(f'{option_type.capitalize()} Option Payoffs')
    plt.xlabel("Payoffs")
    plt.ylabel("Frequency")
    plt.tight_layout()
    
    path = f'plots/payoff_dist_{option_type}.png'
    plt.savefig(path)
    plt.close()
    return path
    
def convergence_plot(S0, K, r, sigma, T, option_type, use_sobol = False):
    """
    Plots the estimated option price vs number of simulations
    """
    N_values = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    prices = []
    
    for N in N_values:
        price = price_option(S0, K, T, r, sigma, N, option_type, use_sobol)
        prices.append(price)
        
    plt.figure(figsize = (8, 6))
    plt.plot(N_values, prices, marker = 'o')
    plt.xscale('log')
    plt.title(f"Convergence ({option_type.capitalize()})")
    plt.xlabel("Number of Simulations (log scale)")
    plt.ylabel("Estimated Option Price")
    plt.grid(True)
    
    path = f"plots/convergence_{option_type}.png"
    plt.savefig(path)
    plt.close()
    return path
    
def delta_compared_stock(K, T, r, sigma, N, option_type, use_sobol = False):
    """
    Computes delta from stock prices; how it changes
    """
    S_values = np.linspace(K * 0.5, K * 1.5, 25) # stock prices from 50% strike price to 150%
    deltas = [estimate_delta(S, K, T, r, sigma, N, option_type, use_sobol = use_sobol) for S in S_values]
    
    plt.figure(figsize = (8, 6))
    plt.plot(S_values, deltas, marker = 'o')
    plt.title(f"Delta vs Stock Price ({option_type.capitalize()})")
    plt.xlabel("Stock Price")
    plt.ylabel("Delta")
    plt.grid(True)
    path = f"plots/delta_vs_stock_{option_type}.png"
    plt.savefig(path)
    plt.close()
    return path
    
def payoff_vs_price(ST, payoffs, option_type):
    """
    Terminal Stock Price vs resulting payoff
    """
    plt.figure(figsize = (8, 6))
    plt.scatter(ST, payoffs, alpha = 0.1, s = 5)
    plt.title(f"{option_type.capitalize()} Payoff vs Terminal Price")
    plt.xlabel("Simulated Terminal Price (S_T)")
    plt.ylabel("Option Payoff")
    plt.grid(True)
    path = f"plots/payoff_vs_price_{option_type}.png"
    plt.savefig(path)
    plt.close()
    return path