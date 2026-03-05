import numpy as np


def create_sequences(data: np.ndarray, window_size: int = 60) -> tuple:
    """
    Slice a 2-D scaled array into overlapping (X, y) sequence pairs.

    Parameters
    ----------
    data        : np.ndarray of shape (n_timesteps, n_features) — already scaled
    window_size : number of past timesteps used as model input

    Returns
    -------
    X : np.ndarray of shape (n_samples, window_size, n_features)
    y : np.ndarray of shape (n_samples, n_features)  — next timestep values
    """
    xs, ys = [], []
    for i in range(len(data) - window_size):
        xs.append(data[i : i + window_size])
        ys.append(data[i + window_size])
    return np.array(xs), np.array(ys)
