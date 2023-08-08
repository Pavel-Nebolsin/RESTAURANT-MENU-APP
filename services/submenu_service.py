import uuid

from fastapi import Depends
from starlette.responses import JSONResponse

from cache.cache import Cache, cache
from models import schemas
from models.models import SubMenu
from models.schemas import SubMenuOut
from repositories.submenu_repository import SubMenuRepository


class SubMenuService:

    def __init__(self, repository: SubMenuRepository = Depends()) -> None:
        self.repository: SubMenuRepository = repository
        self.cache: Cache = cache

    def get_all(self, target_menu_id: uuid.UUID) -> list[schemas.AllSubmenu]:
        item = self.cache.cached_or_fetch('all_submenus',
                                          self.repository.get_all,
                                          target_menu_id)
        return item

    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> schemas.AllSubmenu:
        item = self.cache.cached_or_fetch(f'submenu_{target_submenu_id}',
                                          self.repository.get,
                                          target_menu_id,
                                          target_submenu_id)
        return item

    def create(self, target_menu_id: uuid.UUID, submenu: schemas.SubMenuBase) -> SubMenu:
        item = self.repository.create(target_menu_id, submenu)
        self.cache.invalidate('all_submenus', 'all_menus', f'menu_{target_menu_id}')
        return item

    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               submenu_data: schemas.SubMenuBase) -> SubMenuOut:
        item = self.repository.update(target_menu_id, target_submenu_id, submenu_data)
        self.cache.invalidate('all_submenus', f'submenu_{target_submenu_id}')
        return item

    def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> JSONResponse:
        item = self.repository.delete(target_menu_id, target_submenu_id)
        self.cache.invalidate('all_submenus', 'all_menus', f'submenu_{target_submenu_id}', f'menu_{target_menu_id}')
        return item
