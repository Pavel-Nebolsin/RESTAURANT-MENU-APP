import aiohttp
import pytest
from tests_config import prefix, test_data


# Создаем меню
@pytest.mark.asyncio
async def test_SUBMENU_9_create_menu() -> None:
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

# Просматриваем список подменю


@pytest.mark.asyncio
async def test_SUBMENU_1_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []

# Создаем подменю


@pytest.mark.asyncio
async def test_SUBMENU_2_create_submenu() -> None:
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

            assert test_data['target_submenu_id'] is not None
            assert test_data['target_submenu_title'] == 'Test Submenu'
            assert test_data['target_submenu_description'] == 'This is a test submenu'

# Просматриваем список подменю


@pytest.mark.asyncio
async def test_SUBMENU_3_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() != []

# Просматриваем определенное подменю


@pytest.mark.asyncio
async def test_SUBMENU_4_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200

            response_json = await response.json()
            assert response_json['id'] == target_submenu_id
            assert response_json['title'] == test_data.get('target_submenu_title')
            assert response_json['description'] == test_data.get('target_submenu_description')


# Обновляем определенное подменю
@pytest.mark.asyncio
async def test_SUBMENU_5_update_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    data = {
        'title': 'Updated Submenu',
        'description': 'This is an updated submenu'
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=data) as response:
            assert response.status == 200

            response_json = await response.json()
            # Проверяем, что данные изменились
            assert response_json['title'] != test_data.get('target_submenu_title')
            assert response_json['description'] != test_data.get('target_submenu_description')

            # Сохраняем обновленные данные в словарь
            test_data['target_submenu_title'] = data['title']
            test_data['target_submenu_description'] = data['description']

            # Проверяем, что данные соответствуют обновленным данным
            assert test_data['target_submenu_title'] == response_json['title']
            assert test_data['target_submenu_description'] == response_json['description']

# Просматриваем определенное подменю


@pytest.mark.asyncio
async def test_SUBMENU_6_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200

            response_json = await response.json()
            assert response_json['id'] == test_data.get('target_submenu_id')
            assert response_json['title'] == test_data.get('target_submenu_title')
            assert response_json['description'] == test_data.get('target_submenu_description')

# Удаляем подменю


@pytest.mark.asyncio
async def test_SUBMENU_7_delete_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200

# Просматриваем список подменю


@pytest.mark.asyncio
async def test_SUBMENU_8_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []

# Просматриваем определенное подменю


@pytest.mark.asyncio
async def test_SUBMENU_9_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 404
            response_json = await response.json()
            assert response_json['detail'] == 'submenu not found'

# Удаляем меню


@pytest.mark.asyncio
async def test_SUBMENU_10_delete_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}'

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            assert response.status == 200

# Просматриваем список меню


@pytest.mark.asyncio
async def test_SUBMENU_11_get_menus() -> None:
    url = f'{prefix}/menus'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            assert await response.json() == []
