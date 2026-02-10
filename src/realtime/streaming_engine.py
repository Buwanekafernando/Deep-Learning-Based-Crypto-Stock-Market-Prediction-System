import asyncio 
import numpy  as np

from src.data_ingestion.crypto_client import CryptoClient
from src.data_ingestion.cse_client import CSEClient
from src.features_engineering.technical_indicators import add_indicators
from src.inference.predictor import predict_price
from src.evaluation.metrics import evaluate
from src.rag.explainer import explain_prediction

crypto = CryptoClient()
cse  = CSEClient()

async def stream_market(websocket):
    while True:

        price_data = crypto.get.price("BTCUSDT")
        current_price = float(price_data["price"])

        #dummy indicator example

        indicators = {"RSI": 55}

        prediction = predict_price(current_price)

        metrices = evaluate(
            np.array([current_price]),
            np.array([prediction])
        )

        explantion = explain_prediction(
            prediction - current_price,
            indicators,
            news=[]
        )

        payload = {
            "symbol": "BTC",
            "price": current_price,
            "prediction": prediction,
            "metrics": metrics,
            "explanation": explanation
        }

        await websocket.send_text(json.dumps(payload))
        await asyncio.sleep(5)
        

 