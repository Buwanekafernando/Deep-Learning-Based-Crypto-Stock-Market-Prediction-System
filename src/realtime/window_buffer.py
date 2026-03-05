import numpy as np
from collections import deque        # was 'collection' (missing 's') — fixed


class SlidingWindowBuffer:
    """
    Maintains a fixed-length sliding window of feature vectors for real-time inference.

    Returns windows as shape (1, window_size, n_features) to match model.predict() input.
    """

    def __init__(self, window_size: int = 60, n_features: int = 10):
        self.window_size = window_size
        self.n_features = n_features
        self.buffer = deque(maxlen=window_size)

    def add(self, feature_vector) -> None:
        """
        Append one feature vector (shape: (n_features,)) to the buffer.
        Oldest entry is automatically discarded when the buffer is full.
        """
        vec = np.asarray(feature_vector, dtype=np.float32)
        if vec.shape[0] != self.n_features:
            raise ValueError(
                f"Expected feature vector of length {self.n_features}, got {vec.shape[0]}."
            )
        self.buffer.append(vec)

    def is_ready(self) -> bool:
        """Return True only when the buffer contains exactly window_size vectors."""
        return len(self.buffer) == self.window_size

    def get_window(self) -> np.ndarray:
        """
        Return the current window as shape (1, window_size, n_features).
        Raises RuntimeError if called before the buffer is full.
        """
        if not self.is_ready():
            raise RuntimeError(
                f"Buffer not ready: {len(self.buffer)}/{self.window_size} steps collected."
            )
        return np.array(self.buffer).reshape(1, self.window_size, self.n_features)

    def reset(self) -> None:
        """Clear all buffered data."""
        self.buffer.clear()

    def __len__(self) -> int:
        return len(self.buffer)
