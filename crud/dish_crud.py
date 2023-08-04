import uuid
from typing import List

from fastapi import HTTPException
from starlette.responses import JSONResponse

from models import schemas
from models.models import Menu, SubMenu, Dish


# Возвращает все блюда для определенного подменю
def get_all_dishes(target_submenu_id: uuid.UUID, session) -> List[schemas.DishOut]:
    dishes = session.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()
    return dishes


# Создаёт блюдо для указанного подменю
def create_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                dish_data: schemas.DishBase, session):
    # Проверяем, существуют ли указанные меню и подменю
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
    submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                            SubMenu.menu_id == target_menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Создаем новое блюдо
    new_dish = Dish(**dish_data.model_dump(), submenu_id=target_submenu_id)
    session.add(new_dish)
    session.commit()
    session.refresh(new_dish)
    return new_dish

# Возвращает блюдо по его ID и принадлежности к указанному меню и подменю
def get_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
             target_dish_id: uuid.UUID, session):
    dish = (
        session.query(Dish)
        .join(SubMenu, SubMenu.id == Dish.submenu_id)
        .filter(SubMenu.menu_id == target_menu_id)
        .filter(Dish.submenu_id == target_submenu_id)
        .filter(Dish.id == target_dish_id)
        .first()
    )
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish

# Обновляет блюдо по его ID и принадлежности к указанному меню и подменю
def update_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                dish_data: schemas.DishBase, session):
    dish = (
        session.query(Dish)
        .join(SubMenu, SubMenu.id == Dish.submenu_id)
        .filter(SubMenu.menu_id == target_menu_id)
        .filter(Dish.submenu_id == target_submenu_id)
        .filter(Dish.id == target_dish_id)
        .first()
    )
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')

    for field, value in dish_data.dict().items():
        setattr(dish, field, value)

    session.commit()
    session.refresh(dish)
    return dish

# Удаляет блюдо по его ID и принадлежности к указанному меню и подменю
def delete_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                target_dish_id: uuid.UUID,session):
    dish = (
        session.query(Dish)
        .join(SubMenu, SubMenu.id == Dish.submenu_id)
        .filter(SubMenu.menu_id == target_menu_id)
        .filter(Dish.submenu_id == target_submenu_id)
        .filter(Dish.id == target_dish_id)
        .first()
    )
    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')

    session.delete(dish)
    session.commit()
    return JSONResponse(status_code=200, content={'message': f'Dish {dish.title} deleted successfully'})
