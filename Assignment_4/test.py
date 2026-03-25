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
    # Check if the process exists before trying to kill it
    if os.name != 'nt':
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass # The process is already dead, which is fine

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

#---Updated for Assignement 4---

import os
import time
import requests
import subprocess

def test_docker():
    print("Building Docker image...")
    build_command = "docker build -t my_flask_app ."
    os.system(build_command)
    
    # FIX: Bind container's 5000 to host's 5001
    print("Running Docker container...")
    run_command = ["docker", "run", "-d", "-p", "5001:5000", "my_flask_app"]
    
    container_id = subprocess.check_output(run_command).decode('utf-8').strip()
    time.sleep(5) 
    
    try:
        # FIX: Point request to port 5001
        url = 'http://127.0.0.1:5001/score'
        sample_data = {"text": "This is a sample text for testing the model."} 
        
        response = requests.post(url, json=sample_data)
        assert response.status_code == 200
        print("Docker test passed successfully!")
        
    finally:
        print(f"Stopping and removing container {container_id}...")
        os.system(f"docker stop {container_id}")
        os.system(f"docker rm {container_id}")
    
    try:
        # 3. Send a request to the localhost endpoint /score
        # NOTE: Adjust the JSON payload key ('text' vs 'review', etc.) to match what your Assignment 3 app.py expects!
        url = 'http://127.0.0.1:5000/score'
        sample_data = {"text": "This is a sample text for testing the model."} 
        
        response = requests.post(url, json=sample_data)
        
        # 4. Check if the response is as expected
        assert response.status_code == 200
        print("Docker test passed successfully!")
        
    finally:
        # 5. Close the docker container
        print(f"Stopping and removing container {container_id}...")
        os.system(f"docker stop {container_id}")
        os.system(f"docker rm {container_id}")