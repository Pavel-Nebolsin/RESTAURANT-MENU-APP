import aiohttp
import pytest
from tests_config import prefix

test_data_get_all = []


# Создаем меню
@pytest.mark.asyncio
async def test_GET_ALL_1_create_menu() -> None:
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201
            response_json = await response.json()

            test_data_get_all.append({
                'id': response_json.get('id'),
                'title': response_json.get('title'),
                'description': response_json.get('description'),
                'submenus': []
            })

            assert response_json.get('id') is not None


# Создаем подменю
@pytest.mark.asyncio
async def test_GET_ALL_2_create_submenu() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    data = {
        'title': 'Test Submenu',
        'description': 'This is a test submenu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201
            response_json = await response.json()

            test_data_get_all[0]['submenus'].append({
                'id': response_json.get('id'),
                'title': response_json.get('title'),
                'description': response_json.get('description'),
                'dishes': []
            })

            assert response_json.get('id') is not None


# Создаем блюдо 1
@pytest.mark.asyncio
async def test_GET_ALL_3_create_dish1() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    target_submenu_id = test_data_get_all[0]['submenus'][0]['id']

    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    data = {
        'title': 'Test Dish 1',
        'description': 'This is a test dish 1',
        'price': 19.99
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201
            response_json = await response.json()

            test_data_get_all[0]['submenus'][0]['dishes'].append({
                'id': response_json.get('id'),
                'title': response_json.get('title'),
                'description': response_json.get('description'),
                'price': float(response_json.get('price'))
            })

            assert response_json.get('id') is not None


# Создаем блюдо 2
@pytest.mark.asyncio
async def test_GET_ALL_4_create_dish2() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    target_submenu_id = test_data_get_all[0]['submenus'][0]['id']

    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    data = {
        'title': 'Test Dish 2',
        'description': 'This is a test dish 2',
        'price': 119.99
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201
            response_json = await response.json()

            test_data_get_all[0]['submenus'][0]['dishes'].append({
                'id': response_json.get('id'),
                'title': response_json.get('title'),
                'description': response_json.get('description'),
                'price': float(response_json.get('price'))
            })

            assert response_json.get('id') is not None


# Просматриваем всё содержимое базы одним запросом
@pytest.mark.asyncio
async def test_GET_ALL_5_view_all() -> None:
    url = f'{prefix}/all_menus_with_content/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert response_json == test_data_get_all


# Удаляем блюдо
@pytest.mark.asyncio
async def test_GET_ALL_6_delete_dish() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    target_submenu_id = test_data_get_all[0]['submenus'][0]['id']
    target_dish_id = test_data_get_all[0]['submenus'][0]['dishes'][1]['id']
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем всё содержимое базы после удаления одного блюда одним запросом
@pytest.mark.asyncio
async def test_GET_ALL_7_view_all() -> None:
    url = f'{prefix}/all_menus_with_content/'
    test_data_get_all[0]['submenus'][0]['dishes'].pop(1)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert response_json == test_data_get_all


# Удаляем меню чтобы удалилось всё с ним связанное
@pytest.mark.asyncio
async def test_GET_ALL_8_delete_menu() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    url = f'{prefix}/menus/{target_menu_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем всё содержимое базы после удаления всего
@pytest.mark.asyncio
async def test_GET_ALL_9_view_all() -> None:
    url = f'{prefix}/all_menus_with_content/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert response_json == []
