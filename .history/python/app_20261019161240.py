from fastapi import FastAPI
from pydantic import BaseModel

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