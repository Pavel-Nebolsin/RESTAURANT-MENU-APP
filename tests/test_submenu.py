import requests
from tests_config import prefix, test_data


# Создаем меню
def test_SUBMENU_9_create_menu() -> None:
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }
    response = requests.post(url, json=data)

    assert response.status_code == 201

    target_menu_id = response.json().get('id')
    assert target_menu_id is not None

    test_data['target_menu_id'] = target_menu_id


# Просматриваем список подменю
def test_SUBMENU_1_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Создаем подменю
def test_SUBMENU_2_create_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    data = {
        'title': 'Test Submenu',
        'description': 'This is a test submenu'
    }
    response = requests.post(url, json=data)

    assert response.status_code == 201

    test_data['target_submenu_id'] = response.json().get('id')
    test_data['target_submenu_title'] = response.json().get('title')
    test_data['target_submenu_description'] = response.json().get('description')

    assert test_data['target_submenu_id'] is not None
    assert test_data['target_submenu_title'] == 'Test Submenu'
    assert test_data['target_submenu_description'] == 'This is a test submenu'


# Просматриваем список подменю
def test_SUBMENU_3_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() != []


# Просматриваем определенное подменю
def test_SUBMENU_4_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == target_submenu_id
    assert response_json['title'] == test_data.get('target_submenu_title')
    assert response_json['description'] == test_data.get('target_submenu_description')


# Обновляем определенное подменю
def test_SUBMENU_5_update_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    data = {
        'title': 'Updated Submenu',
        'description': 'This is an updated submenu'
    }
    response = requests.patch(url, json=data)

    assert response.status_code == 200

    response_json = response.json()
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
def test_SUBMENU_6_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == test_data.get('target_submenu_id')
    assert response_json['title'] == test_data.get('target_submenu_title')
    assert response_json['description'] == test_data.get('target_submenu_description')


# Удаляем подменю
def test_SUBMENU_7_delete_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.delete(url)

    assert response.status_code == 200


# Просматриваем список подменю
def test_SUBMENU_8_list_submenus() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Просматриваем определенное подменю
def test_SUBMENU_9_view_submenu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


# Удаляем меню
def test_SUBMENU_10_delete_menu() -> None:
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматриваем список меню
def test_SUBMENU_11_get_menus() -> None:
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []
