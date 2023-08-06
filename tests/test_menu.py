import requests
from tests_config import prefix, test_data


# ТЕСТЫ ДЛЯ МЕНЮ:
# Просматриваем список меню
def test_MENU_1_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Создаем меню
def test_MENU_2_create_menu():
    url = f'{prefix}/menus/'
    data = {
        'title': 'Test Menu',
        'description': 'This is a test menu'
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201

    test_data['target_menu_id'] = response.json().get('id')
    test_data['target_menu_title'] = response.json().get('title')
    test_data['target_menu_description'] = response.json().get('description')

    assert test_data['target_menu_id'] is not None
    assert test_data['target_menu_title'] == 'Test Menu'
    assert test_data['target_menu_description'] == 'This is a test menu'


# Просматриваем список меню
def test_MENU_3_list_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() != []


# Просматриваем определенное меню
def test_MENU_4_view_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == target_menu_id
    assert response_json['title'] == test_data.get('target_menu_title')
    assert response_json['description'] == test_data.get('target_menu_description')


# Обновляем меню
def test_MENU_5_update_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    data = {
        'title': 'Updated Test Menu',
        'description': 'This is an updated test menu'
    }
    response = requests.patch(url, json=data)
    assert response.status_code == 200

    # Проверяем, что данные изменились
    assert test_data['target_menu_title'] != data['title']
    assert test_data['target_menu_description'] != data['description']

    # Сохраняем обновленные данные в словарь
    test_data['target_menu_title'] = data['title']
    test_data['target_menu_description'] = data['description']

    # Проверяем, что данные соответствуют обновленным данным
    assert test_data['target_menu_title'] == response.json().get('title')
    assert test_data['target_menu_description'] == response.json().get('description')


# Удаляем меню
def test_MENU_6_delete_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматриваем список меню
def test_MENU_7_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Просматриваем определенное меню
def test_MENU_8_view_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)

    # Проверяем, что запрос вернул 404 Not Found
    assert response.status_code == 404

    # Проверяем, что вернулось правильное сообщение о том, что меню не существует
    response_json = response.json()
    assert response_json['detail'] == 'menu not found'
