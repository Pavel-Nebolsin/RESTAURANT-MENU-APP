import uuid

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from models import schemas
from models.models import Dish
from services.dish_service import DishService

router = APIRouter()


@router.get('/', response_model=list[schemas.DishOut],
            status_code=status.HTTP_200_OK,
            summary='Возвращает список блюд')
def get_all_dishes_handler(target_submenu_id: uuid.UUID,
                           dish: DishService = Depends()) -> list[schemas.DishOut]:
    return dish.get_all(target_submenu_id)


@router.get('/{target_dish_id}', response_model=schemas.DishOut,
            status_code=status.HTTP_200_OK,
            summary='Возвращает определённое блюдо')
def get_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                     target_dish_id: uuid.UUID,
                     dish: DishService = Depends()) -> schemas.AllDish:
    return dish.get(target_menu_id, target_submenu_id, target_dish_id)


@router.post('/', response_model=schemas.DishOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создаёт блюдо')
def create_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        dish_data: schemas.DishBase,
                        dish: DishService = Depends()) -> Dish:
    return dish.create(target_menu_id, target_submenu_id, dish_data)


@router.patch('/{target_dish_id}', response_model=schemas.DishOut,
              status_code=status.HTTP_200_OK,
              summary='Обновляет блюдо')
def update_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        target_dish_id: uuid.UUID, dish_data: schemas.DishBase = Body(...),
                        dish: DishService = Depends()) -> schemas.DishOut:
    return dish.update(target_menu_id, target_submenu_id, target_dish_id, dish_data)


@router.delete('/{target_dish_id}',
               status_code=status.HTTP_200_OK,
               summary='Удаляет блюдо')
def delete_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        dish: DishService = Depends()) -> JSONResponse:
    return dish.delete(target_menu_id, target_submenu_id, target_dish_id)
