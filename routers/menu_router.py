import uuid

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from models import schemas
from models.models import Menu
from services.menu_service import MenuService

router = APIRouter()


@router.get('/', response_model=list[schemas.AllMenu],
            status_code=status.HTTP_200_OK,
            summary='Возвращает список меню')
async def get_all_menus_handler(menu: MenuService = Depends()) -> list[schemas.AllMenu]:
    return await menu.get_all()


@router.get('/{target_menu_id}', response_model=schemas.AllMenu,
            status_code=status.HTTP_200_OK,
            summary='Возвращает определённое меню')
async def get_menu_handler(target_menu_id: uuid.UUID,
                           menu: MenuService = Depends()) -> schemas.AllMenu:
    return await menu.get(target_menu_id)


@router.post('/', response_model=schemas.MenuOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создаёт меню')
async def create_menu_handler(menu_data: schemas.MenuBase,
                              menu: MenuService = Depends()) -> Menu:
    return await menu.create(menu_data)


@router.patch('/{target_menu_id}', response_model=schemas.MenuOut,
              status_code=status.HTTP_200_OK,
              summary='Обновляет меню')
async def update_menu_handler(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase = Body(...),
                              menu: MenuService = Depends()) -> Menu:
    return await menu.update(target_menu_id, menu_data)


@router.delete('/{target_menu_id}',
               status_code=status.HTTP_200_OK,
               summary='Удаляет меню')
async def delete_menu_handler(target_menu_id: uuid.UUID,
                              menu: MenuService = Depends()) -> JSONResponse:
    return await menu.delete(target_menu_id)
