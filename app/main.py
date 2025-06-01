import os

import uvicorn
from fastapi import FastAPI

from app.api.knowledge import knowledge

app = FastAPI()
app.include_router(knowledge,tags=['Knowledge'])

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True)