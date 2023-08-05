import uuid
from typing import List

from fastapi import Depends
from starlette.responses import JSONResponse

from models import schemas
from models.models import Menu, SubMenu, Dish
from models.schemas import SubMenuOut
from repository.dish import DishRepository


class DishCache:
    # методы кеширования
    pass


class DishService:

    def __init__(self, repository: DishRepository = Depends()):
        self.repository = repository
        self.cache = DishCache()

    def get_all(self, target_submenu_id: uuid.UUID) -> List[schemas.DishOut]:
        item = self.repository.get_all(target_submenu_id)
        return item

    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
            target_dish_id: uuid.UUID) -> schemas.AllDish:
        item = self.repository.get(target_menu_id, target_submenu_id, target_dish_id)
        return item

    def create(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               dish_data: schemas.DishBase) -> Dish:
        item = self.repository.create(target_menu_id, target_submenu_id, dish_data)
        return item

    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
               dish_data: schemas.DishBase) -> schemas.DishOut:
        item = self.repository.update(target_menu_id, target_submenu_id, target_dish_id, dish_data)
        return item

    def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               target_dish_id: uuid.UUID) -> JSONResponse:
        item = self.repository.delete(target_menu_id, target_submenu_id, target_dish_id)
        return item
