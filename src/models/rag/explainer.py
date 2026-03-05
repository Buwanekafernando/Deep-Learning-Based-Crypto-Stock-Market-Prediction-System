def explain_prediction(price_change: float, indicators: dict, news: list) -> str:
    """
    Build a human-readable explanation of a model prediction.

    Parameters
    ----------
    price_change : predicted_price - current_price (positive = bullish)
    indicators   : dict of indicator values (all keys are optional — safe defaults used)
    news         : list of news article dicts with a 'title' key

    Returns
    -------
    Single explanation string.
    """
    explanation = []

    # Direction signal
    if price_change > 0:
        explanation.append("Model predicts an upward trend.")
    else:
        explanation.append("Model predicts a downward trend.")

    # RSI
    rsi = indicators.get("RSI_14")
    if rsi is not None:
        if rsi < 30:
            explanation.append("RSI indicates the asset is oversold.")
        elif rsi > 70:
            explanation.append("RSI indicates the asset is overbought.")

    # MACD
    macd = indicators.get("MACD")
    if macd is not None:
        if macd > 0:
            explanation.append("MACD indicates a bullish trend.")
        else:
            explanation.append("MACD indicates a bearish trend.")

    # Bollinger Bands
    close = indicators.get("Close")
    bb_high = indicators.get("BB_high")
    bb_low = indicators.get("BB_low")
    if close is not None and bb_high is not None and bb_low is not None:
        if close > bb_high:
            explanation.append("Asset is trading above the upper Bollinger Band.")
        elif close < bb_low:
            explanation.append("Asset is trading below the lower Bollinger Band.")

    # Top news headlines
    for article in news[:2]:
        title = article.get("title", "")
        if title:
            explanation.append(f"Related news: {title}")

    return " ".join(explanation)

