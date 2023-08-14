import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.db import create_session
from models.models import Dish, Menu, SubMenu
from schemas.dish_schema import DishBase, DishSchema


class DishRepository:

    def __init__(self, session: AsyncSession = Depends(create_session)) -> None:
        self.session: AsyncSession = session

    async def get_all(self, target_submenu_id: uuid.UUID) -> list[DishSchema]:
        dishes_query = select(Dish).where(Dish.submenu_id == target_submenu_id)
        result = await self.session.execute(dishes_query)
        dishes = result.scalars().all()

        dishes_response = [DishSchema(**dish.__dict__) for dish in dishes]
        return dishes_response

    async def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                  target_dish_id: uuid.UUID) -> DishSchema:
        dish_query = (
            select(Dish)
            .join(SubMenu, SubMenu.id == Dish.submenu_id)
            .where(SubMenu.menu_id == target_menu_id)
            .where(Dish.submenu_id == target_submenu_id)
            .where(Dish.id == target_dish_id)
        )
        dish = await self.session.execute(dish_query)
        dish = dish.scalar_one_or_none()

        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        dish_response = DishSchema(**dish.__dict__)
        return dish_response

    async def create(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     dish_data: DishBase) -> DishSchema:
        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one_or_none()

        submenu_query = select(SubMenu).where(SubMenu.id == target_submenu_id, SubMenu.menu_id == target_menu_id)
        submenu = await self.session.execute(submenu_query)
        submenu = submenu.scalar_one_or_none()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        new_dish = Dish(**dish_data.model_dump(), submenu_id=target_submenu_id)
        self.session.add(new_dish)
        await self.session.commit()
        await self.session.refresh(new_dish)

        dish_response = DishSchema(**new_dish.__dict__)
        return dish_response

    async def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     target_dish_id: uuid.UUID, dish_data: DishBase) -> DishSchema:
        dish_query = (
            select(Dish)
            .join(SubMenu, SubMenu.id == Dish.submenu_id)
            .where(SubMenu.menu_id == target_menu_id)
            .where(Dish.submenu_id == target_submenu_id)
            .where(Dish.id == target_dish_id)
        )
        dish = await self.session.execute(dish_query)
        dish = dish.scalar_one_or_none()

        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        for field, value in dish_data.model_dump().items():
            if field != 'id':
                setattr(dish, field, value)

        await self.session.commit()
        await self.session.refresh(dish)

        dish_response = DishSchema(**dish.__dict__)
        return dish_response

    async def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     target_dish_id: uuid.UUID) -> JSONResponse:
        dish_query = (
            select(Dish)
            .join(SubMenu, SubMenu.id == Dish.submenu_id)
            .where(SubMenu.menu_id == target_menu_id)
            .where(Dish.submenu_id == target_submenu_id)
            .where(Dish.id == target_dish_id)
        )
        dish = await self.session.execute(dish_query)
        dish = dish.scalar_one_or_none()

        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        await self.session.delete(dish)
        await self.session.commit()
        return JSONResponse(status_code=200, content={'message': f'Dish {dish.title} deleted successfully'})
