import uuid

from pydantic import BaseModel


class MenuBase(BaseModel):
    id: uuid.UUID | None = None
    title: str
    description: str


class MenuSchema(MenuBase):
    id: uuid.UUID
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        from_attributes = True
