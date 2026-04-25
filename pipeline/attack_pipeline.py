import requests
import json

ATTACK_API = "https://strike-defender-v1.runasp.net/api/Attacks/generate_Atttacks_Static_Prompt"
MODEL_API = "http://127.0.0.1:8000/predict"

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

        if res.status_code == 200:
            result = res.json()
            prediction = result.get("prediction")
        else:
            prediction = None

    except Exception:
        prediction = None

    # ==============================
    # RAW: attacks / normal
    # ==============================
    record = {
        "id": attack_id,
        "payload": payload
    }

    # ==============================
    # Analysis record
    # ==============================
    analysis_record = {
        "id": attack_id,
        "payload": payload,
        "prediction": prediction,
        "true_label": prediction,  # مؤقت (until labeled dataset)
        "type": "attack" if prediction == 1 else "normal"
    }

    # ==============================
    # Split
    # ==============================
    if prediction == 1:
        real_attacks.append(record)
    elif prediction == 0:
        normal_attacks.append(record)

    analysis_attacks.append(analysis_record)

    print(f"[{attack_id}] -> {prediction}")

# ==============================
# Save RAW ATTACKS
# ==============================
with open("real_attacks.json", "w", encoding="utf-8") as f:
    json.dump(real_attacks, f, indent=4, ensure_ascii=False)

# ==============================
# Save RAW NORMAL
# ==============================
with open("normal_attacks.json", "w", encoding="utf-8") as f:
    json.dump(normal_attacks, f, indent=4, ensure_ascii=False)

# ==============================
# Save ANALYSIS (FULL DATASET)
# ==============================
with open("analysis_attacks.json", "w", encoding="utf-8") as f:
    json.dump(analysis_attacks, f, indent=4, ensure_ascii=False)

print("\nSaved all files ")