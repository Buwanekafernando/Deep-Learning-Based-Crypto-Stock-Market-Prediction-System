import numpy as np 
from tensorflow.keras.models import load_model

model - load_model("models_saved/lstm/lstm_feat_price_model.h5")

def predict_price(latest_price):
    X = np.array(latest_price).reshape(1,1,1)
    return float(model.predict(X)[0][0])

