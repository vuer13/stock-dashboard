from app.monte_carlo_app import monte_carlo_app as monte_carlo
from app.stock_screener_app import stock_screener_app as stock_screener

import streamlit as st

st.set_page_config(page_title = "Finance Dashboard", layout = "wide")

st.title("Financial Dashboard")

tool = st.sidebar.radio("Choose Tool", ["Monte Carlo Option Pricer", "S&P 500 Stock Screener"])

if tool == "Monte Carlo Option Pricer":
    monte_carlo()
else:
    stock_screener()
