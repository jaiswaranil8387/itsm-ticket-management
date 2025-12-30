# ========================
# 1st stage: Builder
# This stage installs dependencies.
# ========================
FROM python:3.11-slim-bookworm AS builder

# Set environment variables for Python.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv for dependency management.
RUN pip install uv

# Set the working directory for the builder stage.
WORKDIR /app

# Copy dependency file to leverage Docker's build cache.
COPY pyproject.toml .

# Create a virtual environment and install dependencies.
RUN uv venv .venv \
    && uv pip install --python .venv/bin/python flask==2.0.2 werkzeug==2.3.7

# Copy the rest of the application source code.
COPY . .

# ============================
# 2nd stage: Distroless Runtime
# This is our final, minimal image.
# ============================
FROM gcr.io/distroless/python3-debian12

# Set the working directory.
WORKDIR /app

# Copy the application source code.
COPY --from=builder /app .

# Find the Python version to correctly locate the site-packages.
# This assumes Python 3.11, as specified in the builder stage.
ARG PYTHON_VERSION=3.11

# Copy only the site-packages from the virtual environment.
# This contains the installed dependencies like Flask and Werkzeug.
COPY --from=builder /app/.venv/lib/python${PYTHON_VERSION}/site-packages /app/site-packages

# Set the PYTHONPATH to tell the native distroless Python interpreter
# where to find the installed packages.
ENV PYTHONPATH=/app/site-packages

# Explicitly set the ENTRYPOINT to the Python interpreter.
# This is a robust pattern for distroless images.
ENTRYPOINT ["/usr/bin/python3.11"]

# The CMD now serves as the default argument to the ENTRYPOINT.
# It specifies which Python script to run.
CMD ["/app/app.py"]

# Update the healthcheck to use the native Python interpreter.
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD ["/usr/bin/python3.11", "/app/healthcheck.py"]

EXPOSE 5000
