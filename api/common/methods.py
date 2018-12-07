from datetime import datetime, timedelta


def get_now():
    return datetime.now().timestamp()


def get_item_by_id(id, item_list):
    try:
        result = list(filter(lambda item: item.id == id, item_list))[0]
    except IndexError:
        result = None

    return result
