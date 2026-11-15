import fastapi 
from fastapi import Depends

from sqlalchemy.orm import Session
from app.dependencies import get_db

import asyncio
import time

from app.routes.urls import router

app = fastapi.FastAPI()
#print(type(app))


app.include_router(router)

@app.get("/async-test")
async def async_test():
    print("Async started")
    await asyncio.sleep(5)
    print("Async finished")
    return {"type": "async"}

@app.get("/sync-test")
def sync_test():
    print("Sync started")
    time.sleep(5)
    print("Sync finished")
    return {"type": "sync"}

@app.get("/test")
def test(db:Session = Depends(get_db)):
    return {"message": str(type(db))}

@app.get("/")
async def test1():
	return {'message':'Welcome to Hell'}

if __name__ == '__main__':
	pass