import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from db.db import create_session
from models.models import Menu
from repositories.repository_utils import get_counts
from schemas.menu_schema import MenuBase, MenuSchema


class MenuRepository:

    def __init__(self, session: AsyncSession = Depends(create_session)) -> None:
        self.session: AsyncSession = session

    async def get_all(self) -> list[MenuSchema]:
        menu_query = select(Menu)
        menus = await self.session.execute(menu_query)
        menus = menus.scalars().all()

        menu_responses = []
        for menu in menus:
            submenus_count, dishes_count = await get_counts(self.session, menu.id)
            menu_response = MenuSchema(
                **menu.__dict__,
                submenus_count=submenus_count,
                dishes_count=dishes_count
            )
            menu_responses.append(menu_response)
        return menu_responses

    async def get(self, target_menu_id: uuid.UUID) -> MenuSchema:

        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one_or_none()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        submenus_count, dishes_count = await get_counts(self.session, menu.id)
        menu_response = MenuSchema(
            **menu.__dict__,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_response

    async def create(self, menu: MenuBase) -> MenuSchema:
        new_menu = Menu(**menu.model_dump())
        self.session.add(new_menu)
        await self.session.commit()
        await self.session.refresh(new_menu)
        menu_response = MenuSchema(**new_menu.__dict__)
        return menu_response

    async def update(self, target_menu_id: uuid.UUID, menu_data: MenuBase) -> MenuSchema:
        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        menu.title = menu_data.title
        menu.description = menu_data.description
        await self.session.commit()
        await self.session.refresh(menu)

        menu_response = MenuSchema(**menu.__dict__)
        return menu_response

    async def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        menu_query = select(Menu).where(Menu.id == target_menu_id)
        menu = await self.session.execute(menu_query)
        menu = menu.scalar_one()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        await self.session.delete(menu)
        await self.session.commit()
        return JSONResponse(status_code=200, content={'message': f'Menu {menu.title} deleted successfully'})
