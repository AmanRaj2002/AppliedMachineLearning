import app
import pytest
import joblib
import numpy as np
from score import score
from sklearn.base import BaseEstimator
import os

# Load model and vectorizer for tests (same as score.py)
model = joblib.load('best_model.joblib')
vectorizer = joblib.load('tfidf_vectorizer.joblib')

def test_score_smoke():
    """Smoke test: no crash."""
    result = score("test text", model, 0.5)
    assert len(result) == 2

def test_score_format():
    """Format test: correct types."""
    pred, prop = score("test", model, 0.5)
    assert isinstance(pred, bool)
    assert isinstance(prop, float)

@pytest.mark.parametrize("text, threshold", [
    ("test", 0.5),
    ("spam", 0.6),
])
def test_score_sanity(text, threshold):
    """Sanity: pred 0/1, prop 0-1."""
    pred, prop = score(text, model, threshold)
    assert pred in [True, False]
    assert 0 <= prop <= 1

def test_score_edge_threshold_0():
    """Edge: threshold=0 → always 1."""
    _, prop = score("any text", model, 0.0)
    assert prop > 0  # Assuming model probs >0
    pred, _ = score("any text", model, 0.0)
    assert pred is True

def test_score_edge_threshold_1():
    """Edge: threshold=1 → always 0."""
    _, prop = score("any text", model, 1.0)
    assert prop <= 1
    pred, _ = score("any text", model, 1.0)
    assert pred is False

@pytest.mark.parametrize("spam_text, ham_text", [
    ("Free entry to win $1000 now!!", "Hello, how are you?"),  # Obvious spam/ham [web:14]
])
def test_score_typical_spam(spam_text, ham_text):
    """Typical: spam →1, ham→0 (adjust threshold if needed)."""
    spam_pred, spam_prop = score(spam_text, model, 0.5)
    ham_pred, _ = score(ham_text, model, 0.5)
    # For real model, spam_prop high →1; assert based on expectation
    assert spam_prop > 0.5  # Assuming good model
    assert spam_pred is True
    assert ham_pred is False

# -------------- # -------------- # -------------->

# Additional to test.py for integration test
import pytest
import subprocess
import requests
import time
import signal
import os
from unittest.mock import patch

@pytest.fixture(scope="module")
def flask_server():
    """Launch Flask via CLI, yield, then kill."""
    proc = subprocess.Popen(
        ['flask', 'run', '--host=127.0.0.1', '--port=5000', '--no-debugger'], 
        cwd=os.getcwd(),  # Ensure correct dir
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid if os.name != 'nt' else None
    )
    time.sleep(5)  # Wait longer for startup
    yield proc
    if os.name != 'nt':
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    else:
        proc.terminate()
    proc.wait()

def test_flask(flask_server):
    """Integration: POST to /score, check response."""
    try:
        response = requests.post(
            'http://127.0.0.1:5000/score',  # Changed to 127.0.0.1
            json={'text': 'Free lotto prize!'},
            timeout=10
        )
        assert response.status_code == 200
        data = response.json()
        assert 'prediction' in data
        assert 'propensity' in data
        assert isinstance(data['prediction'], bool)
        assert isinstance(data['propensity'], float)
        print(f"Flask response: {data}")  # Debug print
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Flask connection failed: {e}")
