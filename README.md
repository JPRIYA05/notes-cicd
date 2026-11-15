# Student Notes Manager - CI/CD Mini Project

Flask notes app deployed automatically: push -> test -> Docker build -> Docker Hub -> cloud VM.

## Run locally
    pip install -r requirements.txt
    python app.py          # http://localhost:5000
    pytest -v              # run tests

## GitHub Secrets required
DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, VM_HOST, VM_USER, VM_SSH_KEY

## VM one-time setup (Ubuntu)
    sudo apt update && sudo apt install -y docker.io
    sudo usermod -aG docker $USER
