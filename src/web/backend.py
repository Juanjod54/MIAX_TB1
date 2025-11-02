import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def index():
    path = os.path.join("src/resources/index.html")
    return FileResponse(path)
