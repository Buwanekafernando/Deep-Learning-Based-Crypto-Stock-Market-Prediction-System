from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import logging

from src.realtime.streaming_engine import stream_market

logger = logging.getLogger(__name__)

app = FastAPI(title="Crypto Market Prediction API")


@app.websocket("/market")
async def market_ws(websocket: WebSocket):
    """
    WebSocket endpoint for live market data and predictions.
    Connect with: ws://localhost:8000/ws/market
    """
    await websocket.accept()
    logger.info("WebSocket client connected: %s", websocket.client)
    try:
        await stream_market(websocket)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected: %s", websocket.client)
    except Exception as exc:
        logger.error("Unhandled WebSocket error: %s", exc)
        await websocket.close(code=1011)
