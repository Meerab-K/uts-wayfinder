from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
from pathlib import Path

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
    return {
        "start": request.start,
        "goal": request.goal,
        "message": "Choices received"
    }