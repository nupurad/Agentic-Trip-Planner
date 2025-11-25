from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str


try:
    print("Loading agent graph on startup...")
    graph_builder = GraphBuilder(model_provider="groq")
    agent_graph = graph_builder()       # build the workflow
    print("Graph loaded successfully.")
except Exception as e:
    print("Failed to initialize graph:", e)
    agent_graph = None


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        if agent_graph is None:
            raise RuntimeError("Graph not initialized")

        user_message = {
            "messages": [
                {"role": "user", "content": query.question}
            ]
        }

        output = agent_graph.invoke(user_message)

        # Output format depends on your nodes
        if isinstance(output, dict) and "messages" in output:
            final_msg = output["messages"][-1].content
        else:
            final_msg = str(output)

        return {"answer": final_msg}

    except Exception as e:
        print("Error in /query:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
