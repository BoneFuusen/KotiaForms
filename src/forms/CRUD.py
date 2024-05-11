from fastapi import HTTPException

from src.forms.form_models import Form
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select


class CRUD:
    async def get_all(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            statement = select(Form).order_by(Form.id)

            result = await session.execute(statement)

            return result.scalars()

    async def add(self, async_session: async_sessionmaker[AsyncSession], form: Form):
        async with async_session() as session:
            session.add(form)
            await session.commit()

        return form

    async def get_by_id(self, async_session: async_sessionmaker[AsyncSession], form_id: int):
        async with async_session() as session:
            statement = select(Form).filter(Form.id == form_id)

            result = await session.execute(statement)

            return result.scalars().one()

    async def update(self, async_session: async_sessionmaker[AsyncSession], form_id, data, user_id):
        async with async_session() as session:
            statement = select(Form).filter(Form.id == form_id)

            result = await session.execute(statement)

            form = result.scalars().one()

            if user_id != form.user_id:
                raise HTTPException(status_code=403, detail="You are not this form's creator. Update request denied.")
            else:
                form.form_name = data["form_name"]
                form.questions = data["questions"]

                await session.commit()

                return form

    async def delete(self, async_session: async_sessionmaker[AsyncSession], form: Form, user_id):
        async with async_session() as session:
            if user_id != form.user_id:
                raise HTTPException(status_code=403, detail="You are not this form's creator. Delete request denied.")
            else:
                await session.delete(form)
                await session.commit()

                return {}
