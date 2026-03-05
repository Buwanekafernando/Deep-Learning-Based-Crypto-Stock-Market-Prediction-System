"""
Real-time streaming engine.

Fetches live OHLCV data from Binance, computes technical indicators, maintains a
sliding-window buffer, generates model predictions, and pushes results over WebSocket.
"""
import asyncio
import json
import logging

import numpy as np
import pandas as pd

from src.data_ingestion.crypto_client import CryptoClient
from src.data_ingestion.cse_client import CSEClient
from src.features.technical_indicators import add_indicators, FEATURE_COLUMNS
from src.evaluation.metrics import evaluate_model
from src.models.rag.explainer import explain_prediction
from src.realtime.window_buffer import SlidingWindowBuffer
from src.inference.predictor import RealTimePredictor

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singletons — instantiated once at module load, reused per WebSocket frame
# ---------------------------------------------------------------------------
_N_FEATURES = len(FEATURE_COLUMNS)   # 10
_WINDOW_SIZE = 60

crypto = CryptoClient()
cse = CSEClient()
buffer = SlidingWindowBuffer(window_size=_WINDOW_SIZE, n_features=_N_FEATURES)
predictor = RealTimePredictor()


def _build_feature_vector(symbol: str = "BTCUSDT") -> tuple[float, list]:
    """
    Fetch the latest OHLCV klines from Binance, compute indicators, and return
    (current_close_price, feature_vector_of_length_N_FEATURES).
    """
    raw = crypto.get_ohlcv(symbol=symbol, interval="1m", limit=100)
    # Each kline: [open_time, open, high, low, close, volume, ...]
    df = pd.DataFrame(raw, columns=[
        "open_time", "Open", "High", "Low", "Close", "Volume",
        "close_time", "qav", "num_trades", "tbbav", "tbqav", "ignore",
    ])
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = df[col].astype(float)

    df = add_indicators(df)   # drops NaN rows, returns only FEATURE_COLUMNS

    if df.empty:
        raise ValueError("Not enough OHLCV data to compute indicators.")

    # Use the last row as the live feature vector
    current_close = float(df["Close"].iloc[-1])
    feature_vector = df[FEATURE_COLUMNS].iloc[-1].tolist()
    return current_close, feature_vector


async def stream_market(websocket) -> None:
    """
    Main WebSocket streaming loop.

    Every 5 seconds:
      1. Fetch live OHLCV + compute indicators
      2. Push the feature vector into the sliding-window buffer
      3. Once the buffer is full (60 steps), run model inference
      4. Compute evaluation metrics and generate an explanation
      5. Send a JSON payload to the connected client
    """
    while True:
        try:
            current_price, feature_vector = _build_feature_vector("BTCUSDT")
            buffer.add(feature_vector)

            indicators = {
                "RSI_14": feature_vector[FEATURE_COLUMNS.index("RSI_14")],
                "MACD":   feature_vector[FEATURE_COLUMNS.index("MACD")],
                "BB_high":feature_vector[FEATURE_COLUMNS.index("BB_high")],
                "BB_low": feature_vector[FEATURE_COLUMNS.index("BB_low")],
                "Close":  current_price,
            }

            payload: dict = {
                "symbol": "BTCUSDT",
                "price": current_price,
                "prediction": None,
                "metrics": {},
                "explanation": "Collecting data…",
                "buffer_fill": f"{len(buffer)}/{_WINDOW_SIZE}",
            }

            if buffer.is_ready():
                window_data = buffer.get_window()           # (1, 60, 10)
                prediction = predictor.predict(window_data)

                metrics = evaluate_model(
                    np.array([current_price]),
                    np.array([prediction]),
                )
                explanation = explain_prediction(
                    prediction - current_price,
                    indicators,
                    news=[],
                )

                payload["prediction"] = prediction
                payload["metrics"] = metrics
                payload["explanation"] = explanation

            await websocket.send_text(json.dumps(payload))

        except Exception as exc:
            logger.error("Streaming error: %s", exc)
            # Send error info to client rather than silently dying
            await websocket.send_text(json.dumps({"error": str(exc)}))

        await asyncio.sleep(5)
