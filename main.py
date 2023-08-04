import uuid
from crud import menu_crud, submenu_crud, dish_crud
from fastapi import FastAPI, status, Body, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import List
from models import schemas
from db import create_session

app = FastAPI(title='Y_LAB MENU API')

# Menu
# Возвращает все меню
@app.get('/api/v1/menus/', response_model=List[schemas.AllMenu])
def get_all_menus(session: Session = Depends(create_session)) -> List[schemas.AllMenu]:
    return menu_crud.get_menus_with_counts(session)


# Создаёт меню
@app.post('/api/v1/menus/', response_model=schemas.MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuBase, session: Session = Depends(create_session)):
    return menu_crud.create_menu(menu, session)


# Возвращает меню
@app.get('/api/v1/menus/{target_menu_id}', response_model=schemas.AllMenu)
def get_menu(target_menu_id: uuid.UUID, session: Session = Depends(create_session)):
    return menu_crud.get_menu_with_counts(target_menu_id, session)


# Обновляет меню
@app.patch('/api/v1/menus/{target_menu_id}', response_model=schemas.MenuOut)
def update_menu(target_menu_id: uuid.UUID, menu_data: schemas.MenuBase = Body(...),
                session: Session = Depends(create_session)) -> schemas.MenuOut:
    return menu_crud.update_menu(target_menu_id, menu_data, session)


# Удаляет меню
@app.delete('/api/v1/menus/{target_menu_id}', response_model=schemas.MenuOut)
def delete_menu(target_menu_id: uuid.UUID, session: Session = Depends(create_session)) -> JSONResponse:
    return menu_crud.delete_menu(target_menu_id, session)


# SubMenu
# Возвращает все подменю
@app.get('/api/v1/menus/{target_menu_id}/submenus', response_model=List[schemas.AllSubmenu])
def get_submenus(target_menu_id: uuid.UUID, session: Session = Depends(create_session)):
    return submenu_crud.get_submenus_for_menu(target_menu_id, session)

# Создаёт подменю
@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.SubMenuOut,
          status_code=status.HTTP_201_CREATED)
def create_submenu(target_menu_id: uuid.UUID, submenu: schemas.SubMenuBase,
                   session: Session = Depends(create_session)):
    return submenu_crud.create_submenu(target_menu_id, submenu, session)



# Возвращает подменю
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.AllSubmenu)
def get_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        session: Session = Depends(create_session)):
    return submenu_crud.get_submenu(target_menu_id, target_submenu_id, session)

# Обновляет подменю
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenuOut)
def update_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           submenu_data: schemas.SubMenuBase = Body(...),
                           session: Session = Depends(create_session)):
    return submenu_crud.update_submenu(target_menu_id, target_submenu_id, submenu_data, session)

# Удаляет подменю
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.SubMenuOut)
def delete_submenu_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                           session: Session = Depends(create_session)):
    return submenu_crud.delete_submenu(target_menu_id, target_submenu_id, session)


# Dish
# Возвращает все блюда
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=List[schemas.DishOut])
def get_all_dishes_handler(target_submenu_id: uuid.UUID, session: Session = Depends(create_session)):
    return dish_crud.get_all_dishes(target_submenu_id, session)


# Создаёт блюдо
@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
          response_model=schemas.DishOut, status_code=status.HTTP_201_CREATED)
def create_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
                        dish_data: schemas.DishBase, session: Session = Depends(create_session)):
    return dish_crud.create_dish(target_menu_id, target_submenu_id, dish_data, session)


# Возвращает блюдо
@app.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
         response_model=schemas.DishOut)
def get_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                     session: Session = Depends(create_session)):
    return dish_crud.get_dish(target_menu_id, target_submenu_id, target_dish_id, session)


# Обновляет блюдо
@app.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
           response_model=schemas.DishOut)
def update_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        dish_data: schemas.DishBase = Body(...), session: Session = Depends(create_session)):
    return dish_crud.update_dish(target_menu_id, target_submenu_id, target_dish_id, dish_data, session)


# Удаляет блюдо
@app.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
            response_model=schemas.DishOut)
def delete_dish_handler(target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
                        session: Session = Depends(create_session)):
    return dish_crud.delete_dish(target_menu_id, target_submenu_id, target_dish_id, session)
