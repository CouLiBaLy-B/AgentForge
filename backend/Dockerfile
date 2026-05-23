# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
RUN pip install bandit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables for production paths
ENV WORKSPACE_DIR=/app/workspace
ENV LOGS_DIR=/app/workspace/logs
ENV MEMORY_DIR=/app/memory

RUN mkdir -p $WORKSPACE_DIR $LOGS_DIR $MEMORY_DIR

EXPOSE 3000

CMD ["python", "main.py"]
