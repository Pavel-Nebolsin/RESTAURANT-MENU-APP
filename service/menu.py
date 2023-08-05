import uuid
from typing import List

from fastapi import Depends
from starlette.responses import JSONResponse

from models import schemas
from models.models import Menu
from repository.menu import MenuRepository


class MenuCache:
    # методы кеширования
    pass


class MenuService:

    def __init__(self, repository: MenuRepository = Depends()):
        self.repository = repository
        self.cache = MenuCache()

    def get_all(self) -> List[schemas.AllMenu]:
        item = self.repository.get_all()
        return item

    def get(self, target_menu_id: uuid.UUID) -> schemas.AllMenu:
        item = self.repository.get(target_menu_id)
        return item

    def create(self, menu: schemas.MenuBase) -> Menu:
        item = self.repository.create(menu)
        return item

    def update(self, target_menu_id: uuid.UUID, menu_data: schemas.MenuBase) -> Menu:
        item = self.repository.update(target_menu_id, menu_data)
        return item

    def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        item = self.repository.delete(target_menu_id)
        return item
