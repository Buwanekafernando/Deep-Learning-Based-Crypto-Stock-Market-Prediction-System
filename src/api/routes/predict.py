"""
REST endpoint for single-shot price prediction.

POST /predict
  Body: { "symbol": "BTCUSDT", "window": [[...], ...] }   (optional; uses live data if omitted)
  Returns: { "symbol": ..., "predicted_price": ..., "model": "LSTM" }
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import numpy as np

from src.inference.predictor import RealTimePredictor
from src.realtime.streaming_engine import _build_feature_vector
from src.realtime.window_buffer import SlidingWindowBuffer
from src.features.technical_indicators import FEATURE_COLUMNS

router = APIRouter(prefix="/predict", tags=["prediction"])

# Lazy-loaded singleton — only instantiated on first request
_predictor: Optional[RealTimePredictor] = None

_N_FEATURES = len(FEATURE_COLUMNS)
_WINDOW_SIZE = 60


def _get_predictor() -> RealTimePredictor:
    global _predictor
    if _predictor is None:
        _predictor = RealTimePredictor()
    return _predictor


class PredictRequest(BaseModel):
    symbol: str = "BTCUSDT"
    window: Optional[List[List[float]]] = None   # shape: (window_size, n_features)


class PredictResponse(BaseModel):
    symbol: str
    predicted_price: float
    model: str = "LSTM"


@router.post("/", response_model=PredictResponse)
def predict(req: PredictRequest):
    """
    Run LSTM inference.
    - If `window` is provided, use it directly (must be window_size × n_features).
    - If omitted, fetch the latest live OHLCV from Binance and build the window automatically.
    """
    predictor = _get_predictor()

    if req.window is not None:
        arr = np.array(req.window, dtype=np.float32)
        if arr.shape != (_WINDOW_SIZE, _N_FEATURES):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"window must have shape ({_WINDOW_SIZE}, {_N_FEATURES}), "
                    f"got {arr.shape}."
                ),
            )
        window_data = arr[np.newaxis, ...]   # (1, 60, 10)
    else:
        # Build a live window by fetching the latest OHLCV candles
        buf = SlidingWindowBuffer(window_size=_WINDOW_SIZE, n_features=_N_FEATURES)
        _, fv = _build_feature_vector(req.symbol)
        # Seed the buffer with the single live row (repeated — only for REST demo)
        for _ in range(_WINDOW_SIZE):
            buf.add(fv)
        window_data = buf.get_window()   # (1, 60, 10)

    predicted_price = predictor.predict(window_data)
    return PredictResponse(symbol=req.symbol, predicted_price=predicted_price)
