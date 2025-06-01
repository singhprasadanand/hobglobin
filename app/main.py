import os

import uvicorn
from fastapi import FastAPI

from app.api.knowledge import knowledge
from app.api.info import info

app = FastAPI()
app.include_router(knowledge,tags=['Knowledge'])
app.include_router(info,tags=['information'])

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)