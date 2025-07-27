FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY src/ ./src/
COPY db/ ./db/

# Create non-root user
RUN useradd -m -u 1000 ffm && chown -R ffm:ffm /app
USER ffm

# Run the application
CMD ["python", "-m", "src.main"]