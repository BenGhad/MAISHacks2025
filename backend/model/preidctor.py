import joblib
import yfinance as yf
import model_trainer as gyatt

model = joblib.load('backend/model/model.joblib')


def predictAny(Return, Ma5, Ma20, Volume_Change ):
    return model.predict([[Return, Ma5, Ma20, Volume_Change]])


Spent =0
Profit =0

def start(startDate, endDate, tickers):
    for ticker in tickers:
        # Download da process
        Ydf = yf.download(ticker, start=startDate, end=endDate)
        Ydf.reset_index(inplace=True)  # Make date a collumn
        pdf = gyatt.process_dataframe(Ydf)

        # Edge case(no data):
        if pdf.empty:
            print(f"No data after processing for {ticker} in the given date range.")
            continue

        # X & Y test:
        X_test = pdf[['Return', 'MA5', 'MA20', 'Volume_Change']]
        y_test = pdf['Target']
        # If X_test is empty, we cannot call predict.
        if len(X_test) == 0:
            print(f"{ticker} has 0 valid rows after feature engineering.")
            continue

        y_predict = model.predict(X_test)