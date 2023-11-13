from pydantic import BaseModel


class TestCreateSchema(BaseModel):
    name: str
