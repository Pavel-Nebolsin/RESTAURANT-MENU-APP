import uuid
from typing import List

from fastapi import HTTPException
from sqlalchemy import func, distinct
from starlette.responses import JSONResponse

import schemas
from models.models import Menu, SubMenu, Dish


# Функция для подсчета количества подменю и блюд, и выдачи списка меню
def get_menus_with_counts(session) -> List[schemas.AllMenu]:
    menus_with_counts = (
        session.query(Menu, func.count(SubMenu.id).label('submenus_count'),
                      func.count(Dish.id).label('dishes_count'))
        .outerjoin(SubMenu, Menu.id == SubMenu.menu_id)
        .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
        .group_by(Menu)
        .all()
    )

    # Cоздание экземпляров схемы AllMenu и заполнения полей
    menu_responses = []
    for menu, submenus_count, dishes_count in menus_with_counts:
        menu_response = schemas.AllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        menu_responses.append(menu_response)
    return menu_responses


# Функция для подсчета количества подменю и блюд, и выдачи меню по айди
def get_menu_with_counts(target_menu_id: uuid.UUID, session) -> schemas.AllMenu:
    # Получаем меню и считаем количество подменю и блюд для данного меню
    menu_query = (
        session.query(Menu, func.count(distinct(SubMenu.id)).label('submenu_count'),
                      func.count(distinct(Dish.id)).label('dishes_count'))
        .outerjoin(SubMenu, Menu.id == SubMenu.menu_id)
        .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
        .filter(Menu.id == target_menu_id)
        .group_by(Menu)
    )

    menu_with_counts = menu_query.first()

    if not menu_with_counts:
        raise HTTPException(status_code=404, detail='menu not found')

    menu, submenus_count, dishes_count = menu_with_counts
    # Cоздание экземпляра схемы AllMenu и заполнения полей
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
