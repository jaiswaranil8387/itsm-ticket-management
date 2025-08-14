# ============================
# 1st stage: Builder
# ============================
FROM python:3.9-slim-bookworm AS builder

# Prevent Python from writing .pyc files & force stdout flush
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies (remove after build)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*docl

# Set working directory
WORKDIR /app

# Copy requirements and install into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ============================
# 2nd stage: Runtime
# ============================
FROM python:3.9-slim-bookworm

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy Python virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy only application code (no venv, no build deps)
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/')"

# Run the application
CMD ["python", "app.py"]
