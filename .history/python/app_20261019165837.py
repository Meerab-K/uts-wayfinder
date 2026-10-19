from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import pandas as pd
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

import jsonify
from main import *

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

    return jsonify({"status": "success", "result": output_data})
    
    '''
    return {
        "start": request.start,
        "goal": request.goal,
        "message": "Choices received"
    }
    '''
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],)