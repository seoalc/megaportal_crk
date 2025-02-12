
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime, date
from app.dao.base import BaseDAO
from app.applications.models import Application
from app.database import async_session_maker

 
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
            query = select(cls.model).filter(cls.model.application_status == 1)
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