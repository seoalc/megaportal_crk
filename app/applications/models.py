from sqlalchemy import text, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, str_uniq, int_pk


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int_pk]
    appearance_date: Mapped[date]
    subscriber_number: Mapped[int]
    subscriber_addres: Mapped[str] = mapped_column(String(length=255))  # Указана длина
    complaint_text: Mapped[str] = mapped_column(Text, nullable=True)
    contact_number: Mapped[str] = mapped_column(String(length=15))
    solution_description: Mapped[str] = mapped_column(Text, nullable=True)
    # Внешний ключ на таблицу users
    user_id_created_application: Mapped[int] = mapped_column(ForeignKey("users.id"))
    application_status: Mapped[int] = mapped_column(default=0)

    # Отношение с таблицей User
    user: Mapped["User"] = relationship("User", back_populates="applications")

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "appearance_date": self.appearance_date,
            "subscriber_number": self.subscriber_number,
            "subscriber_addres": self.subscriber_addres,
            "complaint_text": self.complaint_text,
            "contact_number": self.contact_number,
            "solution_description": self.solution_description,
            "subscriber_number": self.subscriber_number,
            "user_id_created_application": self.user_id_created_application
        }