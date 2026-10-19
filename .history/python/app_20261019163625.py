from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
from pathlib import Path

from fastapi.middleware.cors import CORMiddleware

## Read the csv file
folder = Path(__file__).resolve().parent.parent

nodes = pd.read_csv(folder / "data" / "nodes.csv")
adjacency_matrix = pd.read_csv(folder / "data" / "adjacency_matrix.csv")

print(nodes.head())
print(adjacency_matrix.head())

app = FastAPI()

class PathRequest(BaseModel):
    start: str
    goal: str
    
@app.post("/route")
def find_route(request: PathRequest):

    # A* function
    script_globals = {}

    with open('main.py', 'r') as file:
        script_code = file.read()
    
    exec(script_code, script_globals)

    output_data = script_globals.get('path_image', '')

    return {
        "start": request.start,
        "goal": request.goal,
        "message": "Choices received"
    }
    
# Add CORS middleware
app.add_middleware(
    CORMiddleware,allow_origins=[
        "http://localhost:5500",
    ],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],)