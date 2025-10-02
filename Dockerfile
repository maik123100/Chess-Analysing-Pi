FROM python:3.11-slim

# Install system dependencies including Stockfish
RUN apt-get update && apt-get install -y \
    curl \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python scripts
COPY . .

# Make sure scripts are executable
RUN chmod +x start_ChessDB_updating_service.sh

# Default command - will be overridden by docker-compose
CMD ["python3", "ChessDB_updating_service.py", "std"]