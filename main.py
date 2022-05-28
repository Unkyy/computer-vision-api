from ast import Return
from imp import reload
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
from io import BytesIO

import uvicorn
from models.Url import Url

from service.OcrModel import OcrModel
from service.Web_testing import Web_testing
from service.Web_testing_herf import Web_testing_herf
from service.Web_testing_ocr import Web_testing_ocr
from service.WrapperMongoClient import WrapperMongoClient
app = FastAPI()
import json

from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/webtesting/href")
async def create_web_test_href():
    website = "https://www.python.org/"
    test = Web_testing_herf(website)
    links = test.start(test.geturls)
    WrapperMongoClient(host="localhost", port="27217")\
        .save("nodes", {"test":"href","website": website, "links":json.dumps(links),'created_time': datetime.now()})
    return {"filename": "tst"}

@app.post("/webtesting/ocr")
async def create_web_test():
    website = "https://www.rosartjewels.com/"
    test = Web_testing_ocr(website)
    links = test.start(test.scroll)
    WrapperMongoClient(host="localhost", port="27217")\
        .save("nodes", {"test":"or","website": website, "links":json.dumps(links),'created_time': datetime.now()})
    return {"filename": "tst"}
@app.get("/test")
async def get_tests():
    data = WrapperMongoClient(host="localhost", port="27217").list("nodes")
    node = []
    node.append({"id":data[0]["website"]})
    for line in data:
        for link in json.loads(line["links"]):
            if({"id": link["target"]} not in node):
                node.append({"id": link["target"]})
        line["nodes"] = node
    print(data[-1]["links"])
    return [data[-1]]
@app.post("/security")
async def create_security_test(url: Url):
    WrapperMongoClient(host="localhost", port="27217").save("tzes", {"website": "test"})
    return {"test":"test"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload= True)
    
    
# https://www.anilia.fr/