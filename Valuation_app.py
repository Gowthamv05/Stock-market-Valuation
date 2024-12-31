

import streamlit as st
import yfinance as yf


# Function to fetch stock data
def get_stock_data(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d")
        return {
            "current_price": data['Close'][-1],
            "market_cap": stock.info.get("marketCap", "N/A"),
            "pe_ratio": stock.info.get("trailingPE", "N/A"),
            "sector": stock.info.get("sector", "N/A")
        }
    except Exception as e:
        return {"error": str(e)}

# Function to evaluate stock valuation
def evaluate_stock(pe_ratio, industry_average_pe=20):
    if pe_ratio == "N/A":
        return "PE ratio not available, unable to evaluate"
    if pe_ratio < industry_average_pe * 0.8:
        return "Undervalued, you can invest on this stock🤑"
    elif pe_ratio > industry_average_pe * 1.2:
        return "Overvalued, Avoid doing lumpsum investment👺"
    else:
        return "Fairly Valued 🤝"

# Streamlit UI
st.title("Indian Stock Market Valuation💹")
st.markdown("Enter the stock symbol to fetch its current price and valuation status.")

stock_symbol = st.text_input("Enter Stock Symbol (e.g., TCS.BO for TCS in BSE and TCS.NS for NSE):").strip()

if stock_symbol:
    st.write("Fetching data...")
    stock_data = get_stock_data(stock_symbol)
    
    if "error" in stock_data:
        st.error(f"Error: {stock_data['error']}")
    else:
        st.write(f"**Stock:** {stock_symbol}")
        st.write(f"**Current Price:** ₹{stock_data['current_price']:.2f}")
        st.write(f"**Market Cap:** {stock_data['market_cap']}")
        st.write(f"**Sector:** {stock_data['sector']}")
        st.write(f"**PE Ratio:** {stock_data['pe_ratio']}")
        
        # Valuation evaluation
        valuation_status = evaluate_stock(stock_data['pe_ratio'])
        st.write(f"**Valuation Status:** {valuation_status}")
