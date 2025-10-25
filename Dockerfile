FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY src .

COPY . .
RUN ls -la /app
CMD ["gunicorn",  "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]