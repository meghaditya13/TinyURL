from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Settings(BaseSettings):
	database_url : str
	base_url : str = "http://127.0.0.1:8000"
	model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()

engine = create_engine(url = settings.database_url) # create engine

SessionLocal = sessionmaker(bind = engine, autoflush = False) # create session factory


class Base(DeclarativeBase):
	pass

if __name__ == '__main__':

	print(settings.database_url)
	print(engine, type(engine))
	print(type(SessionLocal))

	with engine.connect() as connection:
		print("engine connected")
