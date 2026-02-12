import pandas as pd
import yfinance as yf
class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = yf.Ticker(self.ticker)
        self.info = self.data.info
        #Initializing the attributes
        self.price = None
        self.eps = None
        self.pe_ratio = None
        self.roe = None
        self.d_to_e = None
        self.annual_dividend = None
        self.payout_ratio = None
        self.profit_margin = None
        self.p_to_b_ratio = None
        self.fcf = None
        #Price
        if "currentPrice" in self.info:
            self.price = self.info.get("currentPrice", None)
        else:
            print("Key not found.")
        #EPS
        try:
            if "trailingEps" in self.info:
                self.eps = self.info.get('trailingEps', None)
        except Exception:
                print("Key not found. ")
        
        #P/E Ratio
        self.pe_ratio = (self.price/self.eps) if self.price and self.eps else None
        
        #ROE
        try:
            net_income = self.data.financials.loc['Net Income'].iloc[0]
            equity = self.data.balance_sheet.loc['Stockholders Equity'].iloc[0]
            self.roe = net_income / equity if equity else None
        except Exception:
            self.roe = None 
        #D/E
        try:
            if "debtToEquity" in self.info:
                self.d_to_e = self.info.get("debtToEquity", None)
        except Exception:
            print("Debt to Equity is not listed")

        #--DIVIDEND YIELD--
        divs = self.data.dividends
        if not divs.empty:
            annual_div = divs.loc[divs.index >(divs.index.max() - pd.DateOffset(years = 1))].sum()
            self.annual_dividend = annual_div
        else:
            self.annual_dividend = 0
        #--Payout Ratio--
        # Formula: Dividend Payout Ratio=Total Dividends / Net Income
        #Using the same divs.
        self.payout_ratio = self.info.get("payoutRatio", None)
        #--Profit Margin--
        # Formula: Net Profit Margin=Net Income / Total Revenue
        fin_data = self.data.financials
        if 'Total Revenue' in fin_data.index: 
            total_revenue = fin_data.loc['Total Revenue'].iloc[0]
            self.profit_margin = net_income / total_revenue
        else:
            total_revenue = 0
            self.profit_margin = 0
        
        # Price-to-Book--
        # Formula: P/B Ratio=Price per Share / Book Value per Share
        book_value = self.info.get('bookValue', None)
        self.p_to_b_ratio = self.price / book_value
        # Free Cash Flow
        self.fcf = self.data.cashflow.loc["Free Cash Flow"].iloc[0]

    def metrics(self):
        data =  {
            "price" : self.price,
            "EPS" : self.eps,
            "P/E_Ratio": self.pe_ratio,
            "ROE" : self.roe,
            "Debt_to_Equity" : self.d_to_e,
            "Annual_Dividend": self.annual_dividend,
            "Payout-Ratio": self.payout_ratio,
            "Profit-margin" :  self.profit_margin,
            "Price to book": self.p_to_b_ratio,
            "Free cash Flow":   self.fcf 
            }
        return data
    
    def get_history(self, start_date, end_date):
        return self.data.history(start= start_date, end=end_date).reset_index()
    
    def get_info(self):
        return self.data.info
    
    def financials(self):
        return self.data.financials.reset_index()
    
    def balance_sheet(self):
        return self.data.balance_sheet.reset_index()
    
    def cashflow(self):
        return self.data.cashflow.reset_index()
