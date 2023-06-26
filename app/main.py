import os
import pathlib
import sys
import uvicorn
from fastapi import FastAPI, UploadFile
import model
import numpy as np
from PIL import Image
from io import BytesIO
app = FastAPI()

BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model"
MODEL_PATH = MODEL_DIR / "model.h5"

AI_MODEL = None

@app.on_event("startup")
def on_startup():
    global AI_MODEL, DB_SESSION
    AI_MODEL = model.AIModel(
        model_path= MODEL_PATH
    )

@app.get("/status")
async def chech_status():
    return {"hello": "world"}

@app.post("/predict", status_code=201)
async def predict(file: UploadFile):
    # print(file.filename)
    # print(file.content_type)
    global AI_MODEL
    im = Image.open(file.file)
    if im.mode in ("RGBA", "P"): 
        im = im.convert("RGB")
    input_pred = np.array(im)
    pred, acc = AI_MODEL.predict(input_pred)
    return {"class": pred, "accuracy": str(acc)}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)