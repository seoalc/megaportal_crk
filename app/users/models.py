from sqlalchemy import text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    user_name: Mapped[str_uniq] = mapped_column(String(length=128))  # Указана длина
    fio: Mapped[str] = mapped_column(String(length=128))  # Указана длина
    password: Mapped[str] = mapped_column(String(length=255))  # Указана длина
    user_status: Mapped[int] = mapped_column(default=0)

    # applications = relationship("Application", back_populates="user")
    # remedial_applications = relationship("Application", foreign_keys="[Application.remedial_user_id]", back_populates="remedial_user")
    # Указываем, что связь идет по user_id_created_application
    created_applications = relationship(
        "Application",
        back_populates="creator",
        foreign_keys="Application.user_id_created_application"
    )

    # Указываем, что связь идет по remedial_user_id
    remedial_applications = relationship(
        "Application",
        back_populates="remedial_user",
        foreign_keys="Application.remedial_user_id"
    )

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"