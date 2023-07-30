import requests

prefix = 'http://main_app:8000/api/v1'

# Словарь для хранения временных данных для тестов
test_data = {}


# ТЕСТЫ МЕНЮ:
# Просматривает список меню
def test_1_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Создает меню
def test_2_create_menu():
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
def test_3_list_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() != []


# Просматривает определенное меню
def test_4_view_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == target_menu_id
    assert response_json['title'] == test_data.get('target_menu_title')
    assert response_json['description'] == test_data.get('target_menu_description')


# Обновляет меню
def test_5_update_menu():
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
def test_6_delete_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматривает список меню
def test_7_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


# Просматривает определенное меню
def test_8_view_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.get(url)

    # Проверяем, что запрос вернул 404 Not Found
    assert response.status_code == 404

    # Проверяем, что вернулось правильное сообщение о том, что меню не существует
    response_json = response.json()
    assert response_json['detail'] == 'menu not found'


# ТЕСТЫ ПОДМЕНЮ:
# Создает меню
def test_9_create_menu():
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


# Просматривает список подменю
def test_10_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Создает подменю
def test_11_create_submenu():
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


# Просматривает список подменю
def test_12_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() != []

# Просматривает определенное подменю
def test_13_view_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == target_submenu_id
    assert response_json['title'] == test_data.get('target_submenu_title')
    assert response_json['description'] == test_data.get('target_submenu_description')

# Обновляет определенное подменю
def test_14_update_submenu():
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

# Просматривает определенное подменю
def test_15_view_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 200

    response_json = response.json()
    assert response_json['id'] == test_data.get('target_submenu_id')
    assert response_json['title'] == test_data.get('target_submenu_title')
    assert response_json['description'] == test_data.get('target_submenu_description')

# Удаляет подменю
def test_16_delete_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.delete(url)

    assert response.status_code == 200

# Просматривает список подменю
def test_17_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []

# Просматривает определенное подменю
def test_18_view_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'

# Удаляет меню
def test_19_delete_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200

# Просматривает список меню
def test_20_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []




