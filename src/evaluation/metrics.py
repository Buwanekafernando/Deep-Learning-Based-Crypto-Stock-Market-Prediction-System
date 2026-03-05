import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def evaluate_model(y_true, y_pred):
    """Return RMSE, MAE, and MAPE for the given true/predicted arrays."""
    return {
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAE": mean_absolute_error(y_true, y_pred),
        "MAPE": np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
    }


# Alias kept for backward compatibility with streaming_engine.py
evaluate = evaluate_model