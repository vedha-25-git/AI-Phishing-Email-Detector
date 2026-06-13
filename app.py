from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route('/', methods=['GET', 'POST'])
def home():

    result = ""
    risk = 0
    keyword_count = 0
    url_count = 0
    confidence = 0.0
    reasons = []

    if request.method == 'POST':

        email_text = request.form['email']

        # AI Prediction
        email_vector = vectorizer.transform([email_text])
        prediction = model.predict(email_vector)[0]

        try:
            confidence = round(
                model.predict_proba(email_vector).max() * 100,
                2
            )
        except:
            confidence = 100.0

        if prediction == "spam":
            result = "⚠️ Phishing / Spam Detected"
        else:
            result = "✅ Safe Email"

        # Keyword Detection
        phishing_keywords = [
            "urgent",
            "verify",
            "password",
            "bank",
            "click here",
            "login",
            "account suspended",
            "winner"
        ]

        for word in phishing_keywords:
            if word.lower() in email_text.lower():
                keyword_count += 1
                reasons.append(
                    f"Contains suspicious keyword: {word}"
                )

        # URL Detection
        urls = re.findall(r'https?://\S+', email_text)
        url_count = len(urls)

        if url_count > 0:
            reasons.append("Contains URL(s)")

        # Risk Score
        risk = min((keyword_count * 15) + (url_count * 20), 100)

    return render_template(
        'index.html',
        result=result,
        risk=risk,
        keyword_count=keyword_count,
        url_count=url_count,
        confidence=confidence,
        reasons=reasons
    )

if __name__ == '__main__':
    app.run(debug=True)