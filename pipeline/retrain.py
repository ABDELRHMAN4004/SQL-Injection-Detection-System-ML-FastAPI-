
import pandas as pd

# اقرأ الداتا القديمة
df = pd.read_csv("SQLiV3.csv", encoding="latin-1")

# اقرأ الهجمات الجديدة
with open("missed_attacks.txt", encoding="utf-8") as f:
    new_attacks = [line.strip() for line in f.readlines()]

# ضيفهم
new_df = pd.DataFrame({
    "Sentence": new_attacks,
    "Label": [1]*len(new_attacks)
})

df = pd.concat([df, new_df], ignore_index=True)

df.to_csv("SQLiV3_updated.csv", index=False)

print("Dataset updated ")