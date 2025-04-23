import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Load training data
df = pd.read_csv("training_data.csv")

# Combine title and description
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")

# Build pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

# Train the model
model.fit(df["text"], df["category"])

# Save the model to disk
joblib.dump(model, "event_classifier.pkl")
print("✅ Model trained and saved as event_classifier.pkl")
