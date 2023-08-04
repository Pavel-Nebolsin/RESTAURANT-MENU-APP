import uuid
from fastapi import APIRouter
from typing import List
from models import schemas
from crud import submenu_crud
from fastapi import status, Body, Depends
from sqlalchemy.orm import Session
from db import create_session

router = APIRouter()

# Возвращает все подменю
@router.get('/', response_model=List[schemas.AllSubmenu])
def get_submenus(target_menu_id: uuid.UUID, session: Session = Depends(create_session)):
    return submenu_crud.get_submenus_for_menu(target_menu_id, session)

# Создаёт подменю
@router.post('/', response_model=schemas.SubMenuOut,
          status_code=status.HTTP_201_CREATED)
def create_submenu(target_menu_id: uuid.UUID, submenu: schemas.SubMenuBase,
                   session: Session = Depends(create_session)):
    return submenu_crud.create_submenu(target_menu_id, submenu, session)
# Возвращает подменю
@router.get('/{target_submenu_id}', response_model=schemas.AllSubmenu)
def get_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        session: Session = Depends(create_session)):
    return submenu_crud.get_submenu(target_menu_id, target_submenu_id, session)

# Обновляет подменю
@router.patch('/{target_submenu_id}', response_model=schemas.SubMenuOut)
def update_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           submenu_data: schemas.SubMenuBase = Body(...),
                           session: Session = Depends(create_session)):
    return submenu_crud.update_submenu(target_menu_id, target_submenu_id, submenu_data, session)

# Удаляет подменю
@router.delete('/{target_submenu_id}', response_model=schemas.SubMenuOut)
def delete_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           session: Session = Depends(create_session)):
    return submenu_crud.delete_submenu(target_menu_id, target_submenu_id, session)