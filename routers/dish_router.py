import uuid
from fastapi import APIRouter
from typing import List
from models import schemas
from crud import dish_crud
from fastapi import status, Body, Depends
from sqlalchemy.orm import Session
from db import create_session

router = APIRouter()

# Возвращает все блюда
@router.get('/', response_model=List[schemas.DishOut])
def get_all_dishes_handler(target_submenu_id: uuid.UUID, session: Session = Depends(create_session)):
    return dish_crud.get_all_dishes(target_submenu_id, session)


# Создаёт блюдо
@router.post('/',
          response_model=schemas.DishOut, status_code=status.HTTP_201_CREATED)
def create_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        dish_data: schemas.DishBase, session: Session = Depends(create_session)):
    return dish_crud.create_dish(target_menu_id, target_submenu_id, dish_data, session)


# Возвращает блюдо
@router.get('/{target_dish_id}',
         response_model=schemas.DishOut)
def get_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                     session: Session = Depends(create_session)):
    return dish_crud.get_dish(target_menu_id, target_submenu_id, target_dish_id, session)


# Обновляет блюдо
@router.patch('/{target_dish_id}',
           response_model=schemas.DishOut)
def update_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        dish_data: schemas.DishBase = Body(...), session: Session = Depends(create_session)):
    return dish_crud.update_dish(target_menu_id, target_submenu_id, target_dish_id, dish_data, session)


# Удаляет блюдо
@router.delete('/{target_dish_id}',
            response_model=schemas.DishOut)
def delete_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        session: Session = Depends(create_session)):
    return dish_crud.delete_dish(target_menu_id, target_submenu_id, target_dish_id, session)