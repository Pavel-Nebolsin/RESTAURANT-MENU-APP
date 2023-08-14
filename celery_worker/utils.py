import uuid


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
