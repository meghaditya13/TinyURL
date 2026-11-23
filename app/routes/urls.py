from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.url import URLCreate
from app.models.url import URL
from app.utils import short_code_generator

from sqlalchemy import select

from fastapi.responses import RedirectResponse # to return a response of redirect
from fastapi import HTTPException #to raise an HTTPException when there is no url to be found
from sqlalchemy.exc import IntegrityError


router = APIRouter()

@router.post("/shorten")
def get_url(data: URLCreate, db:Session = Depends(get_db)):

	MAX_RETRIES = 5

	for retry_index in range(MAX_RETRIES):
		code = short_code_generator()

		orm_obj = URL()
		orm_obj.short_code = code
		orm_obj.original_url = data.url
		try: 
			db.add(orm_obj)
			db.commit()
			break
		except IntegrityError: # handling run condition and uniqueness of short_code
			db.rollback() # doest undo commit or smtg, it makes db usable again from the the error state
			
	if not COMMITED_FLAG:
		raise RuntimeError("Failed to create URl")
	response = {}

	response['short_code'] = code
	response['short_url'] = f"http://127.0.0.1:8000/{code}"
	response['original_url'] = str(data.url)

	return response


@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

	stmt = select(URL).where(URL.short_code == short_code) # i still dont get why i am using URL in select ?

	row_orm_obj = db.scalar(stmt)

	if row_orm_obj is None:

		raise HTTPException(status_code = 404, detail = "URL not found")

	row_orm_obj.clicks += 1

	original_url = row_orm_obj.original_url

	db.commit()

	return RedirectResponse(status_code = 307, url = original_url)


