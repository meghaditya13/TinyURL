import fastapi 

from app.database import engine, Base
from app.models.url import URL

from app.routes.urls import router

Base.metadata.create_all(bind = engine)

app = fastapi.FastAPI()
app.include_router(router)

@app.get("/")
async def test1():
	return {'message':'HI'}

if __name__ == '__main__':
	pass