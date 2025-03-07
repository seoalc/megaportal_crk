from sqlalchemy import text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk
from app.applications.models import application_remedial_users
from app.material_users.models import Material_user


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

    # Отношение к таблице material_user (материалы на руках у пользователя)
    material_assignments: Mapped[list["Material_user"]] = relationship(
        "Material_user",
        back_populates="user",
        lazy="noload"
    )

    # Указываем, что связь идет по remedial_user_id
    # remedial_applications = relationship(
    #     "Application",
    #     back_populates="remedial_user",
    #     foreign_keys="Application.remedial_user_id"
    # )
    # Новый список назначенных заявок (через промежуточную таблицу)
    remedial_applications = relationship(
        "Application",
        secondary=application_remedial_users,
        back_populates="remedial_users"
    )

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"