import aiohttp
import pytest
from tests_config import prefix, test_data


@pytest.mark.asyncio
async def test_MENU_1_get_menus() -> None:
    url = f'{prefix}/menus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []


@pytest.mark.asyncio
async def test_MENU_2_create_menu() -> None:
    url = f'{prefix}/menus'
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
            assert test_data['target_menu_title'] == 'Test Menu'
            assert test_data['target_menu_description'] == 'This is a test menu'


@pytest.mark.asyncio
async def test_MENU_3_list_menus() -> None:
    url = f'{prefix}/menus/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() != []


# Просматриваем определенное меню
@pytest.mark.asyncio
async def test_MENU_4_view_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            response_json = await response.json()

            assert response_json['id'] == target_menu_id
            assert response_json['title'] == test_data.get('target_menu_title')
            assert response_json['description'] == test_data.get('target_menu_description')

# Обновляем меню


@pytest.mark.asyncio
async def test_MENU_5_update_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}'
    data = {
        'title': 'Updated Test Menu',
        'description': 'This is an updated test menu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=data) as response:
            assert response.status == 200

            assert test_data['target_menu_title'] != data['title']
            assert test_data['target_menu_description'] != data['description']

            test_data['target_menu_title'] = data['title']
            test_data['target_menu_description'] = data['description']

            response_json = await response.json()
            assert test_data['target_menu_title'] == response_json.get('title')
            assert test_data['target_menu_description'] == response_json.get('description')

# Удаляем меню


@pytest.mark.asyncio
async def test_MENU_6_delete_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200

# Просматриваем список меню


@pytest.mark.asyncio
async def test_MENU_7_get_menus() -> None:
    url = f'{prefix}/menus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []

# Просматриваем определенное меню


@pytest.mark.asyncio
async def test_MENU_8_view_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 404
            response_json = await response.json()
            assert response_json['detail'] == 'menu not found'
