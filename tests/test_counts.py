import requests
from tests_config import prefix, test_data


# ТЕСТЫ НА ПРОВЕРКУ КОЛИЧЕСТВА БЛЮД В ПОДМЕНЮ И МЕНЮ:
# Создаем меню
def test_COUNT_1_create_menu() -> None:
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }
    response = requests.post(url, json=data)

    # Проверяем, что запрос вернул код 201 CREATED
    assert response.status_code == 201
    response_json = response.json()

    # Сохраняем данные в словарь test_data
    test_data['target_menu_id'] = response_json.get('id')
    test_data['target_menu_title'] = response_json.get('title')
    test_data['target_menu_description'] = response_json.get('description')

    # Проверяем, что response содержит id menu
    assert test_data['target_menu_id'] is not None


# Создаем подменю
def test_COUNT_2_create_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
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
    test_data['target_submenu_id'] = response_json.get('id')
    test_data['target_submenu_title'] = response_json.get('title')
    test_data['target_submenu_description'] = response_json.get('description')

    # Проверяем, что response содержит id подменю
    assert test_data['target_submenu_id'] == response_json.get('id')


# Создаем блюдо 1
def test_COUNT_3_create_dish1() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
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
    test_data['target_dish1_id'] = response_json.get('id')

    # Проверяем, что response содержит id блюда 1
    assert test_data['target_dish1_id'] is not None

# Создаем блюдо 2


def test_COUNT_4_create_dish2() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
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
    test_data['target_dish2_id'] = response_json.get('id')

    # Проверяем, что response содержит id блюда 1
    assert test_data['target_dish2_id'] is not None

# Просматриваем определенное меню


def test_COUNT_5_view_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)

    # Проверяем, что запрос вернул код 200 OK
    assert response.status_code == 200
    response_json = response.json()

    # Проверяем, что 'target_menu_id' из словаря test_data и из response равны
    assert test_data['target_menu_id'] == response_json.get('id')

    # Проверяем, что 'submenus_count' из словаря test_data и из response равны
    assert 1 == response_json.get('submenus_count')

    # Проверяем, что 'dishes_count' из словаря test_data и из response равны
    assert 2 == response_json.get('dishes_count')

# Просматриваем определенное подменю


def test_COUNT_6_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/'
    response = requests.get(url)

    # Проверяем, что запрос вернул код 200 OK
    assert response.status_code == 200
    response_json = response.json()

    # Проверяем, что 'target_submenu_id' из словаря test_data и из response равны
    assert test_data['target_submenu_id'] == response_json.get('id')

    # Проверяем, что 'dishes_count' из response равен 2
    assert 2 == response_json.get('dishes_count')

# Удаляет подменю


def test_COUNT_7_delete_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.delete(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

# Просматриваем список подменю


def test_COUNT_8_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200
    # Проверяем, что ответ содержит пустой список подменю
    assert response.json() == []

# Просматриваем список блюд


def test_COUNT_9_get_dishes() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200
    # Проверяем, что ответ содержит пустой список блюд
    assert response.json() == []

# Просматриваем определенное меню


def test_COUNT_10_view_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)

    # Проверяем, что запрос вернул код 200 OK
    assert response.status_code == 200
    response_json = response.json()

    # Проверяем, что 'target_menu_id' из словаря test_data и из response равны
    assert test_data['target_menu_id'] == response_json.get('id')

    # Проверяем, что 'submenus_count' из response равен 0
    assert 0 == response_json.get('submenus_count')

    # Проверяем, что 'dishes_count' из response равен 0
    assert 0 == response_json.get('dishes_count')

# Удаляем меню


def test_COUNT_11_delete_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматриваем список меню
def test_COUNT_12_get_menus() -> None:
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []
