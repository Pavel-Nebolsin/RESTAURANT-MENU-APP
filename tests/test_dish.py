import aiohttp
import pytest
from tests_config import prefix, test_data


# Создаем меню
@pytest.mark.asyncio
async def test_DISH_1_create_menu() -> None:
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201

            target_menu_id = (await response.json()).get('id')
            assert target_menu_id is not None

            test_data['target_menu_id'] = target_menu_id


# Создаем подменю
@pytest.mark.asyncio
async def test_DISH_2_create_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    data = {
        'title': 'Test Submenu',
        'description': 'This is a test submenu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201

            test_data['target_submenu_id'] = (await response.json()).get('id')
            assert test_data['target_submenu_id'] is not None


# Просматриваем список блюд
@pytest.mark.asyncio
async def test_DISH_3_view_dishes() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []


# Создаем блюдо
@pytest.mark.asyncio
async def test_DISH_4_create_dish() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    data = {
        'title': 'Test Dish',
        'description': 'This is a test dish',
        'price': 10.99
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201

            response_json = await response.json()

            test_data['target_dish_id'] = response_json.get('id')
            test_data['target_dish_title'] = response_json.get('title')
            test_data['target_dish_description'] = response_json.get('description')
            test_data['target_dish_price'] = response_json.get('price')

            assert test_data['target_dish_id'] is not None
            assert test_data['target_dish_title'] == 'Test Dish'
            assert test_data['target_dish_description'] == 'This is a test dish'
            assert test_data['target_dish_price'] == '10.99'

# Просматриваем список блюд


@pytest.mark.asyncio
async def test_DISH_5_get_dishes() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() != []


# Просматриваем определенное блюдо
@pytest.mark.asyncio
async def test_DISH_6_view_dish() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200

            response_json = await response.json()
            assert response_json['id'] == target_dish_id
            assert response_json['title'] == test_data['target_dish_title']
            assert response_json['description'] == test_data['target_dish_description']
            assert response_json['price'] == test_data['target_dish_price']


# Обновляем блюдо
@pytest.mark.asyncio
async def test_DISH_7_update_dish() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    data = {
        'title': 'Updated Test Dish',
        'description': 'This is an updated test dish',
        'price': 55.55
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=data) as response:
            assert response.status == 200

            response_json = await response.json()
            assert response_json['title'] != test_data['target_dish_title']
            assert response_json['description'] != test_data['target_dish_description']
            assert response_json['price'] != test_data['target_dish_price']

            test_data['target_dish_title'] = response_json['title']
            test_data['target_dish_description'] = response_json['description']
            test_data['target_dish_price'] = response_json['price']


# Просматриваем определенное блюдо
@pytest.mark.asyncio
async def test_DISH_8_view_dish() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200

            response_json = await response.json()
            assert response_json['id'] == test_data['target_dish_id']
            assert response_json['title'] == test_data['target_dish_title']
            assert response_json['description'] == test_data['target_dish_description']
            assert response_json['price'] == test_data['target_dish_price']

# Удаляем блюдо


@pytest.mark.asyncio
async def test_DISH_9_delete_dish() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем список блюд
@pytest.mark.asyncio
async def test_DISH_10_get_dishes() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []


# Просматриваем определённое блюдо
@pytest.mark.asyncio
async def test_DISH_11_view_dish() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 404
            response_json = await response.json()
            assert response_json['detail'] == 'dish not found'


# Удаляет подменю
@pytest.mark.asyncio
async def test_DISH_12_delete_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем список подменю
@pytest.mark.asyncio
async def test_DISH_13_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []


# Удаляем меню
@pytest.mark.asyncio
async def test_DISH_14_delete_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем список меню
@pytest.mark.asyncio
async def test_DISH_15_get_menus() -> None:
    url = f'{prefix}/menus/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []
