import uuid

from pydantic import BaseModel


class SubMenuBase(BaseModel):
    id: uuid.UUID | None = None
    title: str
    description: str


class SubMenuSchema(SubMenuBase):
    id: uuid.UUID
    dishes_count: int = 0

    class Config:
        from_attributes = True
