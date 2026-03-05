import os
import pandas as pd
import numpy as np
import joblib

from src.preprocessing.market_preprocessor import MarketPreprocessor
from src.models.deep_learning.lstm_model import build_lstm, train_lstm
from src.features.technical_indicators import FEATURE_COLUMNS

DATA_PATH = "data/raw/stocks/AAPL.csv"
MODEL_SAVE_PATH = "models_saved/lstm/lstm_prod_model.h5"
SCALER_SAVE_PATH = "models_saved/lstm/scaler.pkl"
CLOSE_INDEX = FEATURE_COLUMNS.index("Close")   # 3


def run_training():
    # load data (skip the first two rows which are metadata)
    df = pd.read_csv(DATA_PATH, skiprows=2)
    
    # name columns to standard names
    df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
    
    df["Date"] = pd.to_datetime(df["Date"])
    # sort data by date
    df = df.sort_values("Date").reset_index(drop=True)
    # select features
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    

    #add technical indicators
    preprocessor = MarketPreprocessor(window_size=60)
    df = preprocessor.add_technical_indicators(df)

    #scale the data - exclude Date
    features = [c for c in df.columns if c != "Date"]
    scaled_data = preprocessor.scale(df[features])
    X, y_full = preprocessor.create_sequences(scaled_data)
    y = y_full[:, CLOSE_INDEX]   # predict Close price only

    split = int(len(X) * 0.8)
    X_train, y_train = X[:split], y[:split]

    # input_shape = (window_size, n_features); output = 1 (Close price)
    model = build_lstm(input_shape=(X_train.shape[1], X_train.shape[2]))
    train_lstm(model, X_train, y_train)

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    model.save(MODEL_SAVE_PATH)
    joblib.dump(preprocessor.scaler, SCALER_SAVE_PATH)
    print(f"Model saved to '{MODEL_SAVE_PATH}', scaler to '{SCALER_SAVE_PATH}'")


if __name__ == "__main__":
    run_training()

