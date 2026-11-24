from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database import engine, Base
from app.models.url import URL

from app.routes.urls import router

Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(router)

@app.get("/")
async def home():
	return FileResponse("app/static/index.html")

if __name__ == '__main__':
	pass