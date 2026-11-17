from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.url import URLCreate
from app.models.url import URL
from app.utils import short_code_generator

from sqlalchemy import select

from fastapi.responses import RedirectResponse # to return a response of redirect
from fastapi import HTTPException #to raise an HTTPException when there is no url to be found


router = APIRouter()

@router.post("/shorten")
def get_url(data: URLCreate, db:Session = Depends(get_db)):
	'''
	while code in db.short_code:
		code = short_code_generator()
	'''
	#can't do stuuf like that on db which is a session, work on orm model instead which is upward projection of actual sql db

	while True:
		code = short_code_generator()
		statement = select(URL).where(URL.short_code == code)
		existing = db.scalar(statement) # basically returns the first row or None if there is no row
		if existing is None:
			break

	#db.add(code, data.url)

	orm_obj = URL()
	orm_obj.short_code = code
	orm_obj.original_url = data.url

	db.add(orm_obj)
	db.commit()

	#db.refresh() #why am i refreshing ? its not like we need to update orm metadata everytime we add/edit/write to database ? why refresh the session ?

	db.refresh(orm_obj) #ok, why should i care about the instance, no, why would i want to refresh it in first place ? because orm_obj expires after commit

	response = {}

	response['short_code'] = code
	response['short_url'] = f"http://127.0.0.1:8000/{short_code}"
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


