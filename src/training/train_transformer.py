from src.models.transformer_model import build_transformer_model
from src.training.sequence_builder import create_sequences
from src.preprocessing.preprocess import Preprocessor
import pandas as pd
import numpy as np
import joblib

WINDOW_SIZE = 60

df = pd.read_csv("data/processed/BTC_features.csv")

features = df.values

preprocessor = Preprocessor()
scaled = preprocessor.fit_transform(features)

X, y = create_sequences(scaled, WINDOW_SIZE)

model = build_transformer_model(
    seq_len=WINDOW_SIZE,
    n_features=X.shape[2]
)

model.fit(
    X, y,
    epochs=20,
    batch_size=32,
    validation_split=0.1
)

model.save("models_saved/transformer/transformer_model.h5")
joblib.dump(preprocessor.scaler,
            "models_saved/transformer/scaler.pkl")