# Scikit Stock Bot

Scikit Stock Bot is a proof-of-concept stock screener built in 24 hours for [MAIS Hacks 2025](https://devpost.com/software/skibidi-sci-learn-stock-screener). The project trains a scikit-learn model using 40 years of historical stock data to predict whether a stock's price will increase the day after purchase.

---

## What It Does

- **Model Training:**  
  Trains a random forest classifier on historical stock data from 1980 to 2020.

- **Prediction:**  
  Given a stock ticker, the model predicts if buying today will result in a price increase tomorrow.

- **Simulation:**  
  Simulates stock market performance using historical data (via [yfinance](https://github.com/ranaroussi/yfinance)) to show potential profit when following the model's recommendations.

> **Note:** This project serves as a proof-of-concept. The algorithm is inspired by the greedy approach seen in [Leetcode 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
---

## Features

- **Prediction Model:**  
  Input stock ticker(s) to receive a classification on whether it is worth buying.

- **Market Simulation:**  
  Specify a set of stock tickers along with a start and end date to simulate market performance and view potential profits.

---

## Tech Stack

- **Backend:**  
  - Python with [Pandas](https://pandas.pydata.org/) for data manipulation.  
  - [scikit-learn](https://scikit-learn.org/) for model training and prediction.  
  - A little bit of MATLAB for visualization.

- **Frontend:**  
  - Pure HTML, CSS, and JavaScript with [FastAPI](https://fastapi.tiangolo.com/) as the backend framework.

---

## Future Work

The repo is **archived**. You can follow any continued progress [here](https://github.com/BenGhad/ScikitBot). Planned improvements include:
- Retraining the model on a larger dataset with enhanced feature selection.
- Incorporating NLTK for sentiment analysis.
- Developing a live portfolio dashboard for real-time market analysis.
- Reducing the models risk tolerance

---

## Instructions

1. **Generate the Model:**  
   Run the following command to train the model:
   ```bash
   python backend/model/model_trainer.py
2. **Start the application**
    Run the main application:
    ```bash
    python newMain.py
3. **Then, open your browser and navigate to http://127.0.0.1:8000/**