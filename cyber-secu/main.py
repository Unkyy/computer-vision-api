import os 
import uvicorn
from fastapi import FastAPI

from services.WrapperMongoClient import WrapperMongoClient
app = FastAPI()

from pydantic import BaseModel, Field


class Url(BaseModel):
    url: str = Field(example="website.com")


@app.post("/security")
async def create_security_test(url: Url):
    url ="192.168.1.254"
    nmap="nmap -sS -T4 -p- "+ url
    wpscan="wpscan --url "+url
    nikto="nikto -h "+url
    nmap = os.system(nmap)
    wpscan = os.system(wpscan)
    nikto = os.system(nikto)
    WrapperMongoClient().save("detected-text", {"nmap":nmap, "wpscan": wpscan,"nikto":nikto})

    # WrapperMongoClient(host="localhost", port="27217").save("tzes", {"website": "test"})
    return {"test":"test"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=1212, reload= True)