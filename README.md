# Finance Dashboard
This finance dashboard gives users two core features: a Stock Screener to filter and explore key financial metrics for publicly traded companies, and a Monte Carlo Option Pricer to simulate the pricing of European options using probabilistic models. Built entirely with Streamlit, this interactive web app offers a hands-on way to explore both quantitative finance and real-time market data. Users can customize input parameters for option simulations—such as strike price, volatility, and time to maturity—and visualize the payoff and sensitivity of those options. On the stock side, users can input ticker symbols, fetch up-to-date metrics from the FMP API, apply custom filters (like P/E ratio, EPS, volume, and dividend yield), and sort or export their results. This tool is designed to make complex financial analysis more approachable and intuitive through a simple, clean user interface.

## Monte Carlo European Option Price
The project implements the Monte Carlo simulation for pricing European-style call and put options. It combines stochastic modeling with statistical inference to estimate option prices, confidence intervals and sensitivity measures. 

### Monte Carlo Simulation
The price of a European option is the expected discounted value of its payoff as expiration. The Monte Carlo method simulates many of potential asset price paths and computes the corresponding payoffs under a risk-neutral measure.

$S_T = S_0 \cdot \exp\left[\left(r - \frac{1}{2} \sigma^2\right) T + \sigma \sqrt{T} \cdot Z\right]$

where $Z~N$(0, 1) are standard normal variables. 

Both Anthetic variates and Sobol quasi-random sampling are supported for users to see the variance and convergence.

### Payoff Computation
Call and put payoffs are computed as:
- Call: max($S_T - K$, 0)
- Put: max($K - S_T$, 0)
These were averaged and discounted: Price = $e^{-rT} \cdot$ E[Payoff]

### Implied Volatility
This inverts the BSM formula using Brent's method, solving the implied volatility that matches the observed market price

### Greeks
These values estimate key sensitivities
- Delta: Sensitivity to $S_0$
- Vega: Sensitivity to $\sigma$

## Application Features

- Adjustable parameters
- Toggle for Sobol Sampling
- Output: Implied Volatility, option price, 95% confidence interval, delta, vega
- Plot generation:
    - Simulated Terminal Price and Payoff Histogram
    - Payoff vs Terminal Price
    - Convergence of price with increasing simulation size
    - Delta vs stock price

## Stock Screener
This part of the project utilizes the Financial Modeling Prep (FMP) API by making batch API requests to obtain up to date stock prices based on key financial metrics the user wishes to obtain. Users can sort any column and filter based on their liking. At the end, they can download the filtered results into a CSV file. 

### Requirements
Clone this repository to your local machine, activate the virtual environment (optional) and install requirements: 
```bash
git clone https://github.com/vuer13/stock-dashboard.git
cd stock-dashboard

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
To use this application, users need to obtain a FMP API key, and place it in the .env file
```bash
FMP_API_KEY=your_api_key_here
```

### Run this application
```bash
streamlit run main.py
```

### Limitations
The free FMP API tier only supports 250 requests/day, so the application is unable to fetch all tickers.