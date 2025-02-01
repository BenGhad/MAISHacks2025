import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def process_file(file_path):
    """
    Reads a CSV file and creates features and a target.
      - Daily percent return
      - 5-day and 20-day moving averages
      - Daily percent change in volume
      - A simple target: if tomorrow's return > 1% => 1 (buy), if < -1% => -1 (sell), else 0 (hold)
    """
    # Read CSV and parse dates (adjust dayfirst if needed)
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
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