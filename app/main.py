import os
import pathlib
import sys
import uvicorn
from fastapi import FastAPI, UploadFile

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(directory.parent)
from model import model

app = FastAPI()

MODEL_DIR = BASE_DIR.parent / "model"
MODEL_PATH = MODEL_DIR / "model.h5"

AI_MODEL = None

@app.on_event("startup")
def on_startup():
    global AI_MODEL, DB_SESSION
    AI_MODEL = ml.AIModel(
        model_path= MODEL_PATH
    )

@app.get("/status")
async def chech_status():
    return {"hello": "world"}

@app.post("/predict", status_code=201)
async def predict(file: UploadFile):
    print(file.name)
    print(file.content_type)
    global AI_MODEL
    pred = AI_MODEL.predict(file.file)
    print(pred)
    return pred


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)