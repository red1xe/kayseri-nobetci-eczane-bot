FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . /app

# Create a non-root user and switch to it (best-effort on some base images)
RUN addgroup --system app && adduser --system --ingroup app app || true
USER app

CMD ["python","-u","bot/main.py"]
