
# python 3.13.1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer


file = pd.read_csv('SQLiV3.csv')

file = file[file["Label"].isin([0,1])]
file.dropna(subset=['Sentence'], inplace=True)
file.dropna(subset=['Label'], inplace=True)

# تنظيف
file["Sentence"] = file["Sentence"].astype(str)
file = file[file["Sentence"].str.strip() != ""]

# 🔥 هنا بقى الصح
features = file["Sentence"]
labels = file["Label"]

print("Number of samples:", len(features))

print("Shape:", file.shape)

print("\nSample data:")
print(file["Sentence"].head(10))

print("\nLengths:")
print(file["Sentence"].apply(len).describe())

print("\nUnique values:")
print(file["Sentence"].unique()[:10])

# vectorizer

vector = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2,5)
)

features_vector = vector.fit_transform(features)



x_train,x_test,y_train,y_test=train_test_split(features_vector,labels,test_size=0.2,random_state=42)

from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(x_train, y_train)

rf_predictions = rf_model.predict(x_test)

accuracy_score(y_test, rf_predictions)
print("Random Forest Accuracy:", accuracy_score(y_test, rf_predictions))


cm_rf = confusion_matrix(y_test, rf_predictions)
plt.figure()
plt.imshow(cm_rf)
plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.xticks(np.arange(2))
plt.yticks(np.arange(2))
for i in range(cm_rf.shape[0]):
    for j in range(cm_rf.shape[1]):
        plt.text(j, i, cm_rf[i, j], ha="center", va="center")
plt.show()  
