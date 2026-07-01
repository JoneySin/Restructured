# 1. Use the official Python slim image to keep image size small and deployment fast
FROM python:3.11-slim

# 2. Install required system tools (needed for C-extension libraries like uvloop/orjson)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /Auto-Filter-Bot

# 4. Set Python environment variables
# PYTHONDONTWRITEBYTECODE=1 -> prevents unnecessary .pyc files in the container (saves RAM and disk space)
# PYTHONUNBUFFERED=1 -> shows logs live and instantly, with no buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 5. Copy only requirements.txt first (to take advantage of Docker layer caching)
COPY requirements.txt .

# 6. Install dependencies and clear pip's cache to keep the container lightweight
RUN pip install --no-cache-dir -r requirements.txt

# 7. Now copy the rest of the project code
COPY . .

# 8. Command to run the bot
CMD ["python", "bot.py"]
