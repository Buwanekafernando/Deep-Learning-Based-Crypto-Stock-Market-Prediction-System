import yfinance as yf
import os

SAVE_PATH = "data/raw/crypto"

def fetch_crypto(symbol="BTC-USD", start="2019-01-01", end="2024-12-31"):
    os.makedirs(SAVE_PATH, exist_ok=True)

    data = yf.download(symbol, start=start, end=end)
    file_path = f"{SAVE_PATH}/{symbol}.csv"
    data.to_csv(file_path)

    print(f" Crypto data saved to {file_path}")

if __name__ == "__main__":
    fetch_crypto()
