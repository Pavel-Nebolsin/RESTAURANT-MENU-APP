import uuid

from fastapi import APIRouter, Body, Depends, status

from models import schemas
from services.submenu_service import SubMenuService

router = APIRouter()


@router.get('/', response_model=list[schemas.AllSubmenu],
            status_code=status.HTTP_200_OK,
            summary='Возвращает список подменю')
def get_submenus_handler(target_menu_id: uuid.UUID, submenu: SubMenuService = Depends()):
    return submenu.get_all(target_menu_id)


@router.get('/{target_submenu_id}', response_model=schemas.AllSubmenu,
            status_code=status.HTTP_200_OK,
            summary='Возвращает определённое подменю')
def get_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        submenu: SubMenuService = Depends()):
    return submenu.get(target_menu_id, target_submenu_id)


@router.post('/', response_model=schemas.SubMenuOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создаёт подменю')
def create_submenu_handler(target_menu_id: uuid.UUID, submenu_data: schemas.SubMenuBase,
                           submenu: SubMenuService = Depends()):
    return submenu.create(target_menu_id, submenu_data)


@router.patch('/{target_submenu_id}', response_model=schemas.SubMenuOut,
              status_code=status.HTTP_200_OK,
              summary='Обновляет подменю')
def update_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           submenu_data: schemas.SubMenuBase = Body(...),
                           submenu: SubMenuService = Depends()):
    return submenu.update(target_menu_id, target_submenu_id, submenu_data)


@router.delete('/{target_submenu_id}', response_model=schemas.SubMenuOut,
               status_code=status.HTTP_200_OK,
               summary='Удаляет подменю')
def delete_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           submenu: SubMenuService = Depends()):
    return submenu.delete(target_menu_id, target_submenu_id)
