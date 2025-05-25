import pandas as pd
import streamlit as st
import os
import sys
import time

from stock_screener.stock_screener import sp500_tickers, fetch_stock_info
from stock_screener.visualization_stock import plot_price_history, plot_volume_trend

def stock_screener_app():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    st.header("S&P500 Stock Screener")
    st.markdown("This is a stock screener for all S&P 500 companies")
    
    tickers_input = st.text_input("Enter stock tickers (separated by spaces)", value = "TSLA AMZN AAPL MSFT NVDA")
    tickers = tickers_input.upper().split()
    
    if not tickers:
        st.warning("Please enter at least one ticker")
        return
    
    st.sidebar.subheader("Filters")
    min_pe = st.sidebar.number_input("Min P/E Ratio", 0.0, 100.0, 0.0)
    max_pe = st.sidebar.number_input("Max P/E Ratio", 0.0, 100.0, 50.0)
    min_price = st.sidebar.number_input("Min Price", 0.0, 1000.0, 0.0)
    max_price = st.sidebar.number_input("Max Price", 0.0, 10000.0, 5000.0)
    min_eps = st.sidebar.number_input("Min EPS", 0.0, 100.0, 0.0)
    sector = st.sidebar.text_input("Sector (optional)")
    min_volume = st.sidebar.number_input("Min Volume", 0, 1000000000, 0)
    min_div = st.sidebar.number_input("Min Dividend Yield", 0.0, 10.0, 0.0)
    cap_filter = st.sidebar.selectbox("Market Cap Category", ["All", "Large", "Mid", "Small"])
    
    with st.spinner("Fetching stock data..."):
        data = fetch_stock_info(tickers)

    if not data:
        st.warning("No data found. Please check the tickers or try again later.")
        return
    
    filtered = []
    for d in data:
        if (
            d["PE Ratio"] is not None and
            min_pe <= d["PE Ratio"] <= max_pe and
            d["EPS"] is not None and
            d["EPS"] >= min_eps and 
            d["Price"] is not None and
            min_price <= d["Price"] <= max_price and
            d["Volume"] is not None and
            d["Volume"] >= min_volume and
            d["Dividend Yield"] is not None and 
            d["Dividend Yield"] >= min_div and
            (sector.lower() in d["Sector"].lower() if sector and d["Sector"] else True)
        ):
            mc = d["Market Cap"]
            if cap_filter == "Large" and mc >= 10e9:
                break
            if cap_filter == "Mid" and (2e9 <= mc < 10e9):
                break
            if cap_filter == "Small" and mc < 2e9:
                break
            filtered.append(d)
            
    df = pd.DataFrame(filtered)
    
    if df.empty:
        st.warning("No matching stocks")
        return
    
    sort_col = st.selectbox("Sort by", df.columns, index = 1)
    ascending = st.radio("Order", ["Ascending", "Descending"]) == "Ascending"
    df = df.sort_values(by = sort_col, ascending = ascending)
    
    search = st.text_input("Search ticker or company")
    if search:
        df = df[df["Ticker"].str.contains(search.upper()) | df["Company"].str.contains(search, case = False)]
    
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index = False), 'filtered_sp500.csv')
    
    if not df.empty:
        selected = st.selectbox("Select Ticker for Chart", df["Ticker"].tolist())
        time_range = st.selectbox("Select Time Range", ["1w", "1mo", "3mo", "6mo", "1y", "5y", "max"], index = 2)
        if selected:
            plot_price_history(selected, time_range)
            plot_volume_trend(selected, time_range)