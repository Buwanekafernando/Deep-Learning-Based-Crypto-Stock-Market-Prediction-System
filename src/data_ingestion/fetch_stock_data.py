import os
import pandas as pd
import yfinance as yf
from cse_lk import CSEClient

YAHOO_SAVE_PATH = "data/raw/stocks/yahoo"
CSE_SAVE_PATH = "data/raw/stocks/cse"

os.makedirs(YAHOO_SAVE_PATH, exist_ok=True)
os.makedirs(CSE_SAVE_PATH, exist_ok=True)


def fetch_yahoo_stock(symbol="AAPL", start="2019-01-01", end="2024-12-31"):
    data = yf.download(symbol, start=start, end=end)
    file_path = f"{YAHOO_SAVE_PATH}/{symbol}.csv"
    data.to_csv(file_path)
    print(f"✅ Yahoo stock data saved: {file_path}")


def fetch_cse_company(symbol="LOLC.N0000"):
    client = CSEClient()
    company = client.get_company_info(symbol)

    company_data = {
        "symbol": symbol,
        "name": company.name,
        "last_traded_price": company.last_traded_price,
        "change": company.change,
        "change_percentage": company.change_percentage,
        "volume": company.volume,
        "turnover": company.turnover
    }

    df = pd.DataFrame([company_data])
    file_path = f"{CSE_SAVE_PATH}/{symbol}_snapshot.csv"
    df.to_csv(file_path, index=False)

    print(f"✅ CSE company snapshot saved: {file_path}")


def fetch_cse_market_overview():
    client = CSEClient()
    overview = client.get_market_overview()

    market_data = {
        "market_status": overview["status"].status,
        "aspi": overview["aspi"].value,
        "snp_sl20": overview["snp_sl20"].value,
        "date": overview["aspi"].date
    }

    df = pd.DataFrame([market_data])
    file_path = f"{CSE_SAVE_PATH}/market_overview.csv"
    df.to_csv(file_path, index=False)

    print(f"✅ CSE market overview saved: {file_path}")

def fetch_cse_top_gainers(limit=10):
    client = CSEClient()
    gainers = client.get_top_gainers()

    data = []
    for g in gainers[:limit]:
        data.append({
            "symbol": g.symbol,
            "price": g.price,
            "change": g.change,
            "change_percentage": g.change_percentage
        })

    df = pd.DataFrame(data)
    file_path = f"{CSE_SAVE_PATH}/top_gainers.csv"
    df.to_csv(file_path, index=False)

    print(f"✅ CSE top gainers saved: {file_path}")

if __name__ == "__main__":
    fetch_yahoo_stock("AAPL")
    fetch_cse_company("LOLC.N0000")
    fetch_cse_market_overview()
    fetch_cse_top_gainers()
