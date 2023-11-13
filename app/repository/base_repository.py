from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base


class BaseRepository:
    def __init__(self: "BaseRepository", model: Base):
        self.model = model

    async def get_items(self: "BaseRepository", session: AsyncSession, query=None, offset=None, limit=None, order_by=None):
        if query is None:
            query = select(self.model)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        if order_by is not None:
            query = query.order_by(*order_by)

        return await session.execute(query)

    async def get_item(self: "BaseRepository", session: AsyncSession, obj_id: int):
        return await session.get(self.model, obj_id)

    async def create_item(self: "BaseRepository", session: AsyncSession, obj_in: BaseModel):
        result = await session.execute(
            insert(self.model).values(**obj_in.model_dump()).returning(self.model),
        )
        await session.commit()
        return result.scalar_one()

    async def update_item(self: "BaseRepository", session: AsyncSession, obj_id: int, obj_upd: BaseModel) -> Base:
        update_data = obj_upd.model_dump()
        result = await session.execute(
            update(self.model).where(self.model.id == obj_id).values(**update_data).returning(self.model),
        )
        await session.commit()
        return result.scalar_one()

    async def delete_item(self: "BaseRepository", session: AsyncSession, obj_id: int):
        result = await session.execute(delete(self.model).where(self.model.id == obj_id))
        await session.commit()
        return result
