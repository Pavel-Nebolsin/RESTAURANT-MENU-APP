import uuid
from fastapi import APIRouter
from typing import List
from models import schemas
from fastapi import status, Body, Depends
from starlette.responses import JSONResponse
from service.menu import MenuService

router = APIRouter()


# Возвращает все меню
@router.get('/', response_model=List[schemas.AllMenu])
def get_all_menus_handler(menu: MenuService = Depends()) -> List[schemas.AllMenu]:
    return menu.get_all()


# Возвращает меню
@router.get('/{target_menu_id}', response_model=schemas.AllMenu)
def get_menu_handler(target_menu_id: uuid.UUID, menu: MenuService = Depends()):
    return menu.get(target_menu_id)


# Создаёт меню
@router.post('/', response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu_handler(menu_data: schemas.MenuBase, menu: MenuService = Depends()):
    return menu.create(menu_data)


# Обновляет меню
@router.patch('/{target_menu_id}', response_model=schemas.MenuOut)
def update_menu_handler(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase = Body(...),
                        menu: MenuService = Depends()) -> schemas.MenuOut:
    return menu.update(target_menu_id, menu_data)


# Удаляет меню
@router.delete('/{target_menu_id}', response_model=schemas.MenuOut)
def delete_menu_handler(target_menu_id: uuid.UUID, menu: MenuService = Depends()) -> JSONResponse:
    return menu.delete(target_menu_id)
