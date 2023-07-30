import requests

prefix = 'http://main_app:8000/api/v1'

# Словарь для хранения временных данных для тестов
test_data = {}


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


# ТЕСТЫ ДЛЯ ПОДМЕНЮ:
# Создаем меню
def test_SUBMENU_9_create_menu():
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
def test_SUBMENU_1_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Создаем подменю
def test_SUBMENU_2_create_submenu():
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
def test_SUBMENU_3_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() != []


# Просматриваем определенное подменю
def test_SUBMENU_4_view_submenu():
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
def test_SUBMENU_5_update_submenu():
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
def test_SUBMENU_6_view_submenu():
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
def test_SUBMENU_7_delete_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.delete(url)

    assert response.status_code == 200


# Просматриваем список подменю
def test_SUBMENU_8_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json() == []


# Просматриваем определенное подменю
def test_SUBMENU_9_view_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.get(url)

    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


# Удаляем меню
def test_SUBMENU_10_delete_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматриваем список меню
def test_SUBMENU_11_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []


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


# ТЕСТЫ НА ПРОВЕРКУ КОЛИЧЕСТВА БЛЮД В ПОДМЕНЮ И МЕНЮ:
# Создаем меню
def test_COUNT_1_create_menu():
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
def test_COUNT_2_create_submenu():
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
def test_COUNT_3_create_dish1():
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
def test_COUNT_4_create_dish2():
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

import requests

prefix = 'http://main_app:8000/api/v1'

# Просматриваем определенное меню
def test_COUNT_5_view_menu():
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
def test_COUNT_6_view_submenu():
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
def test_COUNT_7_delete_submenu():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}'
    response = requests.delete(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200

# Просматриваем список подменю
def test_COUNT_8_list_submenus():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200
    # Проверяем, что ответ содержит пустой список подменю
    assert response.json() == []

# Просматриваем список блюд
def test_COUNT_9_get_dishes():
    target_menu_id = test_data.get('target_menu_id')
    target_submenu_id = test_data.get('target_submenu_id')
    url = f'{prefix}/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    response = requests.get(url)

    # Проверяем, что запрос вернул статус 200 OK
    assert response.status_code == 200
    # Проверяем, что ответ содержит пустой список блюд
    assert response.json() == []

# Просматриваем определенное меню
def test_COUNT_10_view_menu():
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
def test_COUNT_11_delete_menu():
    target_menu_id = test_data.get('target_menu_id')
    url = f'{prefix}/menus/{target_menu_id}/'
    response = requests.delete(url)
    assert response.status_code == 200


# Просматриваем список меню
def test_COUNT_12_get_menus():
    url = f'{prefix}/menus/'
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == []