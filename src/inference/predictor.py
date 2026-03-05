"""
Inference helpers for LSTM-based price prediction.

Column order after add_indicators():
  0:Open  1:High  2:Low  3:Close  4:Volume
  5:EMA_20  6:RSI_14  7:MACD  8:BB_high  9:BB_low
close_index = 3 (must stay in sync with technical_indicators.FEATURE_COLUMNS)
"""
import numpy as np
from tensorflow.keras.models import load_model
from src.inference.scaler_loader import load_scaler

# Close-price column index — must match FEATURE_COLUMNS order in technical_indicators.py
_CLOSE_INDEX = 3


class RealTimePredictor:
    """
    Load a trained LSTM model + its paired MinMaxScaler and run real-time inference.

    Parameters
    ----------
    model_path  : Path to the saved Keras model (.h5 or SavedModel directory).
    scaler_path : Path to the joblib-serialized MinMaxScaler.
    """

    def __init__(
        self,
        model_path: str = "models_saved/lstm/lstm_prod_model.h5",
        scaler_path: str = "models_saved/lstm/scaler.pkl",
    ):
        self.model = load_model(model_path)
        self.scaler = load_scaler(scaler_path)
        self.close_index = _CLOSE_INDEX

    def predict(self, window_data: np.ndarray) -> float:
        """
        Generate a single price prediction from a raw (unscaled) window.

        Parameters
        ----------
        window_data : np.ndarray of shape (1, window_size, n_features) — raw values

        Returns
        -------
        Predicted Close price in original price units (inverse-scaled).
        """
        # Scale the entire window using the pre-fitted scaler
        n_features = window_data.shape[2]
        flat = window_data.reshape(-1, n_features)           # (window_size, n_features)
        scaled_flat = self.scaler.transform(flat)
        scaled_window = scaled_flat.reshape(window_data.shape)  # (1, window_size, n_features)

        # Model outputs a single scaled value
        pred_scaled = self.model.predict(scaled_window, verbose=0)  # (1, 1) or (1, n_feat)

        # Inverse-transform: embed prediction back into a dummy row
        dummy = np.zeros((1, n_features))
        dummy[0, self.close_index] = float(pred_scaled.flat[0])
        inv = self.scaler.inverse_transform(dummy)
        return float(inv[0, self.close_index])

