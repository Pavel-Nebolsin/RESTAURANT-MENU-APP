import requests
from tests_config import prefix

test_data_get_all = []

# Создаем меню


def test_GET_ALL_1_create_menu() -> None:
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }
    response = requests.post(url, json=data)

    # Проверяем, что запрос вернул код 201 CREATED
    assert response.status_code == 201
    response_json = response.json()

    # Сохраняем данные в словарь test_data_get_all
    test_data_get_all.append({
        'id': response_json.get('id'),
        'title': response_json.get('title'),
        'description': response_json.get('description'),
        'submenus': []
    })

    # Проверяем, что response содержит id menu
    assert response_json.get('id') is not None


# Создаем подменю
def test_GET_ALL_2_create_submenu() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    data = {
        'title': 'Test Submenu',
        'description': 'This is a test submenu'
    }
    response = requests.post(url, json=data)

    # Проверяем, что запрос вернул код 201 CREATED
    assert response.status_code == 201
    response_json = response.json()

    # Сохраняем данные в словарь test_data
    test_data_get_all[0]['submenus'].append({
        'id': response_json.get('id'),
        'title': response_json.get('title'),
        'description': response_json.get('description'),
        'dishes': []
    })

    # Проверяем, что response содержит id подменю
    assert response_json.get('id') is not None


# Создаем блюдо 1
def test_GET_ALL_3_create_dish1() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    target_submenu_id = test_data_get_all[0]['submenus'][0]['id']

    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    data = {
        'title': 'Test Dish 1',
        'description': 'This is a test dish 1',
        'price': 19.99
    }
    response = requests.post(url, json=data)

    # Проверяем, что запрос вернул код 201 CREATED
    assert response.status_code == 201
    response_json = response.json()

    # Сохраняем данные в словарь test_data
    test_data_get_all[0]['submenus'][0]['dishes'].append({
        'id': response_json.get('id'),
        'title': response_json.get('title'),
        'description': response_json.get('description'),
        'price': float(response_json.get('price'))
    })

    # Проверяем, что response содержит id
    assert response_json.get('id') is not None

# Создаем блюдо 2


def test_GET_ALL_4_create_dish2() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    target_submenu_id = test_data_get_all[0]['submenus'][0]['id']

    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    data = {
        'title': 'Test Dish 2',
        'description': 'This is a test dish 2',
        'price': 119.99
    }
    response = requests.post(url, json=data)

    # Проверяем, что запрос вернул код 201 CREATED
    assert response.status_code == 201
    response_json = response.json()

    # Сохраняем данные в словарь test_data
    test_data_get_all[0]['submenus'][0]['dishes'].append({
        'id': response_json.get('id'),
        'title': response_json.get('title'),
        'description': response_json.get('description'),
        'price': float(response_json.get('price'))
    })

    # Проверяем, что response содержит id блюда
    assert response_json.get('id') is not None

# Просматриваем всё содержимое базы одним запросом


def test_GET_ALL_5_view_all() -> None:
    url = f'{prefix}/all_menus_with_content/'
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    # Проверяем, что response содержит весь список объектов в нужной структуре
    assert response_json == test_data_get_all

# Удаляем блюдо


def test_GET_ALL_6_delete_dish() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    target_submenu_id = test_data_get_all[0]['submenus'][0]['id']
    target_dish_id = test_data_get_all[0]['submenus'][0]['dishes'][1]['id']
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    response = requests.delete(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

# Просматриваем всё содержимое базы после удаления одного блюда одним запросом


def test_GET_ALL_7_view_all() -> None:
    url = f'{prefix}/all_menus_with_content/'
    test_data_get_all[0]['submenus'][0]['dishes'].pop(1)
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    # Проверяем, что response содержит весь список объектов в нужной структуре
    assert response_json == test_data_get_all

# Удаляем меню чтобы удалилось всё с ним связанное


def test_GET_ALL_8_delete_menu() -> None:
    target_menu_id = test_data_get_all[0].get('id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200

# Просматриваем всё содержимое базы после удаления всего


def test_GET_ALL_9_view_all() -> None:
    url = f'{prefix}/all_menus_with_content/'
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    # Проверяем, что response содержит пустой список
    assert response_json == []
