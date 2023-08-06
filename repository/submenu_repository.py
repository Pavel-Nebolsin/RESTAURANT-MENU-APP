import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db import create_session
from models import schemas
from models.models import Dish, Menu, SubMenu


class SubMenuRepository:

    def __init__(self, session: Session = Depends(create_session)) -> None:
        self.session: Session = session

    def get_all(self, target_menu_id: uuid.UUID) -> list[schemas.AllSubmenu]:

        submenus = self.session.query(SubMenu).filter(SubMenu.menu_id == target_menu_id).all()

        submenu_responses = []

        for submenu in submenus:
            dishes_count = self.session.query(func.count(Dish.id)).filter(
                Dish.submenu_id == submenu.id).scalar()

            submenu_response = schemas.AllSubmenu(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id,
                dishes_count=dishes_count
            )

            submenu_responses.append(submenu_response)

        return submenu_responses

    def create(self, target_menu_id: uuid.UUID, submenu_data: schemas.SubMenuBase) -> SubMenu:
        menu = self.session.query(Menu).filter(Menu.id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        new_submenu = SubMenu(**submenu_data.model_dump(), menu_id=target_menu_id)
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)
        return new_submenu

    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> schemas.AllSubmenu:
        submenu = self.session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                     SubMenu.menu_id == target_menu_id).first()
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        dishes_count = self.session.query(func.count(Dish.id)).filter(
            Dish.submenu_id == target_submenu_id).scalar()

        submenu_response = schemas.AllSubmenu(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            menu_id=submenu.menu_id,
            dishes_count=dishes_count
        )

        return submenu_response

    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               submenu_data: schemas.SubMenuBase) -> schemas.SubMenuOut:
        submenu = self.session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                     SubMenu.menu_id == target_menu_id).first()
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        submenu.title = submenu_data.title
        submenu.description = submenu_data.description
        self.session.commit()
        self.session.refresh(submenu)

        return submenu

    def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID) -> JSONResponse:
        submenu = self.session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                     SubMenu.menu_id == target_menu_id).first()
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        self.session.delete(submenu)
        self.session.commit()

        return JSONResponse(status_code=200,
                            content={'message': f'Submenu {submenu.title} deleted successfully'})
