import joblib

model = joblib.load('model.joblib')

def predictAny(Return, Ma5, Ma20, Volume_Change ):
    return model.predict([[Return, Ma5, Ma20, Volume_Change]])


