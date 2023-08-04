import uuid
from crud import menu_crud, submenu_crud, dish_crud
from fastapi import FastAPI, status, Body, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from typing import List
from models import schemas
from db import create_session
from routers import menu_router, submenu_router, dish_router

app = FastAPI(title='Y_LAB MENU API')

app.include_router(menu_router.router,
                   prefix="/api/v1/menus",
                   tags=["menus"])
app.include_router(submenu_router.router,
                   prefix="/api/v1/menus/{target_menu_id}/submenus",
                   tags=["submenus"])
app.include_router(dish_router.router,
                   prefix="/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
                   tags=["dishes"])
