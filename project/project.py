import streamlit as st
from share import Stock
import pandas as pd
import plotly_express as px
import yfinance as yf
from datetime import date, timedelta


def main():
    st.title("Stock Analyser")
    options_array = [None, "Single-Stock", "Multi-Stock"]
    mode = st.selectbox("Enter mode:", options_array)
    today = date.today()
    match mode:
        case "Single-Stock":
            ticker = (st.text_input("Enter Ticker: ", ""))
            if ticker:   
                with st.spinner("⏳ Initializing"):   
                    ticker = None if ticker == "" else ticker.upper()
                    if ticker is not None and validate_single_ticker(ticker): 
                        ticker_object = Stock(ticker= ticker)
                        m = ticker_object.metrics()
                        data = pd.DataFrame(list(m.items()), columns= ["Metric", "Value"])
                        st.table(data)
                        today = date.today()
                        start_date = st.date_input("Enter Start date:",value= today - timedelta(days=365), max_value=today)
                        end_date = st.date_input("Enter Ending Date:", max_value=today)
                        if check_date(start_date, end_date) == 1:
                            st.error("⚠️ Start date must be before end date.")
                        elif check_date(start_date, end_date) == 2:
                            st.warning("📅 Please select a range of at least 7 days.")
                        else:
                            with st.spinner("🗃️ Getting Data"):    
                                hist = ticker_object.get_history(start_date=start_date, end_date=end_date)
                                if st.button("Show Price Graph"):
                                    fig = px.line(hist, x="Date", y="Close", title="Price v/s Time")
                                    st.plotly_chart(fig)
                    else:
                        st.warning("Invalid Ticker")
                    
                        
        case "Multi-Stock":
            ticker = st.text_input("Enter a list of tickers seperated by comma: ")
            with st.spinner("⏳ Initializing"):    
                if ticker:
                    ticker_list = [t.strip() for t in ticker.split(",")]
                    valid_tickers = validate_ticker_list(tickers= ticker_list)
                    # there is room for way more imporvement.
                    # Like showing which are the invalid tickers.
                    # What to do ? If the entire list is invalid.
                    ticker_object_list = [Stock(t) for t in valid_tickers]
                    data = {}
                    for stock in ticker_object_list:
                        data[stock.ticker] = stock.metrics()
                    df = pd.DataFrame.from_dict(data, orient="index")
                    df = df.reset_index().rename(columns={"index": "Ticker"})
                graph_choice = st.selectbox("Choose Comparison Method: ", options=[None,"Scatter Plot", "Price-line curve"])
                if graph_choice:
                    match graph_choice:
                        #plotting a scatter graph
                        case "Scatter Plot":
                            x = st.selectbox("X", options= df.columns[1:])
                            y = st.selectbox("Y", options= df.columns[1:])
                            fig_scatter = px.scatter(df, x=x, y=y, color= "Ticker", size="EPS")
                            st.plotly_chart(fig_scatter)
                        case "Price-line curve":
                            start_date = st.date_input("Enter start date: ", value=today-timedelta(days=365), max_value=today)
                            end_date = st.date_input("Enter end date: ", value=today, max_value=today)
                            if check_date(start_date, end_date) == 1:
                                st.error("⚠️ Start date must be before end date.")
                            elif check_date(start_date, end_date) == 2:
                                st.warning("📅 Please select a range of at least 7 days.")
                            else:    
                                with st.spinner("🗃️ Getting Data"):
                                    data = yf.download(valid_tickers, start=start_date, end=end_date)
                                    data = data["Close"].reset_index()
                                    # Reset index to have Date as a column   
                                    # Convert to long format
                                    df = data.melt(id_vars="Date", var_name="Ticker", value_name="Price")
                                    # Plot line chart
                                    if not df.empty:
                                        fig = px.line(df, x="Date", y="Price", color="Ticker",
                                                    title="Stock Price Variation (Adj Close)")
                                        st.plotly_chart(fig)

def check_date(start, end) -> int:
    if (end - start).days < 0:
        return 1
    elif (end - start).days < 7:
        return 2
    else:
        return 0

def validate_single_ticker(ticker: str) -> bool:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history()
        if not hist.empty:
            return True
        return False
    except Exception:
        return False

def validate_ticker_list(tickers: list) -> list:
    valid = []
    for ticker in tickers:
        if validate_single_ticker(ticker):
            valid.append(ticker)
    return valid    

if __name__ == "__main__":
    main()
