from python:3.11-slim
WORKDIR /app
run python3 -m venv app_pi
env PATH="/app/app_pi/bin:$PATH"

COPY . /app

run pip install -r requirements.txt

cmd ["python","run.py"]

