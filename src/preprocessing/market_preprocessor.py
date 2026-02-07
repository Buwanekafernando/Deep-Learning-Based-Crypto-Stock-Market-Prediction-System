import numpy as np
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler


class MarketPreprocessor:
    # Initialize the preprocessor with a window size
    def __init__(self,window_size=60):
        self.window_size = window_size
        self.scaler = MinMaxScaler()
    
    # Add technical indicators to the dataframe
    def add_technical_indicators(self,df):
        df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
        df["RSI_14"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
        df["MACD"] = ta.trend.MACD(df["Close"]).macd()
        bb = ta.volatility.BollingerBands(df["Close"])
        df["BB_high"] = bb.bollinger_hband()
        df["BB_low"] = bb.bollinger_lband()

        return df.dropna().reset_index(drop=True) 

    # Scale the data
    def scale(self, data:pd.DataFrame) -> np.ndarray:
        return self.scaler.fit_transform(data)
    
    # Create sequences for the data
    def create_sequences(self,data:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
        # xs is the input sequence and ys is the output sequence
        xs,ys = [],[]
        # Loop through the data to create sequences
        for i in range(len(data) - self.window_size):
            x = data[i:i + self.window_size]
            y = data[i + self.window_size]
            xs.append(x)
            ys.append(y)
        return np.array(xs),np.array(ys)
        
