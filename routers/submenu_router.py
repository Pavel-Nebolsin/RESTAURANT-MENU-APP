import uuid
from fastapi import APIRouter
from typing import List
from models import schemas
from fastapi import status, Body, Depends
from service.submenu import SubMenuService

router = APIRouter()


# Возвращает все подменю
@router.get('/', response_model=List[schemas.AllSubmenu])
def get_submenus_handler(target_menu_id: uuid.UUID, submenu: SubMenuService = Depends()):
    return submenu.get_all(target_menu_id)


# Создаёт подменю
@router.post('/', response_model=schemas.SubMenuOut,
             status_code=status.HTTP_201_CREATED)
def create_submenu_handler(target_menu_id: uuid.UUID, submenu_data: schemas.SubMenuBase,
                           submenu: SubMenuService = Depends()):
    return submenu.create(target_menu_id, submenu_data)


# Возвращает подменю
@router.get('/{target_submenu_id}', response_model=schemas.AllSubmenu)
def get_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        submenu: SubMenuService = Depends()):
    return submenu.get(target_menu_id, target_submenu_id)


# Обновляет подменю
@router.patch('/{target_submenu_id}', response_model=schemas.SubMenuOut)
def update_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           submenu_data: schemas.SubMenuBase = Body(...),
                           submenu: SubMenuService = Depends()):
    return submenu.update(target_menu_id, target_submenu_id, submenu_data)


# Удаляет подменю
@router.delete('/{target_submenu_id}', response_model=schemas.SubMenuOut)
def delete_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           submenu: SubMenuService = Depends()):
    return submenu.delete(target_menu_id, target_submenu_id)
