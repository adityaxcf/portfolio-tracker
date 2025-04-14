import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Portfolio Tracker", layout="centered")

st.title("📈 Stock Portfolio Tracker")

# Sidebar input
st.sidebar.header("Add Stock")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL)", "")
qty = st.sidebar.number_input("Quantity", min_value=1, step=1)
buy_price = st.sidebar.number_input("Buy Price", min_value=0.0, step=0.1)

portfolio = st.session_state.get('portfolio', [])

if st.sidebar.button("Add to Portfolio"):
    if ticker and qty > 0 and buy_price > 0:
        stock = yf.Ticker(ticker)
        try:
            live_price = stock.info["regularMarketPrice"]
            data = {
                "Ticker": ticker.upper(),
                "Quantity": qty,
                "Buy Price": buy_price,
                "Live Price": live_price,
                "Current Value": qty * live_price,
                "Invested": qty * buy_price,
                "Gain/Loss": (live_price - buy_price) * qty
            }
            portfolio.append(data)
            st.session_state['portfolio'] = portfolio
        except:
            st.sidebar.error("Invalid Ticker or Network Error")

if portfolio:
    df = pd.DataFrame(portfolio)
    st.dataframe(df.style.format({
        "Buy Price": "{:.2f}",
        "Live Price": "{:.2f}",
        "Current Value": "{:.2f}",
        "Invested": "{:.2f}",
        "Gain/Loss": "{:.2f}"
    }))

    total_gain = df["Gain/Loss"].sum()
    st.metric("💸 Total Gain/Loss", f"${total_gain:.2f}")

    fig = go.Figure([go.Pie(labels=df["Ticker"], values=df["Current Value"], hole=.3)])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Add a stock to start tracking your portfolio.")
