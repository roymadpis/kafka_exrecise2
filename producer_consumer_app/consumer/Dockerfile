FROM python:3.12-slim

# Install pipx
RUN apt update && apt install -y pipx && pipx ensurepath

# Ensure pipx uses user location
ENV PIPX_BIN_DIR="/root/.local/bin"
ENV PATH="${PIPX_BIN_DIR}:${PATH}"

# Install uv
RUN pipx install uv

# Set workdir to project root
WORKDIR /app

# Copy only project dependencies first (for better Docker cache)
COPY ../pyproject.toml ../uv.lock* ./

# Create and install dependencies into a virtual environment using uv
RUN uv venv && uv pip install .

# Copy application code
COPY .. .

# Expose Prometheus metrics port (adjust if needed)
EXPOSE 8001

# Default entrypoint 
ENTRYPOINT ["uv", "run", "--", "python", "-m", "consumer.consumer"]
# ENTRYPOINT ["/app/.venv/bin/python", "-m", "consumer.consumer"]