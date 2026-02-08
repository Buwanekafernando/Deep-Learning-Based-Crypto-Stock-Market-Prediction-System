import requests

class CryptoClient:
    def get_price(self,symbol):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        params = {"symbol":symbol}
        return requests.get(url,params=params).json()
    
    def get_market_status(self):
        url = f"https://api.coingecko.com/api/v3/global"
        return requests.get(url).json()
    
    