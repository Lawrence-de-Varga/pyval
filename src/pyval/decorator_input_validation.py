def is_type_list(type_list: list):
    return all(isinstance(item, type) for item in type_list)
