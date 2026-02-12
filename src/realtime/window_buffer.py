import numpy as np 
from collection import deque

class SlidingWindowBuffer:
    def __init__(self, window_size=60, n_features=10):
        self.window_size = window_size
        self.n_features = n_features
        self.buffer = deque(maxlen=window_size)

    def add(self, feature_vector):
        """
        feature_vector: array-like shape (n_features,)
        """
        self.buffer.append(feature_vector)

    def is_ready(self):
        return len(self.buffer) == self.window_size

    def get_window(self):
        return np.array(self.buffer).reshape(1, self.window_size, self.n_features)