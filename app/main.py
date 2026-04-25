print("MAIN FILE LOADED")

from fastapi import FastAPI, HTTPException
from sklearn.metrics import confusion_matrix
from app.schemas import QueryRequest, PredictionResponse
from app.model_loader import load_model, predict_query
import logging
import json
import os

app = FastAPI(title="SQL Injection Detection API")

logging.basicConfig(level=logging.INFO)


model, vectorizer = load_model()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTACKS_FILE = os.path.join(BASE_DIR, "real_attacks.json")
ANALYSIS_FILE = os.path.join(BASE_DIR, "analysis_attacks.json")

# ==============================
# Root
# ==============================
@app.get("/")
def root():
    return {"status": "running"}


# ==============================
# Predict endpoint
# ==============================
@app.post("/predict", response_model=PredictionResponse)
def predict(req: QueryRequest):
    try:
        pred, prob = predict_query(req.query, model, vectorizer)

        label = "Attack" if pred == 1 else "Normal"

        logging.info(f"Query: {req.query} | Result: {label}")

        return {
            "query": req.query,
            "prediction": int(pred),
            "label": label,
            "confidence": float(prob)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# Get all attacks (RAW output)
# ==============================
@app.get("/attacks")
def get_attacks():
    try:
        if not os.path.exists(ATTACKS_FILE):
            return {
                "count": 0,
                "attacks": []
            }

        with open(ATTACKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "count": len(data),
            "attacks": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# Get attack by ID (RAW output)
# ==============================
@app.get("/attacks/{attack_id}")
def get_attack_by_id(attack_id: str):
    try:
        if not os.path.exists(ATTACKS_FILE):
            raise HTTPException(status_code=404, detail="File not found")

        with open(ATTACKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for attack in data:
            if str(attack["id"]) == str(attack_id):
                return attack

        raise HTTPException(status_code=404, detail="Not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# Export (RAW)
# ==============================
@app.get("/export/attacks")
def export_attacks():
    try:
        if not os.path.exists(ATTACKS_FILE):
            return []

        with open(ATTACKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
   

ANALYSIS_FILE = os.path.join(BASE_DIR, "analysis_attacks.json")


@app.get("/analysis")
def analysis():
    try:
        if not os.path.exists(ANALYSIS_FILE):
            return {
                "total_attacks": 0,
                "normal_attacks": 0,
                "attack_attacks": 0,
                "confusion_matrix": {
                    "TP": 0,
                    "TN": 0,
                    "FP": 0,
                    "FN": 0
                }
            }

        with open(ANALYSIS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        total = len(data)

        normal = sum(1 for x in data if x["type"] == "normal")
        attack = sum(1 for x in data if x["type"] == "attack")

        y_true = []
        y_pred = []

        for item in data:
            if item.get("true_label") is not None:
                y_true.append(item["true_label"])
                y_pred.append(item["prediction"])

        if len(y_true) > 0:
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        else:
            tn = fp = fn = tp = 0

        return {
            "total_attacks": total,
            "normal_attacks": normal,
            "attack_attacks": attack,
            "confusion_matrix": {
                "TP": int(tp),
                "TN": int(tn),
                "FP": int(fp),
                "FN": int(fn)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    