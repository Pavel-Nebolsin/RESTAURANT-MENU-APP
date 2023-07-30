import uuid
from typing import List

from fastapi import HTTPException
from sqlalchemy import func, distinct
from starlette.responses import JSONResponse

import schemas
from models.models import Menu, SubMenu, Dish


# Функция для получения всех подменю для конкретного меню
def get_submenus_for_menu(target_menu_id: uuid.UUID, session) -> List[schemas.AllSubmenu]:
    # Подсчёт кол-ва блюд для каждого подменю
    submenus_with_counts = (
        session.query(SubMenu, func.count(Dish.id).label('dishes_count'))
        .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
        .filter(SubMenu.menu_id == target_menu_id)
        .group_by(SubMenu)
        .all()
    )

    # Создание экземпляров схемы AllSubmenu и заполнение полей
    submenu_responses = []
    for submenu, dishes_count in submenus_with_counts:
        submenu_response = schemas.AllSubmenu(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,  # Добавляем поле description
            menu_id=submenu.menu_id,
            dishes_count=dishes_count
        )
        # Добавление их список подменю для вывода
        submenu_responses.append(submenu_response)

    return submenu_responses


def create_submenu(target_menu_id: uuid.UUID, submenu: schemas.SubMenuBase, session) -> SubMenu:
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    new_submenu = SubMenu(**submenu.model_dump(), menu_id=target_menu_id)
    session.add(new_submenu)
    session.commit()
    session.refresh(new_submenu)
    return new_submenu


# Получаем подменю и подсчитываем количество блюд для данного подменю
def get_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, session) -> schemas.AllSubmenu:
    submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id, SubMenu.menu_id == target_menu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    # Подсчитываем количество блюд
    dishes_count = session.query(func.count(Dish.id)).filter(Dish.submenu_id == target_submenu_id).scalar()

    # Создаем экземпляр схемы SubMenuOut и заполняем поля
    submenu_response = schemas.AllSubmenu(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        menu_id=submenu.menu_id,
        dishes_count=dishes_count
    )

    return submenu_response


# Обновление подменю
def update_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                   submenu_data: schemas.SubMenuBase, session) -> schemas.SubMenuOut:
    submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                            SubMenu.menu_id == target_menu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    submenu.title = submenu_data.title
    submenu.description = submenu_data.description
    session.commit()
    session.refresh(submenu)

    return submenu


# Удаление подменю
def delete_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, session) -> JSONResponse:
    submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                            SubMenu.menu_id == target_menu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    session.delete(submenu)
    session.commit()

    return JSONResponse(status_code=200, content={'message': f'Submenu {submenu.title} deleted successfully'})
