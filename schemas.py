# Pydantic
import uuid

from pydantic import BaseModel, validator, field_validator, root_validator
from typing import List, Optional


###  MENU SCHEMA ###
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
    submenus_count: Optional[int]
    dishes_count: Optional[int]

    class Config:
        from_attributes = True


###  SUBMENU SCHEMA ###

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
    dishes_count: Optional[int]

    class Config:
        from_attributes = True


###  DISH SCHEMA ###

class DishBase(BaseModel):
    title: str
    description: str
    price: float

    @field_validator('price')
    def format_price(cls, value):
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
