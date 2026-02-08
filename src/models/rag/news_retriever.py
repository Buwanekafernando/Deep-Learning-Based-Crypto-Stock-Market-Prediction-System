import requests

NEWS_API_KEY = "YOUR_NEWS_API_KEY"

def get_market_news(query="Stock market"):
    url = "https://newsapi.org/v2/everything"
    #add parameters to the request
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apikey": NEWS_API_KEY
    }
    return requests.get(url,params=params).json()["articles"]

