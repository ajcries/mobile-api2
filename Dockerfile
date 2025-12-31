FROM python:3.10-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from your repo into the /app folder
COPY . .

# IMPORTANT: Ensure 'api' matches your filename 'api.py' 
# and 'app' matches the variable 'app = Flask(__name__)'
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "api:app", "--timeout", "600"]
