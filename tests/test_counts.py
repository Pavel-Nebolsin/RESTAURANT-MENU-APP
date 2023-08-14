import aiohttp
import pytest
from tests_config import prefix, test_data


# ТЕСТЫ НА ПРОВЕРКУ КОЛИЧЕСТВА БЛЮД В ПОДМЕНЮ И МЕНЮ:
# Создаем меню
@pytest.mark.asyncio
async def test_COUNT_1_create_menu() -> None:
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201
            response_json = await response.json()

            test_data['target_menu_id'] = response_json.get('id')
            test_data['target_menu_title'] = response_json.get('title')
            test_data['target_menu_description'] = response_json.get('description')

            assert test_data['target_menu_id'] is not None


# Создаем подменю
@pytest.mark.asyncio
async def test_COUNT_2_create_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    data = {
        'title': 'Test Submenu',
        'description': 'This is a test submenu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            assert response.status == 201
            response_json = await response.json()

            test_data['target_submenu_id'] = response_json.get('id')
            test_data['target_submenu_title'] = response_json.get('title')
            test_data['target_submenu_description'] = response_json.get('description')

            assert test_data['target_submenu_id'] == response_json.get('id')


# Создаем блюдо 1
@pytest.mark.asyncio
async def test_COUNT_3_create_dish1() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
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

            test_data['target_dish1_id'] = response_json.get('id')

            assert test_data['target_dish1_id'] is not None


# Создаем блюдо 2
@pytest.mark.asyncio
async def test_COUNT_4_create_dish2() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
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

            test_data['target_dish2_id'] = response_json.get('id')

            assert test_data['target_dish2_id'] is not None


# Просматриваем определенное меню
@pytest.mark.asyncio
async def test_COUNT_5_view_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert test_data['target_menu_id'] == response_json.get('id')
            assert 1 == response_json.get('submenus_count')
            assert 2 == response_json.get('dishes_count')


# Просматриваем определенное подменю
@pytest.mark.asyncio
async def test_COUNT_6_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert test_data['target_submenu_id'] == response_json.get('id')
            assert 2 == response_json.get('dishes_count')


# Удаляет подменю
@pytest.mark.asyncio
async def test_COUNT_7_delete_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем список подменю
@pytest.mark.asyncio
async def test_COUNT_8_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []


# Просматриваем список блюд
@pytest.mark.asyncio
async def test_COUNT_9_get_dishes() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []


# Просматриваем определенное меню
@pytest.mark.asyncio
async def test_COUNT_10_view_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert test_data['target_menu_id'] == response_json.get('id')
            assert 0 == response_json.get('submenus_count')
            assert 0 == response_json.get('dishes_count')


# Удаляем меню
@pytest.mark.asyncio
async def test_COUNT_11_delete_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200


# Просматриваем список меню
@pytest.mark.asyncio
async def test_COUNT_12_get_menus() -> None:
    url = f'{prefix}/menus/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []
