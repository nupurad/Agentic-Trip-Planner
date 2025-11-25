#!/bin/bash

# Function to handle shutdown
shutdown() {
    echo "Stopping FastAPI and Streamlit..."
    kill $FASTAPI_PID $STREAMLIT_PID
    wait $FASTAPI_PID $STREAMLIT_PID
    exit 0
}

# Trap SIGTERM and SIGINT to trigger shutdown
trap shutdown SIGTERM SIGINT

# Start FastAPI in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Start Streamlit in the background
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 &
STREAMLIT_PID=$!

# Wait for both processes
wait $FASTAPI_PID $STREAMLIT_PID
