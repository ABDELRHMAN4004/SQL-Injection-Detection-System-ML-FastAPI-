import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "model", "sqli_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")


def load_model():
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer


def predict_query(query: str, model, vectorizer):
    vec = vectorizer.transform([query])
    prob = model.predict_proba(vec)[0][1]
    pred = int(prob > 0.4)

    return pred, prob