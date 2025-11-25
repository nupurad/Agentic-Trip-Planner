# WanderBot - An Agentic-AI based Trip Planner Agent 
### (http://3.80.113.62:8501/)

### An AI-powered agent capable of planning a trip to any place world-wide using real-time data.
### Features:
    1. Real-time weather information and forecast
    2. Activities-to-do and Local Attractions
    3. Hotel Cost (single-day/multi-day)
    4. Currency Conversion
    5. Complete Itinerary Planning
    6. Total Expense Calculation
    7. A summary of the suggested itenerary

## Technologies: LangGraph + FastAPI + Streamlit

### API KEYS:
    1. Groq
    2. Google Studio
    3. Google Places
    4. FourSquare
    5. Tavily
    6. Open Weather Map
    7. Langchain

## Step-by-step Implementation

### Install dependencies and define project
brew install uv
uv --version

uv init AI-Trip-Planner

uv python list
uv venv --python 3.12
source .venv/bin/activate

uv pip list
uv pip install <package-name>
uv pip install -r requirements.txt

### Run app (port=8501)
streamlit run app.py

### Run backend (port=8000)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


### Containerize (Docker) and push 
docker buildx build --platform linux/amd64 -t agentic-trip-planner:1.0 .
docker tag agentic-trip-planner:1.0 nupurad/ai-trip-planner-agent
docker run -d --env-file .env -p 80:3000 agentic-trip-planner:1.0
docker push nupurad/ai-trip-planner-agent 

### Create EC2 free-tier instance
AWS console --> download .pem file (t2.micro)
ssh -i ~/.ssh/your-key.pem ec2-user@ec2-<your-public-IP>.compute-1.amazonaws.com

### Add env to EC2 instance
scp -i ai-trip-planner-agent.pem .env ec2-user@<your-public-IP>:/home/ec2-user/

### Make EC2 instance ready for Docker
sudo yum install docker
sudo systemctl start docker
sudo docker pull agentic-trip-planner:latest
sudo docker run -d --env-file .env -p 8000:8000 -p 8501:8501 nupurad/ai-trip-planner-agent:latest

### Use systemd to automatically run image
sudo nano /etc/systemd/system/agentic-trip-planner.service

[Unit]
Description=Trip Planner App
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run --rm -p 8000:8000 -p 8501:8501 --env-file /home/ec2-user/.env nupurad/ai-trip-planner-agent:latest
ExecStop=/usr/bin/docker stop agentic-trip-planner

[Install]
WantedBy=multi-user.target

Ctrl+O 
Ctrl+Enter
Ctrl+X

sudo systemctl daemon-reload

sudo systemctl enable agentic-trip-planner

sudo systemctl start agentic-trip-planner

sudo systemctl status agentic-trip-planner



### Helpful commands
    1. sudo docker stop <container-id>
    2. sudo docker rm <container-id>
    3. sudo docker images
    4. sudo docker ps
    5. sudo docker logs <container-id>






