import asyncio 
import numpy  as np
import json

from src.data_ingestion.crypto_client import CryptoClient
from src.data_ingestion.cse_client import CSEClient
from src.features_engineering.technical_indicators import add_indicators
from src.inference.predictor import predict_price
from src.evaluation.metrics import evaluate
from src.rag.explainer import explain_prediction
from src.realtime.window_buffer import SlidingWindowBuffer
from src.inference.predictor import RealTimePredictor

crypto = CryptoClient()
cse  = CSEClient()
buffer = SlidingWindowBuffer(window_size=60, n_features=10)
predictor = RealTimePredictor()



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


async def stream_market(websocket):
    while True:
        
        current_price = get_live_price_somehow()

        feature_vector = [
            current_price,
            current_price,
            current_price,
            current_price,
            1000,
            0, 0, 0, 0, 0
        ]

        buffer.add(feature_vector)

        if buffer.is_ready():
            window_data = buffer.get_window()
            prediction = predictor.predict(window_data)
            
            payload = {
                "price": current_price,
                "prediction": prediction
            }

            await websocket.send_text(json.dumps(payload))

        await asyncio.sleep(5)
