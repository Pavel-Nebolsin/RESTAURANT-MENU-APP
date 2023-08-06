import uuid

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from models import schemas
from services.menu_service import MenuService

router = APIRouter()


@router.get('/', response_model=list[schemas.AllMenu],
            status_code=status.HTTP_200_OK,
            summary='Возвращает список меню')
def get_all_menus_handler(menu: MenuService = Depends()) -> list[schemas.AllMenu]:
    return menu.get_all()


@router.get('/{target_menu_id}', response_model=schemas.AllMenu,
            status_code=status.HTTP_200_OK,
            summary='Возвращает определённое меню')
def get_menu_handler(target_menu_id: uuid.UUID, menu: MenuService = Depends()):
    return menu.get(target_menu_id)


@router.post('/', response_model=schemas.MenuOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создаёт меню')
def create_menu_handler(menu_data: schemas.MenuBase, menu: MenuService = Depends()):
    return menu.create(menu_data)


@router.patch('/{target_menu_id}', response_model=schemas.MenuOut,
              status_code=status.HTTP_200_OK,
              summary='Обновляет меню')
def update_menu_handler(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase = Body(...),
                        menu: MenuService = Depends()) -> schemas.MenuOut:
    return menu.update(target_menu_id, menu_data)


@router.delete('/{target_menu_id}', response_model=schemas.MenuOut,
               status_code=status.HTTP_200_OK,
               summary='Удаляет меню')
def delete_menu_handler(target_menu_id: uuid.UUID, menu: MenuService = Depends()) -> JSONResponse:
    return menu.delete(target_menu_id)
