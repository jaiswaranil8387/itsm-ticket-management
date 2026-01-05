# ========================
# 1st stage: Builder
# ========================
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tool
RUN pip install uv

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv venv .venv \
    && uv pip install --no-cache --python .venv/bin/python pip==25.3 \
    && uv pip install --no-cache --python .venv/bin/python -r requirements.txt

# Copy source code
COPY . .

# ============================
# 2nd stage: Runtime
# ============================
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install PostgreSQL client libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application from builder
COPY --from=builder /app .

# 1. COPY LIBRARIES (Same as before)
COPY --from=builder /app/.venv/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# 2. [NEW] COPY BINARIES 
# We must copy the 'bin' folder to get 'opentelemetry-instrument' and 'flask' commands
COPY --from=builder /app/.venv/bin/* /usr/local/bin/

# 3. [NEW] UPDATE STARTUP COMMAND
# We remove ENTRYPOINT ["python3"] because we need to run the wrapper executable first.
# This bakes the instrumentation directly into the image.
CMD ["opentelemetry-instrument", "python", "/app/app.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD ["python3", "/app/healthcheck.py"]

EXPOSE 5000