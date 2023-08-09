import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.db import create_session
from models import schemas
from models.models import Dish, Menu, SubMenu


class MenuRepository:

    def __init__(self, session: AsyncSession = Depends(create_session)) -> None:
        self.session: AsyncSession = session

    async def get_all(self) -> list[schemas.AllMenu]:
        menu_query = select(Menu)
        menus = await self.session.execute(menu_query)
        menus = menus.scalars().all()

        menu_responses = []
        for menu in menus:
            submenus_count_query = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu.id)
            submenus_count = await self.session.execute(submenus_count_query)
            submenus_count = submenus_count.scalar_one()

            dishes_count_query = select(func.count(Dish.id)).where(
                Dish.submenu_id == SubMenu.id, SubMenu.menu_id == menu.id
            )
            dishes_count = await self.session.execute(dishes_count_query)
            dishes_count = dishes_count.scalar_one()

            menu_response = schemas.AllMenu(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count
            )
            menu_responses.append(menu_response)
        return menu_responses

    async def get(self, target_menu_id: uuid.UUID) -> schemas.AllMenu:

        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one_or_none()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        submenus_count_query = select(func.count(SubMenu.id)).where(SubMenu.menu_id == target_menu_id)
        submenus_count = await self.session.execute(submenus_count_query)
        submenus_count = submenus_count.scalar_one()

        dishes_count_query = select(func.count(Dish.id)).where(
            Dish.submenu_id == SubMenu.id, SubMenu.menu_id == target_menu_id
        )
        dishes_count = await self.session.execute(dishes_count_query)
        dishes_count = dishes_count.scalar_one()

        menu_response = schemas.AllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_response

    async def create(self, menu: schemas.MenuBase) -> Menu:
        new_menu = Menu(**menu.model_dump())
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        return new_menu

    async def update(self, target_menu_id: uuid.UUID, menu_data: schemas.MenuBase) -> Menu:
        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        menu.title = menu_data.title
        menu.description = menu_data.description
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        menu_title = menu.title
        await self.session.delete(menu)
        await self.session.commit()
        return JSONResponse(status_code=200, content={'message': f'Menu {menu_title} deleted successfully'})
