from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.db.base import Base


class BaseRepository:
    def __init__(self: "BaseRepository", model: Base, session: Session):
        self.model = model
        self.session = session

    async def get_items(self: "BaseRepository", query=None, offset=None, limit=None, order_by=None):
        if query is None:
            query = select(self.model)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        if order_by is not None:
            query = query.order_by(*order_by)

        return self.session.execute(query)

    async def get_item(self: "BaseRepository", obj_id: int):
        return self.session.get(self.model, obj_id)

    async def create_item(self: "BaseRepository", obj_in: BaseModel):
        result = self.session.execute(
            insert(self.model).values(**obj_in.model_dump()).returning(self.model),
        )
        self.session.commit()
        return result.scalar_one()

    async def update_item(self: "BaseRepository", obj_id: int, obj_upd: BaseModel) -> Base:
        update_data = obj_upd.model_dump()
        result = self.session.execute(
            update(self.model).where(self.model.id == obj_id).values(**update_data).returning(self.model),
        )
        self.session.commit()
        return result.scalar_one()

    async def delete_item(self: "BaseRepository", obj_id: int):
        result = self.session.execute(delete(self.model).where(self.model.id == obj_id))
        self.session.commit()
        return result
