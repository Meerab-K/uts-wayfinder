import base64

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import networkx as nx
from main import neighbours, buildings, my_astar_path, draw_map

app = FastAPI()

# Create the graph
G = nx.Graph()
G.add_weighted_edges_from(neighbours)
G.add_nodes_from(buildings)

class PathRequest(BaseModel):
    start: str
    goal: str
    
@app.post("/route")
def find_route(request: PathRequest):
    
    start = request.start
    goal = request.goal

    # Check if buildings exist
    if start not in G or goal not in G:
        raise HTTPException(
            status_code=400,
            detail="Invalid start or goal building"
        )

    # Call A* from main.py
    path, explored = my_astar_path(G, start, goal)

    if path is None:
        raise HTTPException(
            status_code=404,
            detail="No route found"
        )

    route_edges = []
    for i in range(len(path) - 1):
        route_edges.append((path[i], path[i + 1]))

    drawn_path = draw_map(G, route_edges)

    # Calculate total distance
    distance = nx.path_weight(G, path, "weight")
    
    return {
        "path": path,
        "distance": distance,
        "map_image": base64.b64encode(drawn_path).decode("ascii")
    }
    
    '''
    return {
        "start": request.start,
        "goal": request.goal,
        "message": "Choices received"
    }
    '''
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://meerab-k.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],)