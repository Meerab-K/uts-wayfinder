from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PathRequest(BaseModel):
    start: str
    goal: str