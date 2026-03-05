"""
Transformer training script.

Usage (from project root):
    python -m src.training.train_transformer
"""
import os
import pandas as pd
import numpy as np
import joblib

from src.models.transformer_model import build_transformer_model
from src.preprocessing.market_preprocessor import MarketPreprocessor
from src.features.technical_indicators import FEATURE_COLUMNS

# ── Config ──────────────────────────────────────────────────────────────────
DATA_PATH = "data/processed/BTC_features.csv"
SAVE_DIR = "models_saved/transformer"
WINDOW_SIZE = 60
CLOSE_INDEX = FEATURE_COLUMNS.index("Close")   # 3
# ────────────────────────────────────────────────────────────────────────────

df = pd.read_csv(DATA_PATH)

# Ensure only the canonical feature columns are used (in the right order)
df = df[FEATURE_COLUMNS].dropna().reset_index(drop=True)
features = df.values   # (n_rows, n_features) as float64

preprocessor = MarketPreprocessor(window_size=WINDOW_SIZE)
scaled = preprocessor.scale(df)   # fit + transform; shape (n_rows, n_features)

X, y_full = preprocessor.create_sequences(scaled)
y = y_full[:, CLOSE_INDEX]   # predict Close only  →  shape (n_samples,)

model = build_transformer_model(
    seq_len=WINDOW_SIZE,
    n_features=X.shape[2],
)

model.fit(
    X, y,
    epochs=20,
    batch_size=32,
    validation_split=0.1,
)

os.makedirs(SAVE_DIR, exist_ok=True)
model.save(os.path.join(SAVE_DIR, "transformer_model.h5"))
joblib.dump(preprocessor.scaler, os.path.join(SAVE_DIR, "scaler.pkl"))
print(f"Transformer model and scaler saved to '{SAVE_DIR}/'")
