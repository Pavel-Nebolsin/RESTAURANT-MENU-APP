import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db.db import create_session
from models import schemas
from models.models import Dish, Menu, SubMenu


class MenuRepository:

    def __init__(self, session: Session = Depends(create_session)) -> None:
        self.session: Session = session
        self.model = Menu

    def get_all(self) -> list[schemas.AllMenu]:
        menus = self.session.query(self.model).all()
        menu_responses = []
        for menu in menus:
            submenus_count = self.session.query(SubMenu).filter(SubMenu.menu_id == menu.id).count()
            dishes_count = self.session.query(Dish).join(SubMenu).filter(SubMenu.menu_id == menu.id).count()
            menu_response = schemas.AllMenu(
                id=menu.id,
                title=menu.title,
                description=menu.description,
                submenus_count=submenus_count,
                dishes_count=dishes_count
            )
            menu_responses.append(menu_response)
        return menu_responses

    def get(self, target_menu_id: uuid.UUID) -> schemas.AllMenu:
        # Получаем меню по айди
        menu = self.session.query(self.model).filter(self.model.id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        # Подсчитываем количество подменю и блюд для данного меню
        submenus_count = self.session.query(SubMenu).filter(SubMenu.menu_id == target_menu_id).count()
        dishes_count = self.session.query(Dish).join(SubMenu).filter(SubMenu.menu_id == target_menu_id).count()

        # Создаем экземпляр схемы AllMenu и заполняем поля
        menu_response = schemas.AllMenu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=dishes_count
        )
        return menu_response

    def create(self, menu: schemas.MenuBase) -> Menu:
        new_menu = self.model(**menu.model_dump())
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def update(self, target_menu_id: uuid.UUID, menu_data: schemas.MenuBase) -> Menu:
        menu = self.session.query(self.model).filter(self.model.id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        menu.title = menu_data.title
        menu.description = menu_data.description
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def delete(self, target_menu_id: uuid.UUID) -> JSONResponse:
        menu = self.session.query(self.model).filter(self.model.id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        menu_title = menu.title
        self.session.delete(menu)
        self.session.commit()
        return JSONResponse(status_code=200, content={'message': f'Menu {menu_title} deleted successfully'})
