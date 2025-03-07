from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk


class Material_user(Base):
    __tablename__ = "material_user"

    id: Mapped[int_pk]
    material_title_id: Mapped[int] = mapped_column(ForeignKey("material_titles.id"))  # Внешний ключ
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # Внешний ключ
    quantity: Mapped[int]  # Количество на руках

    # Прямое отношение к таблице material_titles
    material_title: Mapped["Material_title"] = relationship(
                                                "Material_title", 
                                                back_populates="user_assignments",
                                                lazy="noload"
                                            )

    # Прямое отношение к таблице users
    user: Mapped["User"] = relationship("User", back_populates="material_assignments")

    def to_dict(self):
        return {
            "id": self.id,
            "material_title_id": self.material_title_id,
            "user_id": self.user_id,
            "quantity": self.quantity,
        }