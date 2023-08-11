import uuid

from fastapi import Depends
from starlette.responses import JSONResponse

from cache.cache import Cache, cache
from repositories.dish_repository import DishRepository
from schemas.dish_schema import DishBase, DishSchema


class DishService:

    def __init__(self, repository: DishRepository = Depends()) -> None:
        self.repository: DishRepository = repository
        self.cache: Cache = cache

    async def get_all(self, target_submenu_id: uuid.UUID) -> list[DishSchema]:
        item = await self.cache.cached_or_fetch('all_dishes',
                                                self.repository.get_all,
                                                target_submenu_id)
        return item

    async def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                  target_dish_id: uuid.UUID) -> DishSchema:
        item = await self.cache.cached_or_fetch(f'dish_{target_dish_id}',
                                                self.repository.get,
                                                target_menu_id,
                                                target_submenu_id,
                                                target_dish_id)
        return item

    async def create(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     dish_data: DishBase) -> DishSchema:
        item = await self.repository.create(target_menu_id,
                                            target_submenu_id,
                                            dish_data)
        await self.cache.invalidate('all_dishes', 'all_submenus', 'all_menus',
                                    f'menu_{target_menu_id}',
                                    f'submenu_{target_submenu_id}')
        return item

    async def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                     dish_data: DishBase) -> DishSchema:
        item = await self.repository.update(target_menu_id,
                                            target_submenu_id,
                                            target_dish_id,
                                            dish_data)
        await self.cache.invalidate('all_dishes', f'dish_{target_dish_id}')
        return item

    async def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     target_dish_id: uuid.UUID) -> JSONResponse:
        item = await self.repository.delete(target_menu_id, target_submenu_id, target_dish_id)
        await self.cache.invalidate('all_dishes', 'all_submenus', 'all_menus',
                                    f'dish_{target_dish_id}',
                                    f'menu_{target_menu_id}',
                                    f'submenu_{target_submenu_id}')
        return item
