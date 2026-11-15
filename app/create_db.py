from app.database import engine, Base
from app.models.url import URL

Base.metadata.create_all(bind = engine)

if __name__ == '__main__':
	print(Base.metadata.tables)
	print(type(URL.__table__))
	print(URL.__table__.columns.keys())
