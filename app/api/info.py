import os
import json

from fastapi import APIRouter
from app.config import KEYDB
from app.schema import ChatBot
from app.services.info import process_query

info = APIRouter()

@info.get('/fine-prints')
def get_fine_prints():
    with open(os.path.join(os.getcwd(),KEYDB),'rb') as f:
        obj = json.load(f)

    return {"response":obj}


@info.post('/chatbot')
def chatbot(request:ChatBot):
    response = process_query(request.query)
    return {"response":response}