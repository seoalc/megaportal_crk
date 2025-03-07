from sqlalchemy import text, String, Text, Table, Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, str_uniq, int_pk

# # Промежуточная таблица для связи "многие ко многим"
# application_remedial_users = Table(
#     "application_remedial_users",
#     Base.metadata,
#     Column("application_id", Integer, ForeignKey("applications.id", ondelete="CASCADE"), primary_key=True),
#     Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
# )

class Material_title(Base):
    __tablename__ = "material_titles"

    id: Mapped[int_pk]
    material_title: Mapped[str] = mapped_column(String(length=255))  # Указана длина
    material_type_id: Mapped[int] = mapped_column(ForeignKey("material_types.id"))  # Внешний ключ

    # Прямое отношение к таблице material_types
    material_type: Mapped["Material_type"] = relationship("Material_type", back_populates="titles")
    stock: Mapped["Material_stock"] = relationship("Material_stock", back_populates="material_title", uselist=False)
    user_assignments: Mapped[list["Material_user"]] = relationship("Material_user", back_populates="material_title")

    def to_dict(self):
        return {
            "id": self.id,
            "material_title": self.material_title,
            "material_type_id": self.material_type_id,
        }

    # id: Mapped[int_pk]
    # material_title: Mapped[str] = mapped_column(String(length=255))  # Указана длина
    # # Внешний ключ на таблицу users
    # materal_type_id: Mapped[int] = mapped_column(ForeignKey("material_types.id"))

    # creator = relationship(
    #     "Material_type",
    #     back_populates="mat_types",
    #     foreign_keys=[materal_type_id]
    # )

    # extend_existing = True

    # def __repr__(self):
    #     return f"{self.__class__.__name__}(id={self.id})"

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "material_title": self.material_title,
    #         "materal_type_id": self.materal_type_id,
    #     }