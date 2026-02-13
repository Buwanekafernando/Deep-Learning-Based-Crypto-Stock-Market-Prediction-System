import numpy as np 
from tensorflow.keras.models import load_model
from src.inference.scaler_loader import load_scaler

model = load_model("models_saved/lstm/lstm_feat_price_model.h5")

def predict_price(latest_price):
    X = np.array(latest_price).reshape(1,1,1)
    return float(model.predict(X)[0][0])

class RealTimePredictor:
    #initialize the predictor with the model and scaler
    def __init__(self,
                 model_path="models_saved/lstm/lstm_feat_price_model.h5",
                 scaler_path="models_saved/lstm/scaler.pkl"):

        self.model = load_model(model_path)
        self.scaler = load_scaler(scaler_path)

        # index of Close price (same as training)
        self.close_index = 3
    
    def scale_features(self, feature_vector):
        scaled = self.scaler.transform([feature_vector])
        return scaled[0]
    
    def predict(self,window_data):
        
        scaled_window = self.scaler.transform(
            window_data.reshape(-1, window_data.shape[2])
        )

        pred_scaled = self.model.predict(scaled_window)

        # inverse scaling trick
        dummy = np.zeros((1, window_data.shape[2]))
        dummy[0, self.close_index] = pred_scaled[0][0]  

        inv = self.scaler.inverse_transform(dummy)
        return float(inv[0, self.close_index])  
