from fastapi import FastAPI

from routers import dish_router, menu_router, submenu_router

app = FastAPI(title='Y_LAB RESTAURANT API')

app.include_router(menu_router.router,
                   prefix='/api/v1/menus',
                   tags=['menus'])
app.include_router(submenu_router.router,
                   prefix='/api/v1/menus/{target_menu_id}/submenus',
                   tags=['submenus'])
app.include_router(dish_router.router,
                   prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
                   tags=['dishes'])
