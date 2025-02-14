
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.dao.base import BaseDAO
from app.applications.models import Application
from app.database import async_session_maker
from app.users.models import User

 
class ApplicationDAO(BaseDAO):
    model = Application

    @classmethod
    async def get_unassigned_applications(cls):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.application_status == 0)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_assigned_applications(cls):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.application_status == 1).options(selectinload(cls.model.remedial_users))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_applications_by_subscriber_number(cls, subscriber_number: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.subscriber_number == subscriber_number)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_application(cls, **application_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_application = Application(**application_data)
                session.add(new_application)
                await session.flush()
                new_application_id = new_application.id
                await session.commit()
                return new_application_id

    @classmethod
    async def update_remedial_user(cls, application_id: int, application_status: int, remedial_user_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == application_id)
                    .values(application_status=application_status, remedial_user_id=remedial_user_id)
                )
                await session.execute(query)
                await session.commit()

    @classmethod
    async def add_remedial_users(cls, application_id: int, user_ids: list[int]):
        """ Добавляет исполнителей к заявке (можно передавать несколько ID). """
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    # Получаем объект заявки
                    query = select(Application).filter(Application.id == application_id)
                    result = await session.execute(query)
                    application = result.scalar_one_or_none()
                    
                    if not application:
                        return 0  # Если заявка не найдена

                    # 🔥 Явно загружаем связанных исполнителей перед изменением
                    await session.refresh(application, ["remedial_users"])

                    # Добавляем новых исполнителей (если их еще нет)
                    for user_id in user_ids:
                        if user_id not in [u.id for u in application.remedial_users]:
                            application.remedial_users.append(await session.get(User, user_id))

                    await session.commit()
                    return len(application.remedial_users)  # Количество исполнителей
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    @classmethod
    async def update_application_status(cls, application_id: int, application_status: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == application_id)
                    .values(application_status=application_status)
                )
                await session.execute(query)
                await session.commit()

    @classmethod
    async def update_complaint_text(cls, application_id: int, complaint_text: str):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == application_id)
                    .values(complaint_text=complaint_text)
                )
                await session.execute(query)
                await session.commit()

    @classmethod
    async def update_appearance_date(cls, application_id: int, appearance_date: date):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    update(cls.model)
                    .where(cls.model.id == application_id)
                    .values(appearance_date=appearance_date)
                )
                await session.execute(query)
                await session.commit()

    @classmethod
    async def delete_application(cls, application_id: int) -> int:
        return await cls.delete(id=application_id)  # Исполь