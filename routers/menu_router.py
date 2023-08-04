import uuid
from fastapi import APIRouter
from typing import List
from models import schemas
from crud import menu_crud, submenu_crud
from fastapi import status, Body, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from db import create_session

router = APIRouter()

# Возвращает все меню
@router.get('/', response_model=List[schemas.AllMenu])
def get_all_menus(session: Session = Depends(create_session)) -> List[schemas.AllMenu]:
    return menu_crud.get_menus_with_counts(session)


# Создаёт меню
@router.post('/', response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuBase, session: Session = Depends(create_session)):
    return menu_crud.create_menu(menu, session)


# Возвращает меню
@router.get('/{target_menu_id}', response_model=schemas.AllMenu)
def get_menu(target_menu_id: uuid.UUID, session: Session = Depends(create_session)):
    return menu_crud.get_menu_with_counts(target_menu_id, session)


# Обновляет меню
@router.patch('/{target_menu_id}', response_model=schemas.MenuOut)
def update_menu(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase = Body(...),
                session: Session = Depends(create_session)) -> schemas.MenuOut:
    return menu_crud.update_menu(target_menu_id, menu_data, session)


# Удаляет меню
@router.delete('/{target_menu_id}', response_model=schemas.MenuOut)
def delete_menu(target_menu_id: uuid.UUID, session: Session = Depends(create_session)) -> JSONResponse:
    return menu_crud.delete_menu(target_menu_id, session)


