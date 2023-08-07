import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db.db import create_session
from models import schemas
from models.models import Dish, Menu, SubMenu


class DishRepository:

    def __init__(self, session: Session = Depends(create_session)) -> None:
        self.session: Session = session

    def get_all(self, target_submenu_id: uuid.UUID) -> list[schemas.DishOut]:
        dishes = self.session.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()
        return dishes

    def create(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               dish_data: schemas.DishBase) -> Dish:

        menu = self.session.query(Menu).filter(Menu.id == target_menu_id).first()
        submenu = self.session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                     SubMenu.menu_id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        new_dish = Dish(**dish_data.model_dump(), submenu_id=target_submenu_id)
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
            target_dish_id: uuid.UUID) -> Dish:
        dish = (
            self.session.query(Dish)
            .join(SubMenu, SubMenu.id == Dish.submenu_id)
            .filter(SubMenu.menu_id == target_menu_id)
            .filter(Dish.submenu_id == target_submenu_id)
            .filter(Dish.id == target_dish_id)
            .first()
        )
        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')
        return dish

    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
               dish_data: schemas.DishBase) -> Dish:
        dish = (
            self.session.query(Dish)
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

        self.session.commit()
        self.session.refresh(dish)
        return dish

    def delete(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               target_dish_id: uuid.UUID) -> JSONResponse:
        dish = (
            self.session.query(Dish)
            .join(SubMenu, SubMenu.id == Dish.submenu_id)
            .filter(SubMenu.menu_id == target_menu_id)
            .filter(Dish.submenu_id == target_submenu_id)
            .filter(Dish.id == target_dish_id)
            .first()
        )
        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')

        self.session.delete(dish)
        self.session.commit()
        return JSONResponse(status_code=200, content={'message': f'Dish {dish.title} deleted successfully'})
