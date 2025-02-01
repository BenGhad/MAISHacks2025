import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def process_file(file_path):
    """
    Reads a CSV file and creates features and a target.
      - Daily percent return
      - 5-day and 20-day moving averages
      - Daily percent change in volume
      - A simple target: if tomorrow's return > 1% => 1 (buy), if < -1% => -1 (sell), else 0 (hold)
    """
    # Read CSV and parse dates (adjust dayfirst if needed)
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=False)
    df.sort_values('Date', inplace=True)

    # Compute daily return from Close prices
    df['Return'] = df['Close'].pct_change()

    # Compute moving averages (5-day and 20-day)
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # Compute volume change
    df['Volume_Change'] = df['Volume'].pct_change()

    # Create target based on next day's return (shift -1)
    df['Next_Return'] = df['Return'].shift(-1)

    def label_target(r):
        if r > 0.01:  # if next day gain > 1%
            return 1
        elif r < -0.01:  # if next day loss > 1%
            return -1
        else:
            return 0

    df['Target'] = df['Next_Return'].apply(label_target)

    # Remove rows with NaN values (from rolling calculations and shifting)
    df.dropna(inplace=True)
    return df


mod = RandomForestClassifier()

# Path to the folder containing CSV files
raw_folder = "data/raw"

# List all CSV files in the folder
csv_files = os.listdir(raw_folder)

# Loop through each CSV file and process it
for file in csv_files:
    # Define X (features) and Y (target)
    file_path = os.path.join(raw_folder, file)
    processed_df = process_file(file_path)
    X = processed_df[['Return', 'MA5', 'MA20', 'Volume_Change']]
    Y = processed_df['Target']
    mod.fit(X, Y)


joblib.dump(mod, 'backend/model/model.joblib')



