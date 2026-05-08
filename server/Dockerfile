FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy metadata files needed for installation
COPY pyproject.toml ./

# Copy the actual source code directory 
# (Make sure this name matches what is in [tool.setuptools] packages)
COPY stac_validator/ ./stac_validator/

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system . uvicorn fastapi requests

# Copy the server directory specifically
COPY server/ ./server/

# Final install
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system .

# Create schema cache directory
RUN mkdir -p local_schemas/.schemas && chmod -R 777 local_schemas

EXPOSE 8000

# Start the server using uvicorn
# Note: Since we are in /app and copied the root, 
# 'server.server:app' points to 'server/server.py'
CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]