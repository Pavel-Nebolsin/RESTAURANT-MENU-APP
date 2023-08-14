from fastapi import APIRouter, Depends, status

from services.menu_service import MenuService

router = APIRouter()


@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Возвращает все меню, подменю и блюда')
async def get_all_handler(menu: MenuService = Depends()):
    return await menu.all_menus_with_content()
