import numpy as np
from tensorflow.keras.models import load_model

def predict_next(model_path,X_input):
    #load the model and predict the next value 
    model = load_model(model_path)
    prediction = model.predict(X_input)
    return prediction