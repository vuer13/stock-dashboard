import pandas as pd
import os
from dotenv import load_dotenv
import requests
import streamlit as st

def sp500_tickers():
    """
    Gets all S&P500 companies
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)[0]
    return table[["Symbol", "Security", "GICS Sector"]].rename(
        columns = {"Symbol": "Ticker", "Security": "Company", "GICS Sector": "Sector"}
    )
    
def fetch_stock_info(tickers):
    load_dotenv()
    API_KEY = os.getenv("FMP_API_KEY")
    
    try:
        tickers_str = ",".join(tickers)
        url = f"https://financialmodelingprep.com/api/v3/profile/{tickers_str}?apikey={API_KEY}"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        results = []
        for info in data:
            results.append({
                "Ticker": info.get("symbol"),
                "Company": info.get("companyName"),
                "Price": info.get("price"),
                "PE Ratio": info.get("pe"),
                "EPS": info.get("eps"),
                "Volume": info.get("volAvg"),
                "Beta": info.get("beta"),
                "Dividend Yield": info.get("lastDiv"),
                "Market Cap": info.get("mktCap"),
                "Sector": info.get("sector")
            })
        return results

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []