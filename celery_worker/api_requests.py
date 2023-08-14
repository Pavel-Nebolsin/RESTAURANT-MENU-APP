import requests

prefix = 'http://main_app:8000/api/v1'


def process_menu(menu_id, title, description, operation_type):
    print(f'menu {operation_type}')
    url = f'{prefix}/menus/'
    data = {
        'id': menu_id,
        'title': title,
        'description': description
    }
    if operation_type == 'to_add':
        response = requests.post(url, json=data)
    elif operation_type == 'to_update':
        response = requests.patch(url + menu_id, json=data)
    else:
        response = requests.delete(url + menu_id)
    return response.json()


def process_submenu(menu_id, submenu_id, title, description, operation_type):
    print(f'submenu {operation_type}')
    url = f'{prefix}/menus/{menu_id}/submenus/'
    data = {
        'id': submenu_id,
        'title': title,
        'description': description
    }
    if operation_type == 'to_add':
        response = requests.post(url, json=data)
    elif operation_type == 'to_update':
        response = requests.patch(url + submenu_id, json=data)
    else:
        response = requests.delete(url + submenu_id)

    return response.json()


def process_dish(menu_id, submenu_id, dish_id, title, description, price, operation_type):
    print(f'dish {operation_type}')
    url = f'{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes/'
    data = {
        'id': dish_id,
        'title': title,
        'description': description,
        'price': price
    }
    if operation_type == 'to_add':
        response = requests.post(url, json=data)
    elif operation_type == 'to_update':
        response = requests.patch(url + dish_id, json=data)
    else:
        response = requests.delete(url + dish_id)
    return response.json()


process = {'menus': process_menu,
           'submenus': process_submenu,
           'dishes': process_dish}
