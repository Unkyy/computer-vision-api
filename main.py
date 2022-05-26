from ast import Return
from imp import reload
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
from io import BytesIO

import uvicorn
from models.Url import Url

from service.OcrModel import OcrModel
from service.Webtesting import Webtesting
from service.WrapperMongoClient import WrapperMongoClient
app = FastAPI()
import json


@app.post("/cocomodel/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/ocrmodel/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    image = np.asarray(Image.open(BytesIO(contents)).convert('RGB'))
    texts, boxes = OcrModel().read_text(image)
    # print(text)
    WrapperMongoClient().save("detected-text", {"boxes":json.dumps(boxes), "texts": texts})
    return {"filename": file.filename}

@app.post("/webtesting")
async def create_web_test():
    Webtesting("https://www.rosartjewels.com/").start()
    return {"filename": "tst"}


@app.post("/security")
async def create_security_test(url: Url):
    return {"test":"test"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload= True)
    
    
# https://www.anilia.fr/