import uuid
from typing import List
from fastapi import Depends
from starlette.responses import JSONResponse
from cache.cache import cache
from models import schemas
from models.models import Menu
from repository.menu import MenuRepository


class MenuService:

    def __init__(self, repository: MenuRepository = Depends()):
        self.repository = repository
        self.cache = cache

    def get_all(self) -> List[schemas.AllMenu]:
        item = self.cache.cached_or_fetch('all_menus', self.repository.get_all)
        return item

    def get(self, target_menu_id: uuid.UUID) -> schemas.AllMenu:
        item = self.cache.cached_or_fetch(f'menu_{target_menu_id}', self.repository.get, target_menu_id)
        return item

    def create(self, menu: schemas.MenuBase) -> Menu:
        item = self.repository.create(menu)
        self.cache.invalidate('all_menus')
        return item

    def update(self, target_menu_id: uuid.UUID, menu_data: schemas.MenuBase) -> Menu:
        item = self.repository.update(target_menu_id, menu_data)
        self.cache.invalidate('all_menus', f'menu_{target_menu_id}')
        return item

    def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        item = self.repository.delete(target_menu_id)
        self.cache.invalidate('all_menus', f'menu_{target_menu_id}')
        return item
