#FastAPI

from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os

app = FastAPI()


class QueryRequest(BaseModel):
    query: str 

@app.post("/query")
async def handle_query(query: QueryRequest):
    try:
        print(query)
        #object of GraphBuilder class
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        #graph image
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        
        print("Graph saved as 'my_graph.png' in {os.getcwd()}'")

        #pydantic validation
        messages={"messages": [query.query]}

        output = react_app.invoke(messages)

        #if instance is decitionary
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



    