import uuid

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from models import schemas
from models.models import SubMenu
from services.submenu_service import SubMenuService

router = APIRouter()


@router.get('/', response_model=list[schemas.AllSubmenu],
            status_code=status.HTTP_200_OK,
            summary='Возвращает список подменю')
async def get_submenus_handler(target_menu_id: uuid.UUID,
                               submenu: SubMenuService = Depends()) -> list[schemas.AllSubmenu]:
    return await submenu.get_all(target_menu_id)


@router.get('/{target_submenu_id}', response_model=schemas.AllSubmenu,
            status_code=status.HTTP_200_OK,
            summary='Возвращает определённое подменю')
async def get_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                              submenu: SubMenuService = Depends()) -> schemas.AllSubmenu:
    return await submenu.get(target_menu_id, target_submenu_id)


@router.post('/', response_model=schemas.SubMenuOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создаёт подменю')
async def create_submenu_handler(target_menu_id: uuid.UUID, submenu_data: schemas.SubMenuBase,
                                 submenu: SubMenuService = Depends()) -> SubMenu:
    return await submenu.create(target_menu_id, submenu_data)


@router.patch('/{target_submenu_id}', response_model=schemas.SubMenuOut,
              status_code=status.HTTP_200_OK,
              summary='Обновляет подменю')
async def update_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                                 submenu_data: schemas.SubMenuBase = Body(...),
                                 submenu: SubMenuService = Depends()) -> schemas.SubMenuOut:
    return await submenu.update(target_menu_id, target_submenu_id, submenu_data)


@router.delete('/{target_submenu_id}',
               status_code=status.HTTP_200_OK,
               summary='Удаляет подменю')
async def delete_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                                 submenu: SubMenuService = Depends()) -> JSONResponse:
    return await submenu.delete(target_menu_id, target_submenu_id)
