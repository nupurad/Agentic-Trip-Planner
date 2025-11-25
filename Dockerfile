FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies needed for many Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose both FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Environment settings
ENV PYTHONUNBUFFERED=1

# Start both back-end and front-end when the container launches
# FastAPI runs on 0.0.0.0:8000
# Streamlit runs on 0.0.0.0:8501
# Copy start script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Run both FastAPI and Streamlit
CMD ["./start.sh"]
