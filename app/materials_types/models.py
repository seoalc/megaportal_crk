from sqlalchemy import text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk
from app.applications.models import application_remedial_users


class Material_type(Base):
    __tablename__ = "material_types"

    id: Mapped[int_pk]
    material_type: Mapped[str] = mapped_column(String(length=128), unique=True)  # Уникальное поле

    # Обратное отношение к таблице material_titles
    titles: Mapped[list["Material_title"]] = relationship("Material_title", back_populates="material_type")

    def to_dict(self):
        return {
            "id": self.id,
            "material_type": self.material_type,
        }

    # id: Mapped[int_pk]
    # material_type: Mapped[str_uniq] = mapped_column(String(length=128))  # Указана длина

    # created_applications = relationship(
    #     "Material_title",
    #     back_populates="title",
    #     foreign_keys="Material_title.materal_type_id"
    # )

    # extend_existing = True

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "material_type": self.material_type,
    #     }