from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import User
from app.material_users.models import Material_user
from app.utils.logging_config import logger

 
class MaterialuserDAO(BaseDAO):
    model = Material_user

    @classmethod
    async def get_materials_user_qantity_by_user_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_material_to_user(cls, material_title_id: int, user_id: int, quantity: int):
        logger.info(f"Наименование материала из DAO: {material_title_id}")
        async with async_session_maker() as session:
            async with session.begin():
                # Проверяем уникальность
                existing_material = await cls.find_one_or_none(material_title_id=material_title_id, user_id=user_id)
                logger.info(f"Дебаггинг проверка в DAO: {existing_material}")
                if existing_material:
                    # Если запись существует, обновляем количество
                    new_quantity = existing_material.quantity + quantity
                    query = (
                        update(cls.model)
                        .where(cls.model.material_title_id == material_title_id, cls.model.user_id == user_id)
                        .values(quantity=new_quantity)
                    )
                    await session.execute(query)
                    await session.commit()  # Фиксируем изменения
                    logger.info(f"Количество материала обновлено: material_title_id={material_title_id}, user_id={user_id}, новое количество={new_quantity}")
                    
                    # Обновляем объект для возврата
                    existing_material.quantity = new_quantity
                    return existing_material
                else:
                    # Если записи нет, создаём новую
                    new_material_quantity = cls.model(
                        material_title_id=material_title_id,
                        user_id=user_id,  # Исправлено: используем user_id, а не material_title_id
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