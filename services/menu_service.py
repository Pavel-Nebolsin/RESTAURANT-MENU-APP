import uuid

from fastapi import Depends
from starlette.responses import JSONResponse

from cache.cache import Cache, cache
from repositories.menu_repository import MenuRepository
from schemas.menu_schema import MenuBase, MenuSchema


class MenuService:

    def __init__(self, repository: MenuRepository = Depends()) -> None:
        self.repository: MenuRepository = repository
        self.cache: Cache = cache

    async def get_all(self) -> list[MenuSchema]:
        item = await self.cache.cached_or_fetch('all_menus', self.repository.get_all)
        return item

    async def get(self, target_menu_id: uuid.UUID) -> MenuSchema:
        item = await self.cache.cached_or_fetch(f'menu_{target_menu_id}', self.repository.get, target_menu_id)
        return item

    async def create(self, menu: MenuBase) -> MenuSchema:
        await self.cache.invalidate('all_menus')
        item = await self.repository.create(menu)
        return item

    async def update(self, target_menu_id: uuid.UUID, menu_data: MenuBase) -> MenuSchema:
        await self.cache.invalidate('all_menus', f'menu_{target_menu_id}')
        item = await self.repository.update(target_menu_id, menu_data)
        return item

    async def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        await self.cache.invalidate('all_menus', f'menu_{target_menu_id}')
        item = await self.repository.delete(target_menu_id)
        return item

    async def all_menus_with_content(self):
        item = await self.repository.all_menus_with_content()
        return item
