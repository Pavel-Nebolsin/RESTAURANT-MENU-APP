import requests

prefix = 'http://main_app:8000/api/v1'

# Словарь для хранения временных данных для тестов
test_data = {}

# ТЕСТЫ МЕНЮ:

# Просматривает список меню
def test_get_menus_1():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Создает меню
def test_create_menu_2():
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


# Просматривает список меню
def test_list_menus_3():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() != []


# Просматривает определенное меню
def test_view_menu_4():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == target_menu_id
    assert response_json['title'] == test_data.get('target_menu_title')
    assert response_json['description'] == test_data.get('target_menu_description')


# Обновляет меню
def test_update_menu_5():
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

# Удаляет меню
def test_delete_menu_6():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматривает список меню
def test_get_menus_7():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Просматривает определенное меню
def test_view_menu_8():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)

    # Проверяем, что запрос вернул 404 Not Found
    assert response.status_code == 404

    # Проверяем, что вернулось правильное сообщение о том, что меню не существует
    response_json = response.json()
    assert response_json['detail'] == 'menu not found'

