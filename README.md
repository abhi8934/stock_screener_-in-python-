# Stock Analyser

#### Video Demo: [Youtube Link](https://youtu.be/gYDg-QRrRPM)

### Description:
Stock Analyser is a program designed to help users analyze and visualize stock data in two different modes:

Project structure:
- project.py
  
- Share.py
- test_project.py
- Readme.md
- requirements.txt

### Features
- **1) Single Stock Mode**
  - The user inputs a single stock ticker.  
  - The program calculates and displays a list of financial metrics such as:
    - Price:- The stocks current trading price.
    
    - Earnings Per Share (EPS):- Gets "trailingEps" from [.info]() of [yfinance]().
    - P/E Ratio:- Calcultes P/E Ratio by dividing **price** and **eps** (Price/EPS) 

    - ROE:- ROE for a stock is calculated by fetch the financials of the company using [.financials]() and simply locating the **Net Income**, and in the balance sheet [.balance_sheet]() locating **Stockholders Equity**

    - Debt to Equity:- From the [.info]() of a ticker object fetch "debtToEquity".
  
    - Annual Dividends:- Calculated by adding the didvidends for a year fetched by [.dividends].

    - Payout Ratio:- Payout ratio is fetched as it is [.info] of the Stock object.

    - Profit Margin:- Calculated by dividing **Net Income** by **Total Revenue**.
      Total Revenue:- Fetched as it is for [.financials] of the Stock object.

    - Price to Book ratio:- Calculated by fetching the **bookValue** from [.info] of the Stock object and then dividing it by **price**.
    
    - Free Cash Flow:- Fetched as it is by from [.cashflow] of the stock object

- Results are shown in a **tabular format** for clarity. 
(pic) 
- The user can also view the **price graph over a period (default = 1 year)**. 
(pic) 
- Invalid tickers are explicitly handled, with the program clearly stating when a ticker is invalid. 
(Pic)

**2) Multi Stock Mode**
- The user inputs a list of **comma-separated stock tickers**.  
- The program generates:
  -**Price line charts** (for trend comparison)
  - **Scatter plots** (for visual relationship analysis)  
- Invalid tickers are automatically excluded from plots, ensuring accurate and clean visualizations.  

### How to Use:
- In the command line type `streamlit run project.py` to run the program.
- The user has an option to select modes
  - Single Stock
  - Double Stock
  ![image](/home/abhi294/c_code/final/images/image_modes.png)
- Provides both **tabular** 
  ![image](/home/abhi294/c_code/final/images/AAPL-metrics.png)
  and **graphical** outputs.(1year and 3years)
  ![image](/home/abhi294/c_code/final/images/AAPL-1y.png)
  ![image](/home/abhi294/c_code/final/images/AAPL-3y.png)
- Supports both single and multi-stock analysis.  
  * Multistock Mode with 10 valid tickers.
    ![image](/home/abhi294/c_code/final/images/Multi_stock_mode_with_tickers.png)
  * Line-curve in Multi-Stock mode.
    ![image](/home/abhi294/c_code/final/images/Multi_stock_mode_line_curve.png)
  * Scatter-curve in Multi-Stock mode.
    ![image](/home/abhi294/c_code/final/images/Multi_stock_scatter_options.png)

### Author - Abhimanyu Pandey
 


