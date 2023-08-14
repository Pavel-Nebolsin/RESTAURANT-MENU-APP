import copy
import logging
import uuid
from typing import Any

import api_requests
import openpyxl
from celery import Celery

logging.basicConfig(level=logging.INFO)

app = Celery('tasks',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://')

new_objects_dict: Any = {'menus': [], 'submenus': [], 'dishes': []}
old_objects_dict: Any = {'menus': [], 'submenus': [], 'dishes': []}

data_to_process: Any = {
    'to_add': {'menus': [], 'submenus': [], 'dishes': []},
    'to_update': {'menus': [], 'submenus': [], 'dishes': []},
    'to_delete': {'menus': [], 'submenus': [], 'dishes': []}
}


@app.task()
def periodic_task():
    main_task('/admin/Menu.xlsx')


app.conf.beat_schedule = {
    'run-every-15-seconds': {
        'task': 'tasks.periodic_task',
        'schedule': 10.0,
    },
}


def clean_data_to_process():
    for key in data_to_process:
        data_to_process[key] = {'menus': [], 'submenus': [], 'dishes': []}


def replace_list_in_list(main_list, replacement_list, data_type):
    idx_list = {'menus': 0,
                'submenus': 1,
                'dishes': 2}
    idx = idx_list[data_type]
    target = replacement_list[idx]
    for i, sublist in enumerate(main_list):
        if len(sublist) > 0 and sublist[idx] == target:
            main_list[i] = replacement_list


def remove_list_from_list(main_list, target_list):
    main_list[:] = [sublist for sublist in main_list if sublist != target_list]


def process_objects(objects, operation):
    if operation == 'to_delete':
        for data_type in ['dishes', 'submenus', 'menus']:
            for obj in objects[data_type]:
                api_requests.process[data_type](*obj, operation_type=operation)
                remove_list_from_list(old_objects_dict[data_type], obj)

    else:
        for data_type in ['menus', 'submenus', 'dishes']:
            for obj in objects[data_type]:
                api_requests.process[data_type](*obj, operation_type=operation)
                replace_list_in_list(old_objects_dict[data_type], obj, data_type)


def process_new_data(*args):
    for process_type in args:
        process_objects(data_to_process[process_type], process_type)


def compare_lists(list1, list2):
    missing_lists = []

    for sublist in list1:
        if sublist not in list2:
            missing_lists.append(sublist)

    return missing_lists


def is_valid_uuid(uuid_string):
    try:
        uuid_string = str(uuid_string)
        uuid_obj = uuid.UUID(uuid_string)
        return str(uuid_obj) == uuid_string
    except ValueError:
        return False


def add_or_update(old_list, new_list, model):
    add = new_list.copy()
    update = []
    idx_list = {'menus': 0,
                'submenus': 1,
                'dishes': 2}
    idx = idx_list[model]

    for i, new_obj in enumerate(new_list):
        for old_obj in old_list:
            if new_obj[idx] == old_obj[idx]:
                update.append(add.pop(i))

    return add, update


def check_for_added_or_updated(new_dict, old_dict):
    for model_type in ['menus', 'submenus', 'dishes']:
        objects_to_add_or_update = compare_lists(new_dict[model_type], old_dict[model_type])
        to_add, to_update = add_or_update(old_dict[model_type], objects_to_add_or_update, model=model_type)
        data_to_process['to_add'][model_type] += to_add
        data_to_process['to_update'][model_type] += to_update


def check_for_deleted(new_dict, old_dict):
    for model_type in ['menus', 'submenus', 'dishes']:
        objects_to_delete = compare_lists(old_dict[model_type], new_dict[model_type])
        data_to_process['to_delete'][model_type] += objects_to_delete


def parse_xlsx(url):
    wb = openpyxl.load_workbook(url)
    sheet = wb.active

    last_menu_id = None
    last_submenu_id = None

    menus = []
    submenus = []
    dishes = []

    for row in sheet.iter_rows(values_only=True):
        if is_valid_uuid(row[0]):
            last_menu_id = row[0]
            menus.append([row[0], row[1], row[2]])
        elif is_valid_uuid(row[1]):
            last_submenu_id = row[1]
            submenus.append([last_menu_id, row[1], row[2], row[3]])
        elif is_valid_uuid(row[2]):
            dishes.append([last_menu_id, last_submenu_id, row[2], row[3], row[4], row[5]])
    result = {'menus': menus, 'submenus': submenus, 'dishes': dishes}
    return result


def main_task(url):
    global new_objects_dict
    global old_objects_dict

    new_objects_dict = parse_xlsx(url)
    print('new:', new_objects_dict['menus'], new_objects_dict['submenus'], new_objects_dict['dishes'], sep='\n')
    print('old:', old_objects_dict['menus'], old_objects_dict['submenus'], old_objects_dict['dishes'], sep='\n')
    check_for_added_or_updated(new_objects_dict, old_objects_dict)
    process_new_data('to_add', 'to_update')
    check_for_deleted(new_objects_dict, old_objects_dict)
    process_new_data('to_delete')

    print('to add', data_to_process['to_add'])
    print('to update', data_to_process['to_update'])
    print('to delete', data_to_process['to_delete'])

    old_objects_dict = copy.deepcopy(new_objects_dict)
    clean_data_to_process()
