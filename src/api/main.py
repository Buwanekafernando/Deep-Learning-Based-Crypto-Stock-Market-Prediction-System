"""
FastAPI application entry point.

Run with:
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
"""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.websocket__server import router as ws_router           # WebSocket route
from src.api.routes.predict import router as predict_router     # REST predict route

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Deep Learning Market Prediction API",
    description=(
        "Real-time crypto and stock price prediction using LSTM and Transformer models. "
        "WebSocket: /ws/market | REST: /predict"
    ),
    version="1.0.0",
)

# Allow the React dashboard (localhost:3000) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-routers
app.include_router(predict_router)
app.include_router(ws_router, prefix="/ws")


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "Market Prediction API is running."}
