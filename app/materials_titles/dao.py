from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.dao.base import BaseDAO
from app.materials_titles.models import Material_title
from app.database import async_session_maker
from app.users.models import User
from app.utils.logging_config import logger

 
class MaterialtitleDAO(BaseDAO):
    model = Material_title

    @classmethod
    async def get_material_title_by_id(cls, id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_materials_titles_by_type(cls, material_type_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.material_type_id == material_type_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_material_title(cls, material_type_id: int, material_title: str):
        logger.info(f"Тип материала из DAO: {material_type_id}")
        async with async_session_maker() as session:
            async with session.begin():
                # Проверяем уникальность
                existing_title = await cls.find_one_or_none(material_title=material_title)
                if existing_title:
                    raise ValueError(f"Наименование материала '{material_title}' уже существует")
               # Создаём новый экземпляр Material_title
                new_material_title = cls.model(
                    material_type_id=material_type_id,
                    material_title=material_title
                )
                session.add(new_material_title)
                try:
                    await session.commit()
                    logger.info(f"Успешно добавлено наименование: {material_title} (ID: {new_material_title.id})")
                    return new_material_title
                except SQLAlchemyError as e:
                    await session.rollback()
                    logger.error(f"Ошибка при добавлении наименования материала: {str(e)}")
                    raise e