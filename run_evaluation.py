import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

from app.main import analyze
from app.main import AnalyzeRequest


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/train.csv")


y_true = []
y_pred = []


# -----------------------------
# Run evaluation loop
# -----------------------------
for _, row in df.iterrows():

    text = row["prompt"]
    expected = row["expected_policy"]

    # Call your FastAPI logic directly
    result = analyze(AnalyzeRequest(text=text))

    predicted = result["decision"]

    y_true.append(expected)
    y_pred.append(predicted)


# -----------------------------
# Classification Report
# -----------------------------
print("\n📊 CLASSIFICATION REPORT\n")
print(classification_report(y_true, y_pred))


# -----------------------------
# Confusion Matrix
# -----------------------------
print("\n📊 CONFUSION MATRIX\n")
print(confusion_matrix(y_true, y_pred))


# -----------------------------
# Extra Metrics (Manual counts)
# -----------------------------

tp_block = sum((yt == "BLOCK" and yp == "BLOCK") for yt, yp in zip(y_true, y_pred))
fp_block = sum((yt != "BLOCK" and yp == "BLOCK") for yt, yp in zip(y_true, y_pred))
fn_block = sum((yt == "BLOCK" and yp != "BLOCK") for yt, yp in zip(y_true, y_pred))

accuracy = sum(yt == yp for yt, yp in zip(y_true, y_pred)) / len(y_true)

precision = tp_block / (tp_block + fp_block + 1e-9)
recall = tp_block / (tp_block + fn_block + 1e-9)
f1 = 2 * (precision * recall) / (precision + recall + 1e-9)


print("\n📌 CUSTOM METRICS (BLOCK CLASS ONLY)")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

print("\nFalse Positives:", fp_block)
print("False Negatives:", fn_block)
