from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class URL(Base):

	__tablename__ = "urls"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement =True)
	clicks: Mapped[int] = mapped_column(default = 0)
	short_code: Mapped[str] = mapped_column(String(6), unique = True, index = True)
	original_url: Mapped[str] = mapped_column(Text, nullable = False)

