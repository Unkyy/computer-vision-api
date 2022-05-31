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
from service.Web_testing_ia import Web_testing_ia
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
    WrapperMongoClient()\
        .save("nodes", {"test":"href","website": website, "links":json.dumps(links),'created_time': datetime.now()})
    return {"filename": "tst"}

@app.post("/webtesting/cv")
async def create_web_test():
    website = "https://www.rosartjewels.com/"
    test = Web_testing_ia(website,type_test="cv")
    links = test.start(test.scroll)
    WrapperMongoClient()\
        .save("nodes", {"test":"or","website": website, "links":json.dumps(links),'created_time': datetime.now()})
    return {"filename": "tst"}

@app.post("/webtesting/ocr")
async def create_web_test():
    website = "https://www.rosartjewels.com/"
    print("ocr")
    test = Web_testing_ia(website)
    links = test.start(test.scroll)
    WrapperMongoClient()\
        .save("nodes", {"test":"or","website": website, "links":json.dumps(links),'created_time': datetime.now()})
    return {"filename": "tst"}

@app.get("/test/{test1}/{test2}")
async def get_tests(test1,test2):
    data = WrapperMongoClient()\
        .list("nodes",{"website":{"$regex": "/.*www.rosartjewels.com.*/"}}\
            ,{'_id': 0})
    data2 = WrapperMongoClient()\
        .list("nodes",{"website":{"$regex": "/.*www.python.org.*/"}}\
            ,{'_id': 0})
    node = []
    node.append({"id":data[0]["website"]})
    detected = False
    print(data2)
    for link in json.loads(data[0]["links"]):
        if({"id": link["target"]} not in node):
            node.append({"id": link["target"], "color": "green"})
        for link2 in json.loads(data2[0]["links"]):
            if(link["target"] == link2["target"]):
                detected =True
        if(detected == False):
            print(node[-1])
        else:
            detected =False 
    data[0]["nodes"] = node
    return data

@app.get("/tests")
async def get_tests_name():
    data = WrapperMongoClient().list("nodes",{},{'_id': 0,"nodes":0,"links":0})
    return data

@app.post("/security")
async def create_security_test(url: Url):
    WrapperMongoClient().save("tzes", {"website": "test"})
    return {"test":"test"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload= True)
    
    
# https://www.anilia.fr/