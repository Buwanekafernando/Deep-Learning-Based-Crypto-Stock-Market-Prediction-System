import pandas as pd
import ta


# Canonical feature order — must stay in sync with RealTimePredictor.close_index (index 3)
FEATURE_COLUMNS = [
    "Open", "High", "Low", "Close", "Volume",
    "EMA_20", "RSI_14", "MACD", "BB_high", "BB_low",
]


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute technical indicators and append them to `df`.

    Expected input columns: Open, High, Low, Close, Volume.
    Returns a new DataFrame with NaN rows dropped and index reset.

    Output columns (in order):
        Open, High, Low, Close, Volume, EMA_20, RSI_14, MACD, BB_high, BB_low
    """
    df = df.copy()

    df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
    df["RSI_14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd()

    bb = ta.volatility.BollingerBands(df["Close"])
    df["BB_high"] = bb.bollinger_hband()
    df["BB_low"] = bb.bollinger_lband()

    df = df.dropna().reset_index(drop=True)
    return df[FEATURE_COLUMNS]
