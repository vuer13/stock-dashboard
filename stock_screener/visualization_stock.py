import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

def plot_price_history(ticker, period):
    hist = yf.Ticker(ticker).history(period = period)
    fig, ax = plt.subplots()
    ax.plot(hist.index, hist["Close"], label = "Close Price")
    ax.set_ylabel("Price")
    ax.set_xlabel("Date")
    ax.legend()
    
    st.subheader(f"{ticker} - Price History ({period})")
    st.pyplot(fig)
    
def plot_volume_trend(ticker, period):
    hist = yf.Ticker(ticker).history(period = period)
    fig, ax = plt.subplots()
    ax.bar(hist.index, hist["Volume"], color = "blue")
    ax.set_ylabel("Volume")
    ax.set_xlabel("Date")
    
    st.subheader(f"{ticker} - Volume Trend ({period})")
    st.pyplot(fig)