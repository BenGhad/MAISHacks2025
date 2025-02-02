import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import yfinance as yf

def process_dataframe(dataframe):
    """
    processes dataframe with:
    Date Close Volume,
    then creates
      - Return
      - MA5, MA20
      - Volume_Change
      - Next_Return
      - Target
    """
    df = dataframe.copy()
    df.sort_values('Date', inplace=True)

    # Compute daily return from Close prices
    df['Return'] = df['Close'].pct_change(fill_method=None)
    df['Return'].fillna(0) #0% profit on day 0

    # Compute moving averages (5-day and 20-day)
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # Compute volume change
    df['Volume_Change'] = df['Volume'].pct_change(fill_method=None)
    df['Volume_Change'].fillna(0)

    # Create next-day return and target
    df['Next_Return'] = df['Return'].shift(-1)
    df['Next_Return'].fillna(0)

    # Skibidi Classification
    def label_target(r):
        if r > 0.01:
            return 1
        elif r < -0.01:
            return -1
        else:
            return 0

    df['Target'] = df['Next_Return'].apply(label_target)
    # accounting for the fact that kaggle has the hygiene of a CS major
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    return df

def process_file(file_path):
    """
      reads CSV -> dataframe. PROCESS!!!!
    """
    print(f"[INFO] reading {file_path}")
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=False)
    processed_df = process_dataframe(df)
    print(f"[INFO] Finished Processing {file_path} (Valid rows: {len(processed_df)}")
    return processed_df


# ---------------------
# 1) COMBINE ALL CSVs
# ---------------------
def combine_data(raw_folder):
    """
    Reads all CSV files in the folder, processes them, and concatenates into a single DataFrame.
    """
    all_dfs = []
    count = 0
    for file in os.listdir(raw_folder):
        if count == cap:
            break
        count += 1
        print(f"[INFO] Processing {file}")
        if file.lower().endswith(".csv"):
            file_path = os.path.join(raw_folder, file)
            processed_df = process_file(file_path)
            all_dfs.append(processed_df)

    # Concatenate all processed data
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Sort by date after concatenation
    combined_df.sort_values("Date", inplace=True)
    print(f"[INFO] Finished Combining {count} files")
    return combined_df




# ----------------------
# 2) MAIN SCRIPT
# ----------------------
if __name__ == "__main__":
    #Settings to compile:
    cap = int(input("How many files to train on? (More is better, but more intensive): "))


    #Training Phase:
    raw_folder = "data/raw"
    # Combine all CSV data into one DataFrame
    train_df = combine_data(raw_folder)

    # Prepare training data
    X_train = train_df[['Return', 'MA5', 'MA20', 'Volume_Change']]
    y_train = train_df['Target']
    print("[INFO] Training RandomForestClassifier model...")
    # Fit the random forest on the training set
    model = RandomForestClassifier(
        n_estimators=100, # Default
        max_depth=20, # Limited tree growth but less memory overload
        n_jobs=-1, # I paid for 100% of the CPU I'm going to use 100% of the CPU
        max_samples=0.7, #lowers RAM usage
        random_state=42 #the answer
    )

    model.fit(X_train, y_train)
    print("[INFO] Model training completed.")

    # Yfinance testing
    test_tickers = []
    results = {}
    start_date = "2024-01-01"
    end_date = "2025-01-01"


    for ticker in test_tickers:
        #Download da process
        print(f"[INFO] Downloading & testing data for ticker: {ticker}")
        Ydf = yf.download(ticker, start=start_date, end=end_date)
        Ydf.reset_index(inplace=True) # Make date a collumn
        pdf = process_dataframe(Ydf)

        #Edge case(no data):
        if pdf.empty:
            print(f"[WARNING]No data after processing for {ticker} in the given date range.")
            continue

        #X & Y test:
        X_test = pdf[['Return', 'MA5', 'MA20', 'Volume_Change']]
        y_test = pdf['Target']
        # If X_test is empty, we cannot call predict.
        if len(X_test) == 0:
            print(f"[WARNING]{ticker} has 0 valid rows after feature engineering.")
            continue
        print(f"[INFO] Running predictions for {ticker}...")
        y_predict = model.predict(X_test)
        acc = accuracy_score(y_test, y_predict)
        print(f"[RESULT]{ticker} Test Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_predict, digits=4))

    # Save the model
    joblib.dump(model, "model.joblib")
    print("[INFO]Model saved to model.joblib")
