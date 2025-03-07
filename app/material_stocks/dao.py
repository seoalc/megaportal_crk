from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.dao.base import BaseDAO
from app.material_stocks.models import Material_stock
from app.database import async_session_maker
from app.users.models import User
from app.utils.logging_config import logger

 
class MaterialstocksDAO(BaseDAO):
    model = Material_stock

    @classmethod
    async def get_materials_quantity_by_id(cls, material_title_id: int):
        logger.info(f"ID материала из DAO: {material_title_id}")
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.material_title_id == material_title_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_material_to_stock(cls, material_title_id: int, quantity: int):
        logger.info(f"Наименование материала из DAO: {material_title_id}")
        async with async_session_maker() as session:
            async with session.begin():
                # Проверяем уникальность
                existing_material = await cls.find_one_or_none(material_title_id=material_title_id)
                logger.info(f"Дебаггинг проверка в DAO: {existing_material}")
                if existing_material:
                    # Если запись существует, обновляем количество
                    new_quantity = existing_material.quantity + quantity
                    query = (
                        update(cls.model)
                        .where(cls.model.material_title_id == material_title_id)
                        .values(quantity=new_quantity)
                    )
                    await session.execute(query)
                    logger.info(f"Количество материала обновлено: {material_title_id} (ID: {existing_material.id})")
                    return existing_material
                else:
                # Создаём новый экземпляр Material_title
                    new_material_quantity = cls.model(
                        material_title_id=material_title_id,
                        quantity=quantity
                    )
                    session.add(new_material_quantity)
                    try:
                        await session.commit()
                        logger.info(f"Успешно добавлено количество: {material_title_id} (ID: {new_material_quantity.id})")
                        return new_material_quantity
                    except SQLAlchemyError as e:
                        await session.rollback()
                        logger.error(f"Ошибка при добавлении наименования материала: {str(e)}")
                        raise e

    # Новый метод для уменьшения количества
    @classmethod
    async def decrease_quantity(cls, material_title_id: int, quantity: int):
        logger.info(f"Уменьшение количества материала: material_title_id={material_title_id}, quantity={quantity}")
        async with async_session_maker() as session:
            async with session.begin():
                existing_material = await cls.find_one_or_none(material_title_id=material_title_id)
                if not existing_material:
                    raise ValueError("Материал не найден на складе")
                if existing_material.quantity < quantity:
                    raise ValueError("Недостаточно материала на складе")
                
                new_quantity = existing_material.quantity - quantity
                query = (
                    update(cls.model)
                    .where(cls.model.material_title_id == material_title_id)
                    .values(quantity=new_quantity)
                )
                await session.execute(query)
                await session.commit()
                logger.info(f"Количество материала уменьшено: material_title_id={material_title_id}, новое количество={new_quantity}")
                existing_material.quantity = new_quantity
                return existing_material