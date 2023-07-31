import uuid
from typing import List

from fastapi import HTTPException
from sqlalchemy import func, distinct
from starlette.responses import JSONResponse

import schemas
from models.models import Menu, SubMenu, Dish


# Функция для подсчета количества подменю и блюд, и выдачи списка меню
def get_menus_with_counts(session) -> List[schemas.AllMenu]:
    menus = session.query(Menu).all()
    menu_responses = []
    for menu in menus:
        submenus_count = session.query(SubMenu).filter(SubMenu.menu_id == menu.id).count()
        dishes_count = session.query(Dish).join(SubMenu).filter(SubMenu.menu_id == menu.id).count()
        menu_response = schemas.AllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        menu_responses.append(menu_response)
    return menu_responses


def get_menu_with_counts(target_menu_id: uuid.UUID, session) -> schemas.AllMenu:
    # Получаем меню по айди
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    # Подсчитываем количество подменю и блюд для данного меню
    submenus_count = session.query(SubMenu).filter(SubMenu.menu_id == target_menu_id).count()
    dishes_count = session.query(Dish).join(SubMenu).filter(SubMenu.menu_id == target_menu_id).count()

    # Создаем экземпляр схемы AllMenu и заполняем поля
    menu_response = schemas.AllMenu(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=submenus_count,
        dishes_count=dishes_count
    )
    return menu_response


def create_menu(menu: schemas.MenuBase, session):
    new_menu = Menu(**menu.model_dump())
    session.add(new_menu)
    session.commit()
    session.refresh(new_menu)
    return new_menu


def update_menu(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase, session) -> schemas.MenuOut:
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    menu.title = menu_data.title
    menu.description = menu_data.description
    session.commit()
    session.refresh(menu)
    return menu


def delete_menu(target_menu_id: uuid.UUID, session) -> JSONResponse:
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')

    menu_title = menu.title
    session.delete(menu)
    session.commit()
    return JSONResponse(status_code=200, content={'message': f'Menu {menu_title} deleted successfully'})
