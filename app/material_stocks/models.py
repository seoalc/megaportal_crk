from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class Material_stock(Base):
    __tablename__ = "material_stock"

    id: Mapped[int_pk]
    material_title_id: Mapped[int] = mapped_column(ForeignKey("material_titles.id"))  # Внешний ключ
    quantity: Mapped[int]  # Количество на складе

    # Прямое отношение к таблице material_titles
    material_title: Mapped["Material_title"] = relationship("Material_title", back_populates="stock")

    def to_dict(self):
        return {
            "id": self.id,
            "material_title_id": self.material_title_id,
            "quantity": self.quantity,
        }