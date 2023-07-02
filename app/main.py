import os
import pathlib
import sys
import uvicorn
from fastapi import FastAPI, UploadFile, Request, Response, status
import model
import numpy as np
from PIL import Image
from io import BytesIO
from fastapi.exceptions import HTTPException
import monitoring
import time

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model"
MODEL_PATH = MODEL_DIR / "model.h5"

AI_MODEL = None

MONITORING = monitoring.monitoring()

@app.on_event("startup")
def on_startup():
    global AI_MODEL, DB_SESSION
    AI_MODEL = model.AIModel(
        model_path= MODEL_PATH
    )

@app.get("/metric")
async def chech_status(request: Request):
    print(request.client.host)
    if str(request.client.host) == "127.0.0.1" or str(request.client.host) == "185.173.104.89" or str(request.client.host) == "185.208.79.8":
        return MONITORING.status_inference()

    raise HTTPException(status_code=403, detail="Not accessible")

@app.post("/predict", status_code=201)
async def predict(file: UploadFile):
    global AI_MODEL

    # check the content type
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        MONITORING.add_number_of_fail_req_inference()
        raise HTTPException(status_code=400, detail="Invalid file type")

    start = time.time()
    im = Image.open(file.file)
    if im.mode in ("RGBA", "P"): 
        im = im.convert("RGB")
    input_pred = np.array(im)
    pred, acc = AI_MODEL.predict(input_pred)
    end = time.time()
    MONITORING.add_number_of_suc_req_inference(acc=acc,label=pred,duration=end-start)
    return {"class": pred, "accuracy": str(acc)}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)