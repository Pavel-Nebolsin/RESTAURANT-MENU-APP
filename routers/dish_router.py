import uuid

from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from schemas.dish_schema import DishBase, DishSchema
from services.dish_service import DishService

router = APIRouter()


@router.get('/', response_model=list[DishSchema],
            status_code=status.HTTP_200_OK,
            summary='Возвращает список блюд')
async def get_all_dishes_handler(target_submenu_id: uuid.UUID,
                                 dish: DishService = Depends()) -> list[DishSchema]:
    return await dish.get_all(target_submenu_id)


@router.get('/{target_dish_id}', response_model=DishSchema,
            status_code=status.HTTP_200_OK,
            summary='Возвращает определённое блюдо')
async def get_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           target_dish_id: uuid.UUID,
                           dish: DishService = Depends()) -> DishSchema:
    return await dish.get(target_menu_id, target_submenu_id, target_dish_id)


@router.post('/', response_model=DishSchema,
             status_code=status.HTTP_201_CREATED,
             summary='Создаёт блюдо')
async def create_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                              dish_data: DishBase,
                              dish: DishService = Depends()) -> DishSchema:
    return await dish.create(target_menu_id, target_submenu_id, dish_data)


@router.patch('/{target_dish_id}', response_model=DishSchema,
              status_code=status.HTTP_200_OK,
              summary='Обновляет блюдо')
async def update_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                              target_dish_id: uuid.UUID, dish_data: DishBase = Body(...),
                              dish: DishService = Depends()) -> DishSchema:
    return await dish.update(target_menu_id, target_submenu_id, target_dish_id, dish_data)


@router.delete('/{target_dish_id}',
               status_code=status.HTTP_200_OK,
               summary='Удаляет блюдо')
async def delete_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                              dish: DishService = Depends()) -> JSONResponse:
    return await dish.delete(target_menu_id, target_submenu_id, target_dish_id)
