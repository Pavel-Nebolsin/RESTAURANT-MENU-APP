import uuid

from fastapi import Depends
from starlette.responses import JSONResponse

from cache.cache import Cache, cache
from models import schemas
from models.models import Dish
from repository.dish_repository import DishRepository


class DishService:

    def __init__(self, repository: DishRepository = Depends()) -> None:
        self.repository: DishRepository = repository
        self.cache: Cache = cache

    def get_all(self, target_submenu_id: uuid.UUID) -> list[schemas.DishOut]:
        item = self.cache.cached_or_fetch('all_dishes',
                                          self.repository.get_all,
                                          target_submenu_id)
        return item

    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
            target_dish_id: uuid.UUID) -> schemas.AllDish:
        item = self.cache.cached_or_fetch(f'dish_{target_dish_id}',
                                          self.repository.get,
                                          target_menu_id,
                                          target_submenu_id,
                                          target_dish_id)
        return item

    def create(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               dish_data: schemas.DishBase) -> Dish:
        item = self.repository.create(target_menu_id,
                                      target_submenu_id,
                                      dish_data)
        self.cache.invalidate('all_dishes')
        return item

    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
               dish_data: schemas.DishBase) -> schemas.DishOut:
        item = self.repository.update(target_menu_id,
                                      target_submenu_id,
                                      target_dish_id,
                                      dish_data)
        self.cache.invalidate('all_dishes', f'dish_{target_dish_id}')
        return item

    def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               target_dish_id: uuid.UUID) -> JSONResponse:
        item = self.repository.delete(target_menu_id, target_submenu_id, target_dish_id)
        self.cache.invalidate('all_dishes', 'all_submenus', 'all_menus',
                              f'dish_{target_dish_id}',
                              f'menu_{target_menu_id}',
                              f'submenu_{target_submenu_id}')
        return item
