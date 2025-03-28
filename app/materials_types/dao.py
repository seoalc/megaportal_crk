
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.dao.base import BaseDAO
from app.materials_types.models import Material_type
from app.database import async_session_maker
from app.users.models import User
from app.utils.logging_config import logger

 
class MaterialtypeDAO(BaseDAO):
    model = Material_type

    @classmethod
    async def get_material_type_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_material_type(cls, material_type: str):
        logger.info(f"Тип материала из DAO: {material_type}")
        async with async_session_maker() as session:
            async with session.begin():
                # Проверяем уникальность
                existing_type = await cls.find_one_or_none(material_type=material_type)
                if existing_type:
                    raise ValueError(f"Тип материала '{material_type}' уже существует")
                # Создаём новый экземпляр Material_type
                new_material_type = cls.model(material_type=material_type)
                session.add(new_material_type)
                try:
                    await session.commit()
                    return new_material_type  # Возвращаем созданный объект
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e