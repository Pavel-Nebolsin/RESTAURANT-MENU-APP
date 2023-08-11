import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Dish, SubMenu


async def get_counts(session: AsyncSession,
                     menu_id: uuid.UUID,
                     submenu_id: uuid.UUID | None = None) -> tuple[int, int]:
    if submenu_id is None:
        submenus_count_query = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu_id)
        submenus_count = await session.execute(submenus_count_query)
        submenus_count = submenus_count.scalar_one() if submenus_count else 0
    else:
        submenus_count = None  # Если submenu_id указан, не считаем количество подменю

    dishes_count_query = select(func.count(Dish.id)).join(SubMenu).where(
        SubMenu.menu_id == menu_id
    )
    if submenu_id is not None:
        dishes_count_query = dishes_count_query.where(SubMenu.id == submenu_id)

    dishes_count = await session.execute(dishes_count_query)
    dishes_count = dishes_count.scalar_one() if dishes_count else 0

    return submenus_count, dishes_count
