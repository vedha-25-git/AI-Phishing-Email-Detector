import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
data = pd.read_csv("dataset/spam.csv")

# Convert text into numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data["message"])

# Labels
y = data["label"]

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("AI Model Trained Successfully!")