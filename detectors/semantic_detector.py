import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv("data/train.csv")

X = df["prompt"]
y = df["expected_policy"]

vectorizer = TfidfVectorizer()

X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()

model.fit(X_vec, y)

joblib.dump(model, "semantic_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model trained successfully")

model = joblib.load("semantic_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def semantic_score(text):

    vec = vectorizer.transform([text])

    prob = model.predict_proba(vec)[0][1]

    return float(prob)
