import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def compare_models(y_true, lstm_pred, transformer_pred):

    results = {}

    results["LSTM_RMSE"] = np.sqrt(
        mean_squared_error(y_true, lstm_pred)
    )

    results["Transformer_RMSE"] = np.sqrt(
        mean_squared_error(y_true, transformer_pred)
    )

    results["LSTM_MAE"] = mean_absolute_error(y_true, lstm_pred)
    results["Transformer_MAE"] = mean_absolute_error(y_true, transformer_pred)

    return results