FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg gcc && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# api:app means "look in api.py for the object named app"
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "api:app", "--timeout", "600"]
