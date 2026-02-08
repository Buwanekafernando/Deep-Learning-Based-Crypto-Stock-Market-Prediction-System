import requests

BASE_URL = "https://cse-api-ghosthacker.herokuapp.com/api"

class CSEClient:

    def get_all_symbols(self):
        url = f"{BASE_URL}/stock/all"
        return requests.get(url).json()

    def get_market_status(self):
        url = f"{BASE_URL}/market/status"
        return requests.get(url).json()
    
    def get_stock_details(self,symbol):
        url = f"{BASE_URL}/stock/{symbol}"
        return requests.get(url).json()

    def get_trades(self, symbol):
        url = f"{BASE_URL}/trades/{symbol}"
        return requests.get(url).json()

