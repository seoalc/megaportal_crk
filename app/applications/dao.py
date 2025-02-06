
from sqlalchemy.future import select
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