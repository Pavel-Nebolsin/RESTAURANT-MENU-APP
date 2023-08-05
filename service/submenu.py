import uuid
from typing import List

from fastapi import Depends
from starlette.responses import JSONResponse

from models import schemas
from models.models import Menu, SubMenu
from models.schemas import SubMenuOut
from repository.submenu import SubMenuRepository


class SubMenuCache:
    # методы кеширования
    pass


class SubMenuService:
    def __init__(self, repository: SubMenuRepository = Depends()):
        self.repository = repository
        self.cache = SubMenuCache()

    def get_all(self, target_menu_id: uuid.UUID) -> List[schemas.AllSubmenu]:
        item = self.repository.get_all(target_menu_id)
        return item

    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> schemas.AllSubmenu:
        item = self.repository.get(target_menu_id, target_submenu_id)
        return item

    def create(self, target_menu_id: uuid.UUID, submenu: schemas.SubMenuBase) -> SubMenu:
        item = self.repository.create(target_menu_id, submenu)
        return item

    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               submenu_data: schemas.SubMenuBase) -> SubMenuOut:
        item = self.repository.update(target_menu_id, target_submenu_id, submenu_data, )
        return item

    def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> JSONResponse:
        item = self.repository.delete(target_menu_id, target_submenu_id)
        return item
