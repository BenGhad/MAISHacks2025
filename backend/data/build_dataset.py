#Builds the dataset & processes it
# !/usr/bin/env python3
import os
import json
import datetime
import pandas as pd

from backend.utils import config_manager
from backend import fmp_api


def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def save_raw_data(ticker, raw_data, raw_dir):
    filename = f"{ticker}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(raw_dir, filename)
    with open(file_path, "w") as f:
        json.dump(raw_data, f, indent=4)
    print(f"Raw data for {ticker} saved to: {file_path}")
    return file_path


def save_processed_data(df, ticker, processed_dir):
    filename = f"{ticker}_processed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(processed_dir, filename)
    df.to_csv(file_path, index=False)
    print(f"Processed data for {ticker} saved to: {file_path}")
    return file_path


def main():
    # Load configuration settings from config.yaml
    config = config_manager.load_config()
    api_key = config.get("api_key")
    if not api_key:
        raise ValueError("API key not found in configuration. Please check your config.yaml.")

    # Define Tickers
    ticker = "AAPL"  # To-Do: Make a list of like 500 ticker
    interval = "5min"

    # Define date range, 2-5 years for bear bull
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=730)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    # Directories for storing data
    raw_dir = os.path.join("data", "raw")
    processed_dir = os.path.join("data", "processed")
    ensure_directory(raw_dir)
    ensure_directory(processed_dir)

    # Fetch raw intraday data from FMP
    try:
        print(f"Fetching {interval} data for {ticker} from {start_date} to {end_date}...")
        raw_data = fmp_api.get_intraday_data(ticker, interval, start_date, end_date, api_key=api_key)
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return

    # Save raw data to disk
    raw_file_path = save_raw_data(ticker, raw_data, raw_dir)

    # Preprocess the raw data (assuming the function returns a Pandas DataFrame)
    try:
        print("Preprocessing raw data...")
        df_processed = None # data_preprocessor.preprocess_data(raw_data)
    except Exception as e:
        print(f"Error during data preprocessing: {e}")
        return

    # Save the processed data to disk
    processed_file_path = save_processed_data(df_processed, ticker, processed_dir)

    print("Dataset building complete.")


if __name__ == "__main__":
    main()
