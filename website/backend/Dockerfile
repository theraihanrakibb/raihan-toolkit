# syntax=docker/dockerfile:1.6

# raihan-toolkit backend — FastAPI
# python:3.11-slim, non-root, runs uvicorn on port 8000.
FROM python:3.11-slim

# Non-root user
RUN useradd --create-home --uid 1000 app

WORKDIR /app

# Install deps first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Drop privileges
USER app

EXPOSE 8000

# No reload in production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
