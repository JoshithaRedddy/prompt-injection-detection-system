import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class MLPromptInjectionDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
        self.model = LogisticRegression()
        self.is_trained = False

    def train(self, csv_path):
        data = pd.read_csv(csv_path)

        X = self.vectorizer.fit_transform(data["prompt"])
        y = data["label"]

        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, prompt):
        if not self.is_trained:
            raise RuntimeError("Model is not trained")

        X = self.vectorizer.transform([prompt])
        pred = self.model.predict(X)[0]
        prob = self.model.predict_proba(X)[0][1]

        return pred, prob
