import os
import joblib
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import backend.model.model_trainer as gyatt
from backend.model.model_trainer import process_dataframe
import io
import base64

# Load the pre-trained model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model.joblib')

model = joblib.load(model_path)
print("model loaded")

def predictNext(ticker):
    df = yf.download(ticker, period="3mo")
    if (df.empty):
        return f"{ticker}: No data available"
    df.reset_index(inplace=True)
    processed_df = process_dataframe(df)
    if processed_df.empty:
        return f"{ticker}: Not enough data available"

    ytd = processed_df.iloc[-1]
    ret = ytd['Return']
    ma5 = ytd['MA5']
    ma20 = ytd['MA20']
    vol_change = ytd['Volume_Change']

    features = pd.DataFrame([[ret, ma5, ma20, vol_change]],
                            columns=['Return', 'MA5', 'MA20', 'Volume_Change'])
    prediction = model.predict(features)[0]

    if prediction > 0:
        decision = "Yes"
    elif prediction < 0:
        decision = "No"
    else:
        decision = "YiHRT"
    return f"{ticker}: {decision}"

def plotGraph(ticker):
    ticker_data = yf.Ticker(ticker)
    historical_data = ticker_data.history(period="1y")

    # Plot the closing prices
    plt.figure(figsize=(10, 6))
    plt.plot(historical_data.index, historical_data['Close'], label=f'{ticker} Close Price', color='blue')

    # Add title and labels
    plt.title(f'{ticker} Stock Price (Last 1 Year)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img


def predictAny(ret, ma5, ma20, vol_change):
    # Create a DataFrame
    features = pd.DataFrame([[ret, ma5, ma20, vol_change]],
                            columns=['Return', 'MA5', 'MA20', 'Volume_Change'])
    prediction = model.predict(features)
    return prediction[0]


def start(startDate, endDate, tickers):
    """
    Simulate trades for each ticker from startDate to endDate using daily data.

    Rules/Alg:
      1) If already holding a ticker:
         a) If model prediction is +1 ("positive"), buy more shares proportional
            to the daily percent gain.
            Example: If daily gain is +20%, buy 20% more shares.
         b) If model prediction is -1 or 0 ("negative" or "neutral"), sell all shares.

      2) If NOT holding a ticker:
         a) If prediction is +1, buy $1000 worth of shares.
         b) If prediction is -1 or 0, do nothing.

    At the end of the period, sell any remaining shares (settle all positions).
    Returns final Profit.
    """

    expenses = 0.0 # Total money spent(Assume profit cannot be traded for simplicity)
    Profit = 0.0 # Running cash balance
    portfolio = {}

    # Go through each ticker individually
    for ticker in tickers:
        # Download data from yfinance
        df = yf.download(ticker, start=startDate, end=endDate)
        if df.empty:
            print(f"No data for {ticker} in the specified range.")
            continue

        df.reset_index(inplace=True)  # Convert the 'Date' index to a column
        # Process using the same transformations used in training
        pdf = gyatt.process_dataframe(df)
        if pdf.empty:
            print(f"No valid rows after processing {ticker} within date range.")
            continue

        # Sort by date just in case
        pdf.sort_values("Date", inplace=True)

        # We will iterate day by day in chronological order
        # 'Close' to track price, 'Return' to track daily returns, etc.
        # Keep track of the previous day's Close to calculate daily percent gain
        # for the "buy more" logic.
        prev_close = None

        # Ensure we have a key in the portfolio dictionary
        # or initialize with 0 shares if not present
        if ticker not in portfolio:
            portfolio[ticker] = 0.0

        for i, row in pdf.iterrows():
            current_close = float(row['Close'].iloc[0])
            # Model input features
            ret = float(row['Return'].iloc[0])
            ma5 = float(row['MA5'].iloc[0])
            ma20 = float(row['MA20'].iloc[0])
            vol_change = float(row['Volume_Change'].iloc[0])

            # Get prediction from the model
            prediction = predictAny(ret, ma5, ma20, vol_change)
            # prediction will be 1, 0, or -1

            # If we already hold shares of this ticker...
            if portfolio[ticker] > 0:
                if prediction >= 0:
                    # Buy more shares proportional to daily percent gain
                    # We need the daily percent gain from the last close to today's close:
                    if prev_close is not None and prev_close > 0:
                        daily_gain_pct = (current_close - prev_close) / prev_close
                        if daily_gain_pct > 0:
                            # Buy that % more shares
                            shares_to_buy = portfolio[ticker] * daily_gain_pct
                            cost = shares_to_buy * current_close
                            expenses += cost
                            # Increase position
                            portfolio[ticker] += shares_to_buy
                else:
                    # prediction is bad, sell everything
                    shares_held = portfolio[ticker]
                    proceeds = shares_held * current_close
                    # Add to Profit
                    Profit += proceeds
                    # Reset holding
                    portfolio[ticker] = 0.0

            # If we are NOT holding shares
            else:
                if prediction >= 0:
                    # Buy $1000 worth
                    shares_to_buy = 1000.0 / current_close # In case we refactor for growth
                    expenses += 1000.0
                    portfolio[ticker] = shares_to_buy
                # If prediction == 0 or -1, do nothing
                else:
                    pass

            # Update prev_close for next iteration
            prev_close = current_close

        # After the last day in the range, if still holding, sell everything
        if portfolio[ticker] > 0:
            last_close = float(pdf.iloc[-1]['Close'].iloc[0])
            shares_held = portfolio[ticker]
            proceeds = shares_held * last_close
            Profit += proceeds
            portfolio[ticker] = 0.0

    print(f"Final Cash Balance: {Profit:.2f}")
    print(f"Total Expenses (Money Invested): {expenses:.2f}")
    if(expenses != 0):
        pctProfit = (Profit / expenses) * 100
        print(f"Percent Profit: {pctProfit:.2f}%")
        return "Profit: " + str(round(pctProfit, 2)) + " -> " + str(round(pctProfit, 2)) + "% profit"
    else:
        return "No trades were made "


# Example usage:
if __name__ == "__main__":
    my_tickers = ["AAPL", "MSFT", "AMZN", "DELL", "GOOG", "WIX"]
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    # Run the simulation
    final_profit = start(start_date, end_date, my_tickers)
    print(f"Simulation completed. Final Profit: {final_profit:.2f}")
