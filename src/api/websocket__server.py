from fastapi import FastAPI, WebSocket
import asyncio
import json

from src.realtime.streaming_engine import stream_market


app = FastAPI()

clients = set()

@app.websocket("/ws/market")
async def market_ws(websocket:WebSocket):
    await websocket.accept()
    clients.add(websocket)

    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.remove(websocket)

async def market_ws(websocket: WebSocket):
    await websocket.accept()
    await stream_market(websocket)

    