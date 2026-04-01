FROM python:3.11-slim

# System deps if needed for FAISS or other vector libs
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Create a dir inside the container
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code over to container
COPY . .

EXPOSE 8000

# Start the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]