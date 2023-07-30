import time
import uuid

from fastapi import FastAPI, status, HTTPException, Body
from sqlalchemy import func, distinct
from starlette.responses import JSONResponse, HTMLResponse
from typing import List
import schemas
from db import SessionLocal
from models.models import Menu, SubMenu, Dish

app = FastAPI(title='YLAB Intensive')


@app.get('/55')
def test():
    time.sleep(5)
    return HTMLResponse('<h1>Hello my dear!</h1>')

# CRUD операции для Menu

# Возвращает все меню
@app.get('/api/v1/menus/', response_model=List[schemas.AllMenu])
def get_all_menus():
    with SessionLocal() as session:
        # Подсчёт кол-ва подменю и блюд для каждого меню
        menus_with_counts = (
            session.query(Menu, func.count(SubMenu.id).label('submenus_count'), func.count(Dish.id).label('dishes_count'))
            .outerjoin(SubMenu, Menu.id == SubMenu.menu_id)
            .outerjoin(Dish, SubMenu.id == Dish.submenu_id)
            .group_by(Menu)
            .all()
        )

        # Создание экземпляров схемы AllMenu и заполнение полей
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

# Создаёт меню
@app.post('/api/v1/menus/',response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuBase):
    with SessionLocal() as session:
        new_menu = Menu(**menu.model_dump())
        session.add(new_menu)
        session.commit()
        session.refresh(new_menu)
        return new_menu

# Возвращает меню
@app.get('/api/v1/menus/{target_menu_id}', response_model=schemas.AllMenu)
def get_menu(target_menu_id: uuid.UUID):
    with SessionLocal() as session:
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
        menu_response = schemas.AllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )

        return menu_response


# Обновляет меню
@app.patch('/api/v1/menus/{target_menu_id}', response_model=schemas.MenuOut)
def update_menu(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase = Body(...)):
    with SessionLocal() as session:
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        menu.title = menu_data.title
        menu.description = menu_data.description
        session.commit()
        session.refresh(menu)
        return menu


# Удаляет меню
@app.delete('/api/v1/menus/{target_menu_id}', response_model=schemas.MenuOut)
def delete_menu(target_menu_id: uuid.UUID):
    with SessionLocal() as session:
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        session.delete(menu)
        session.commit()
        return JSONResponse(status_code=200, content={'message': f'Menu {menu.title} deleted successfully'})

# CRUD операции для SubMenu

# Возвращает все подменю
@app.get('/api/v1/menus/{target_menu_id}/submenus', response_model=List[schemas.AllSubmenu])
def get_submenus_for_menu(target_menu_id: uuid.UUID):
    with SessionLocal() as session:
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


# Создаёт подменю
@app.post('/api/v1/menus/{target_menu_id}/submenus',
          response_model=schemas.SubMenuOut, status_code=status.HTTP_201_CREATED)
def create_submenu(target_menu_id: uuid.UUID, submenu: schemas.SubMenuBase):
    with SessionLocal() as session:
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        new_submenu = SubMenu(**submenu.model_dump(), menu_id=target_menu_id)
        session.add(new_submenu)
        session.commit()
        session.refresh(new_submenu)
        return new_submenu

# Возвращает подменю
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
         response_model=schemas.AllSubmenu)
def get_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID):
    with SessionLocal() as session:
        # Получаем сабменю
        submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                SubMenu.menu_id == target_menu_id).first()
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        # Подсчитываем количество блюд для данного сабменю
        dishes_count = session.query(func.count(Dish.id)).filter(
            Dish.submenu_id == target_submenu_id).scalar()

        # Создаем экземпляр схемы SubMenuOut и заполняем поля
        submenu_response = schemas.AllSubmenu(
            id=submenu.id,
            title=submenu.title,
            description = submenu.description,
            menu_id=submenu.menu_id,
            dishes_count=dishes_count
        )

        return submenu_response


# Обновляет подменю
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
           response_model=schemas.SubMenuOut)
def update_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                   submenu_data: schemas.SubMenuBase = Body(...)):
    with SessionLocal() as session:
        submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id, SubMenu.menu_id == target_menu_id).first()

        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        submenu.title = submenu_data.title
        submenu.description = submenu_data.description
        session.commit()
        session.refresh(submenu)
        return submenu

# Удаляет подменю
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
            response_model=schemas.SubMenuOut)
def delete_submenu(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID):
    with SessionLocal() as session:
        submenu = session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                SubMenu.menu_id == target_menu_id).first()
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        session.delete(submenu)
        session.commit()
        return JSONResponse(status_code=200, content={'message': f'Submenu {submenu.title} deleted successfully'})

# CRUD операции для Dish

# Возвращает все блюда
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
         response_model=List[schemas.DishOut])
def get_all_dishes(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID):
    with SessionLocal() as session:
        dishes = session.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()
        return dishes


# Создаёт блюдо
@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
          response_model=schemas.DishOut,status_code=status.HTTP_201_CREATED)
def create_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, dish_data: schemas.DishBase):
    with SessionLocal() as session:
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


# Возвращает блюдо
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
         response_model=schemas.DishOut)
def get_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID):
    with SessionLocal() as session:
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


# Обновляет блюдо
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
              response_model=schemas.DishOut)
def update_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                dish_data: schemas.DishBase = Body(...)):
    with SessionLocal() as session:
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

# Удаляет блюдо
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
               response_model=schemas.DishOut)
def delete_dish(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID):
    with SessionLocal() as session:
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
