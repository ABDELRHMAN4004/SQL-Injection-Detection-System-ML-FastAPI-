import requests
import json
import os

ATTACK_API = "https://strike-defender-v1.runasp.net/api/Attacks/generate_Atttacks_Static_Prompt"
MODEL_API = "http://127.0.0.1:8000/predict"

# ==============================
# FIX: write INSIDE app folder
# ==============================
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "app")
BASE_DIR = os.path.abspath(BASE_DIR)

REAL_ATTACKS_FILE = os.path.join(BASE_DIR, "real_attacks.json")
NORMAL_ATTACKS_FILE = os.path.join(BASE_DIR, "normal_attacks.json")
ANALYSIS_FILE = os.path.join(BASE_DIR, "analysis_attacks.json")


# ==============================
# Fetch attacks
# ==============================
response = requests.post(ATTACK_API)

print("Status Code:", response.status_code)

if response.status_code != 200:
    print("Error:", response.text)
    exit()

data = response.json()

if not isinstance(data, list):
    print("Invalid format")
    exit()

# ==============================
# Outputs
# ==============================
real_attacks = []
normal_attacks = []
analysis_attacks = []

print("\n=== Classification Started ===\n")

for item in data:
    attack_id = item.get("id")
    payload = item.get("payload")

    if not payload:
        continue

    try:
        res = requests.post(
            MODEL_API,
            json={"query": payload}
        )

        prediction = res.json().get("prediction") if res.status_code == 200 else None

    except Exception:
        prediction = None

    record = {
        "id": attack_id,
        "payload": payload
    }

    analysis_record = {
        "id": attack_id,
        "payload": payload,
        "prediction": prediction,
        "true_label": prediction,  # unchanged as requested
        "type": "attack" if prediction == 1 else "normal"
    }

    if prediction == 1:
        real_attacks.append(record)
    elif prediction == 0:
        normal_attacks.append(record)

    analysis_attacks.append(analysis_record)

    print(f"[{attack_id}] -> {prediction}")

# ==============================
# SAVE FILES (NOW SAME FOLDER AS API)
# ==============================
with open(REAL_ATTACKS_FILE, "w", encoding="utf-8") as f:
    json.dump(real_attacks, f, indent=4, ensure_ascii=False)

with open(NORMAL_ATTACKS_FILE, "w", encoding="utf-8") as f:
    json.dump(normal_attacks, f, indent=4, ensure_ascii=False)

with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
    json.dump(analysis_attacks, f, indent=4, ensure_ascii=False)

print("\nSaved all files")