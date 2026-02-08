def explain_prediction(price_change,indicators, news):
    explanation =[]

    if price_change > 0:
        explanation.append("Model predicts an upward trend.")
    else:
        explanation.append("Model predicts a downward trend.")

    #add technical indicators
    if indicators["RSI_14"] < 30:
        explanation.append("RSI indicates the stock is oversold.")
    elif indicators["RSI_14"] > 70:
        explanation.append("RSI indicates the stock is overbought.")
    
    if indicators["MACD"] > 0:
        explanation.append("MACD indicates a bullish trend.")
    else:
        explanation.append("MACD indicates a bearish trend.")
    
    if indicators["BB_high"] < indicators["Close"]:
        explanation.append("Stock is trading above the upper Bollinger Band.")
    elif indicators["BB_low"] > indicators["Close"]:
        explanation.append("Stock is trading below the lower Bollinger Band.")
    
    #add news
    top_news = news[:2]
    for article in top_news:
        explanation.append(f"Related news: {article['title']}")

    return " ".join(explanation)
