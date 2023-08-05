import uuid
from fastapi import APIRouter
from typing import List
from models import schemas
from fastapi import status, Body, Depends
from service.dish import DishService

router = APIRouter()


# Возвращает все блюда
@router.get('/', response_model=List[schemas.DishOut])
def get_all_dishes_handler(target_submenu_id: uuid.UUID, dish: DishService = Depends()):
    return dish.get_all(target_submenu_id)


# Создаёт блюдо
@router.post('/',
             response_model=schemas.DishOut, status_code=status.HTTP_201_CREATED)
def create_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        dish_data: schemas.DishBase, dish: DishService = Depends()):
    return dish.create(target_menu_id, target_submenu_id, dish_data)


# Возвращает блюдо
@router.get('/{target_dish_id}',
            response_model=schemas.DishOut)
def get_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                     dish: DishService = Depends()):
    return dish.get(target_menu_id, target_submenu_id, target_dish_id)


# Обновляет блюдо
@router.patch('/{target_dish_id}',
              response_model=schemas.DishOut)
def update_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        dish_data: schemas.DishBase = Body(...), dish: DishService = Depends()):
    return dish.update(target_menu_id, target_submenu_id, target_dish_id, dish_data)


# Удаляет блюдо
@router.delete('/{target_dish_id}',
               response_model=schemas.DishOut)
def delete_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        dish: DishService = Depends()):
    return dish.delete(target_menu_id, target_submenu_id, target_dish_id)
