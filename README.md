brew install uv
uv --version

uv init AI-Trip-Planner

uv python list
uv venv --python 3.12
source .venv/bin/activate

uv pip list
uv pip install <package-name>
uv pip install -r requirements.txt


streamlit run app.py

uvicorn main:app --host 0.0.0.0 --port 8000 --reload


