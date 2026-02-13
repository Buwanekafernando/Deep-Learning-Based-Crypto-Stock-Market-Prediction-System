import joblib 

def load_scaler(path="models_saved/lstm/scaler.pkl"):
    return joblib.load(path)