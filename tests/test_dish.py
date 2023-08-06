import requests
from tests_config import prefix, test_data


# ТЕСТЫ ДЛЯ БЛЮД:
# Создаем меню
def test_DISH_1_create_menu():
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


# Создаем подменю
def test_DISH_2_create_submenu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    data = {
        'title': 'Test Submenu',
        'description': 'This is a test submenu'
    }
    response = requests.post(url, json=data)

    assert response.status_code == 201

    test_data['target_submenu_id'] = response.json().get('id')

    assert test_data['target_submenu_id'] is not None


# Просматриваем список блюд
def test_DISH_3_view_dishes():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    response = requests.get(url)

    assert response.status_code == 200

    assert response.json() == []


# Создаем блюдо
def test_DISH_4_create_dish():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    data = {
        'title': 'Test Dish',
        'description': 'This is a test dish',
        'price': 10.99
    }
    response = requests.post(url, json=data)

    # Проверяем, что запрос вернул статус 201 CREATED
    assert response.status_code == 201

    # Сохраняем данные о созданном блюде в словаре test_data
    test_data['target_dish_id'] = response.json().get('id')
    test_data['target_dish_title'] = response.json().get('title')
    test_data['target_dish_description'] = response.json().get('description')
    test_data['target_dish_price'] = response.json().get('price')

    # Проверяем, что данные из ответа совпадают с сохраненными в словаре test_data
    assert test_data['target_dish_id'] is not None
    assert test_data['target_dish_title'] == 'Test Dish'
    assert test_data['target_dish_description'] == 'This is a test dish'
    assert test_data['target_dish_price'] == '10.99'


# Просматриваем список блюд
def test_DISH_5_get_dishes():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

    # Проверяем, что ответ содержит не пустой список блюд
    assert response.json() != []


# Просматриваем определенное блюдо
def test_DISH_6_view_dish():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

    # Проверяем, что ответ содержит ожидаемое блюдо
    response_json = response.json()
    assert response_json['id'] == target_dish_id
    assert response_json['title'] == test_data['target_dish_title']
    assert response_json['description'] == test_data['target_dish_description']
    assert response_json['price'] == test_data['target_dish_price']


# Обновляем блюдо
def test_DISH_7_update_dish():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    data = {
        'title': 'Updated Test Dish',
        'description': 'This is an updated test dish',
        'price': 55.55
    }
    response = requests.patch(url, json=data)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

    # Проверяем, что данные блюда были обновлены
    response_json = response.json()
    assert response_json['title'] != test_data['target_dish_title']
    assert response_json['description'] != test_data['target_dish_description']
    assert response_json['price'] != test_data['target_dish_price']

    # Сохраняем обновленные данные
    test_data['target_dish_title'] = response_json['title']
    test_data['target_dish_description'] = response_json['description']
    test_data['target_dish_price'] = response_json['price']


# Просматриваем определенное блюдо
def test_DISH_8_view_dish():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

    # Проверяем, что данные полученного блюда соответствуют сохраненным данным
    response_json = response.json()
    assert response_json['id'] == test_data['target_dish_id']
    assert response_json['title'] == test_data['target_dish_title']
    assert response_json['description'] == test_data['target_dish_description']
    assert response_json['price'] == test_data['target_dish_price']


# Удаляем блюдо
def test_DISH_9_delete_dish():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    response = requests.delete(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200


# Просматриваем список блюд
def test_DISH_10_get_dishes():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

    # Проверяем, что ответ содержит пустой список блюд
    assert response.json() == []


# Просматриваем определённое блюдо
def test_DISH_11_view_dish():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    target_dish_id = test_data.get('target_dish_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 404 NOT FOUND
    assert response.status_code == 404

    # Проверяем, что в ответе содержится ожидаемое сообщение
    assert response.json()['detail'] == 'dish not found'


# Удаляет подменю
def test_DISH_12_delete_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.delete(url)

    assert response.status_code == 200


# Просматриваем список подменю
def test_DISH_13_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Удаляем меню
def test_DISH_14_delete_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматриваем список меню
def test_DISH_15_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []
