from sqlalchemy import text, String, Text, Table, Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, str_uniq, int_pk

# Промежуточная таблица для связи "многие ко многим"
application_remedial_users = Table(
    "application_remedial_users",
    Base.metadata,
    Column("application_id", Integer, ForeignKey("applications.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int_pk]
    appearance_date: Mapped[date]
    subscriber_number: Mapped[int]
    subscriber_addres: Mapped[str] = mapped_column(String(length=255))  # Указана длина
    complaint_text: Mapped[str] = mapped_column(Text, nullable=True)
    contact_number: Mapped[str] = mapped_column(String(length=15))
    solution_description: Mapped[str] = mapped_column(Text, nullable=True)
    closed_text: Mapped[str] = mapped_column(Text, nullable=True)
    # Внешний ключ на таблицу users
    user_id_created_application: Mapped[int] = mapped_column(ForeignKey("users.id"))
    application_status: Mapped[int] = mapped_column(nullable=True)

    # Отношение с таблицей User
    # user: Mapped["User"] = relationship("User", back_populates="applications")
    # remedial_user: Mapped["User"] = relationship("User", foreign_keys=[remedial_user_id], back_populates="remedial_applications")
    # Указываем имя обратной связи
    creator = relationship(
        "User",
        back_populates="created_applications",
        foreign_keys=[user_id_created_application]
    )

    # remedial_user = relationship(
    #     "User",
    #     back_populates="remedial_applications",
    #     foreign_keys=[remedial_user_id]
    # )
    # Новый список исполнителей (через промежуточную таблицу)
    remedial_users = relationship(
        "User",
        secondary=application_remedial_users,
        back_populates="remedial_applications"
    )

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
            "closed_text": self.closed_text,
            "user_id_created_application": self.user_id_created_application,
            "application_status": self.application_status,
        }