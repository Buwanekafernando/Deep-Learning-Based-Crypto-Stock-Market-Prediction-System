import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_lstm(input_shape):
    """
    Builds and compiles an LSTM model.
    """
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=25),
        Dense(units=1),               # Predict Close price only
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm(model, X_train, y_train, epochs=10, batch_size=32):
    """
    Trains the LSTM model.
    """
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
