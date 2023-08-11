import uuid

from pydantic import BaseModel, field_validator


class DishBase(BaseModel):
    title: str
    description: str
    price: float

    @field_validator('price')
    def format_price(cls, value: float) -> str:
        return str(value)


class DishSchema(DishBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
