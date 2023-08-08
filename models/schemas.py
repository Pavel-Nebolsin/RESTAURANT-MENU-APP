import uuid
from typing import Any

from pydantic import BaseModel, field_validator


# MENU SCHEMAS
class MenuBase(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class MenuOut(MenuBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class AllMenu(MenuBase):
    id: uuid.UUID
    submenus_count: int | None
    dishes_count: int | None

    class Config:
        from_attributes = True


# SUBMENU SCHEMAS

class SubMenuBase(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class SubMenuOut(SubMenuBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class AllSubmenu(SubMenuBase):
    id: uuid.UUID
    dishes_count: int | None

    class Config:
        from_attributes = True


# DISH SCHEMAS

class DishBase(BaseModel):
    title: str
    description: str
    price: float

    @field_validator('price')
    def format_price(cls, value: Any) -> str:
        return str(value)

    class Config:
        from_attributes = True


class DishOut(DishBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class AllDish(DishBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
