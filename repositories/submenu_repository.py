import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.db import create_session
from models import schemas
from models.models import Dish, Menu, SubMenu


class SubMenuRepository:

    def __init__(self, session: AsyncSession = Depends(create_session)) -> None:
        self.session: AsyncSession = session

    async def get_all(self, target_menu_id: uuid.UUID) -> list[schemas.AllSubmenu]:
        submenus_query = select(SubMenu).where(SubMenu.menu_id == target_menu_id)
        submenus = await self.session.execute(submenus_query)
        submenus = submenus.scalars().all()

        submenu_responses = []

        for submenu in submenus:
            dishes_count_query = select(func.count(Dish.id)).where(Dish.submenu_id == submenu.id)
            dishes_count = await self.session.execute(dishes_count_query)
            dishes_count = dishes_count.scalar_one()

            submenu_response = schemas.AllSubmenu(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=dishes_count
            )

            submenu_responses.append(submenu_response)

        return submenu_responses

    async def create(self, target_menu_id: uuid.UUID, submenu_data: schemas.SubMenuBase) -> SubMenu:
        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        new_submenu = SubMenu(**submenu_data.model_dump(), menu_id=target_menu_id)
        self.session.add(new_submenu)
        await self.session.commit()
        await self.session.refresh(new_submenu)
        return new_submenu

    async def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> schemas.AllSubmenu:
        submenu_query = select(SubMenu).where(SubMenu.id == target_submenu_id, SubMenu.menu_id == target_menu_id)
        submenu = await self.session.execute(submenu_query)
        submenu = submenu.scalar_one_or_none()

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        dishes_count_query = select(func.count(Dish.id)).where(Dish.submenu_id == target_submenu_id)
        dishes_count = await self.session.execute(dishes_count_query)
        dishes_count = dishes_count.scalar_one()

        submenu_response = schemas.AllSubmenu(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            menu_id=submenu.menu_id,
            dishes_count=dishes_count
        )

        return submenu_response

    async def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     submenu_data: schemas.SubMenuBase) -> schemas.SubMenuOut:
        submenu_query = select(SubMenu).where(SubMenu.id == target_submenu_id, SubMenu.menu_id == target_menu_id)
        submenu = await self.session.execute(submenu_query)
        submenu = submenu.scalar_one()

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        submenu.title = submenu_data.title
        submenu.description = submenu_data.description
        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> JSONResponse:
        submenu_query = select(SubMenu).where(SubMenu.id == target_submenu_id, SubMenu.menu_id == target_menu_id)
        submenu = await self.session.execute(submenu_query)
        submenu = submenu.scalar_one()

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        await self.session.delete(submenu)
        await self.session.commit()

        return JSONResponse(status_code=200,
                            content={'message': f'Submenu {submenu.title} deleted successfully'})
