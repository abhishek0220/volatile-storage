from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import os
import json

ROOT_STORE_PATH = os.path.join(os.getcwd(), 'tem')
SERVER_LINK = "https://storage.abhis.me"

app = FastAPI()

class DataBlock(BaseModel):
    data: str

class CreateResponse(BaseModel):
    link: str = SERVER_LINK+"/file/<UID>"

class GetFileResponse(BaseModel):
    status: str = "OK"
    file: DataBlock

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/create", response_model=CreateResponse)
async def create_data(data_obj: DataBlock):
    file_name = str(uuid.uuid4()) + ".json"
    file_loc = os.path.join(ROOT_STORE_PATH, file_name)

    json_object = json.dumps(data_obj.dict(), indent = 4)
  
    with open(file_loc, "w") as outfile:
        outfile.write(json_object)

    return {"link": SERVER_LINK+"/file/"+ file_name}


@app.get('/file/{file_id}', response_model=GetFileResponse)
async def get_file(file_id: str):
    file_loc = os.path.join(ROOT_STORE_PATH, file_id)
    resp = {}
    try:
        with open(file_loc, "r") as openfile:
            json_object = json.load(openfile)
    except:
        resp['status'] = "NOT_OK"
    else:
        resp['file'] = json_object
    return resp
