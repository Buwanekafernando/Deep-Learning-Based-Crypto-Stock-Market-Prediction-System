import requests

# Binance public REST API — no API key required for read-only ticker data
_BINANCE_BASE = "https://api.binance.com/api/v3"


class CryptoClient:

    def get_price(self, symbol: str = "BTCUSDT") -> dict:
        """Return the latest price for `symbol` as {'symbol': ..., 'price': '...'}."""
        url = f"{_BINANCE_BASE}/ticker/price"
        response = requests.get(url, params={"symbol": symbol}, timeout=10)
        response.raise_for_status()
        return response.json()  # {"symbol": "BTCUSDT", "price": "67432.00"}

    def get_ohlcv(self, symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 200) -> list:
        """
        Fetch OHLCV klines from Binance.
        Returns a list of rows:
          [open_time, open, high, low, close, volume, ...]
        """
        url = f"{_BINANCE_BASE}/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_market_status(self) -> dict:
        """Return Binance system status: {'status': 0, 'msg': 'normal'}."""
        url = f"{_BINANCE_BASE}/system/status"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
