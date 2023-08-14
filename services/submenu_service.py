import uuid

from fastapi import Depends
from starlette.responses import JSONResponse

from cache.cache import Cache, cache
from repositories.submenu_repository import SubMenuRepository
from schemas.submenu_schema import SubMenuBase, SubMenuSchema


class SubMenuService:

    def __init__(self, repository: SubMenuRepository = Depends()) -> None:
        self.repository: SubMenuRepository = repository
        self.cache: Cache = cache

    async def get_all(self, target_menu_id: uuid.UUID) -> list[SubMenuSchema]:
        item = await self.cache.cached_or_fetch('all_submenus',
                                                self.repository.get_all,
                                                target_menu_id)
        return item

    async def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> SubMenuSchema:
        item = await self.cache.cached_or_fetch(f'submenu_{target_submenu_id}',
                                                self.repository.get,
                                                target_menu_id,
                                                target_submenu_id)
        return item

    async def create(self, target_menu_id: uuid.UUID, submenu: SubMenuBase) -> SubMenuSchema:
        self.cache.invalidate('all_submenus', 'all_menus', f'menu_{target_menu_id}')
        item = await self.repository.create(target_menu_id, submenu)
        return item

    async def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     submenu_data: SubMenuBase) -> SubMenuSchema:
        self.cache.invalidate('all_submenus', f'submenu_{target_submenu_id}')
        item = await self.repository.update(target_menu_id, target_submenu_id, submenu_data)
        return item

    async def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> JSONResponse:
        self.cache.invalidate('all_menus', 'all_submenus',
                              f'submenu_{target_submenu_id}',
                              f'menu_{target_menu_id}')
        item = await self.repository.delete(target_menu_id, target_submenu_id)
        return item
