import uuid
from typing import List

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db import create_session
from models import schemas
from models.models import Menu, SubMenu, Dish


class DishRepository:

    def __init__(self, session: Session = Depends(create_session)):
        self.session: Session = session
        self.model = Dish

    # Возвращает все блюда для определенного подменю
    def get_all(self, target_submenu_id: uuid.UUID) -> List[schemas.DishOut]:
        dishes = self.session.query(Dish).filter(Dish.submenu_id == target_submenu_id).all()
        return dishes

    # Создаёт блюдо для указанного подменю
    def create(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
               dish_data: schemas.DishBase):
        # Проверяем, существуют ли указанные меню и подменю
        menu = self.session.query(Menu).filter(Menu.id == target_menu_id).first()
        submenu = self.session.query(SubMenu).filter(SubMenu.id == target_submenu_id,
                                                SubMenu.menu_id == target_menu_id).first()

        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')

        # Создаем новое блюдо
        new_dish = Dish(**dish_data.model_dump(), submenu_id=target_submenu_id)
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    # Возвращает блюдо по его ID и принадлежности к указанному меню и подменю
    def get(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID,
            target_dish_id: uuid.UUID):
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

    # Обновляет блюдо по его ID и принадлежности к указанному меню и подменю
    def update(self, target_menu_id: uuid.UUID, target_submenu_id: uuid.UUID, target_dish_id: uuid.UUID,
               dish_data: schemas.DishBase):
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

    # Удаляет блюдо по его ID и принадлежности к указанному меню и подменю
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
