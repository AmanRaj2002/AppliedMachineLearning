# score.py
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import BaseEstimator

# Load the best model and vectorizer from train.ipynb (assume saved as 'best_model.joblib' or 'model.pkl')
# Adjust filename/path based on your repo's train.ipynb output
model = joblib.load('best_model.joblib')  # or 'model.pkl'
vectorizer = joblib.load('tfidf_vectorizer.joblib')  # Assume vectorizer saved too; critical for text

def score(text: str, model: BaseEstimator, threshold: float) -> tuple[bool, float]:
    """
    Scores a trained model on text: returns prediction (bool) and propensity (float).
    Assumes binary classification (spam=1), model has predict_proba.
    """
    # Transform text
    text_vec = vectorizer.transform([text])
    # Get propensity (prob of class 1/spam)
    propensity = model.predict_proba(text_vec)[0][1]
    # Binary prediction based on threshold
    prediction = propensity > threshold
    return bool(prediction), float(propensity)
